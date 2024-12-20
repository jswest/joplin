import { ChromaClient } from "chromadb";
import { json } from "@sveltejs/kit";

import { getArrayField } from "$lib/utils.js";

const client = new ChromaClient();

export async function PUT({ params, request }) {
  const { authors, dek, hed, year } = await request.json();
  try {
    const documents = await client.getCollection({ name: "documents" });
    const prevRes = await documents.get({
      ids: [params.id],
      include: ["embeddings", "metadatas"],
    });
    const nextMeta = { ...prevRes.metadatas[0] };
    nextMeta.authors = getArrayField(authors).join(",");
    nextMeta.dek = dek;
    nextMeta.hed = hed;
    nextMeta.year = year;
    console.log(nextMeta)
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
