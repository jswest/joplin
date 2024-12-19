import { ChromaClient } from "chromadb";
import { json } from "@sveltejs/kit";

const client = new ChromaClient();

export async function POST({ params, request }) {
  const tags = await request.json();
  try {
    const documents = await client.getCollection({ name: "documents" });
    await documents.update({
      ids: [params.id],
      metadatas: [{ tags: tags }],
    });
    const res = await documents.get({
      ids: [params.id],
      include: ["metadatas"],
    });
    return json(res.metadatas[0]);
  } catch (error) {
    console.error(error);
    return json({ error: error });
  }
}

export async function PUT({ params, request }) {
  const tags = await request.json();
  try {
    const documents = await client.getCollection({ name: "documents" });
    await documents.update({
      ids: [params.id],
      metadatas: [{ tags: tags }],
    });
    const res = await documents.get({
      ids: [params.id],
      include: ["metadatas"],
    });
    return json(res.metadatas[0]);
  } catch (error) {
    console.error(error);
    return json({ error: error });
  }
}

export async function DELETE({ params }) {
  try {
    const documents = await client.getCollection({ name: "documents" });
    await documents.update({
      ids: [params.id],
      metadatas: [{ tags: null }],
    });
    const res = await documents.get({
      ids: [params.id],
      include: ["metadatas"],
    });
    return json(res.metadatas[0]);
  } catch (error) {
    console.error(error);
    return json({ error: error });
  }
}
