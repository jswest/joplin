import { ChromaClient } from "chromadb";
import { error } from "@sveltejs/kit";
import { FASTAPI_PORT } from "$lib/config";

const client = new ChromaClient();

export async function load({ params }) {
  const pdfResponse = await fetch(
    `http://localhost:${FASTAPI_PORT}/documents/${params.id}/pdf`
  );

  const documents = await client.getCollection({ name: "documents" });
  const documentResponse = await documents.get({
    ids: [params.id],
    include: ["metadatas"],
  });

  if (!pdfResponse.ok) {
    throw error(pdfResponse.status, "Could not load PDF");
  }

  const pdfData = await pdfResponse.arrayBuffer();

  return {
    contentType: "application/pdf",
    documentId: params.id,
    documentMetadata: documentResponse.metadatas[0],
    pdfData: pdfData,
  };
}
