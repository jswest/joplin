import { ChromaClient } from "chromadb";
import { json } from "@sveltejs/kit";

import { getTags } from "$lib/utils.js";

const client = new ChromaClient();

export async function POST({ params, request }) {
  const { tags } = await request.json();
  try {
    const documents = await client.getCollection({ name: "documents" });
    const prevRes = await documents.get({
      ids: [params.id],
      include: ["embeddings", "metadatas"],
    });
    const nextMeta = { ...prevRes.metadatas[0] };
    const extantTags = getTags(prevRes.metadatas[0].tags);
    const nextTags = [
      ...new Set([
        ...getTags(tags).map((tag) => tag.toLowerCase()),
        ...extantTags,
      ]),
    ].sort();
    nextMeta.tags = nextTags.join(",");
    console.log(nextMeta);
    await documents.update({
      ids: [params.id],
      embeddings: prevRes.embeddings,
      metadatas: [nextMeta],
    });
    return json(nextMeta);
  } catch (error) {
    console.error(error);
    return json({ error: error.message });
  }
}

export async function DELETE({ params, request }) {
  const { tag } = await request.json();
  try {
    const documents = await client.getCollection({ name: "documents" });
    const prevRes = await documents.get({
      ids: [params.id],
      include: ["embeddings", "metadatas"],
    });
    const nextMeta = { ...prevRes.metadatas[0] };
    const extantTags = getTags(prevRes.metadatas[0].tags);
    const nextTags = extantTags.filter((t) => t !== tag);
    nextMeta.tags = nextTags.join(",");
    await documents.update({
      ids: [params.id],
      embeddings: prevRes.embeddings,
      metadatas: [nextMeta],
    });
    return json(nextMeta);
  } catch (error) {
    console.error(error);
    return json({ error: error.message });
  }
}
