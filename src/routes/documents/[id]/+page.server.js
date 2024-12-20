import { ChromaClient } from "chromadb";
import { error } from "@sveltejs/kit";
import { FASTAPI_PORT } from "$lib/config";

const client = new ChromaClient();

export async function load({ params }) {
  const documents = await client.getCollection({ name: "documents" });
  const documentResponse = await documents.get({
    ids: [params.id],
    include: ["documents", "metadatas"],
  });

  const document = documentResponse.metadatas[0];
  let data;
  if (document.format === "pdf") {
    const pdfResponse = await fetch(
      `http://localhost:${FASTAPI_PORT}/documents/${params.id}/pdf`
    );
    if (!pdfResponse.ok) {
      throw error(pdfResponse.status, "Could not load PDF");
    }
    data = await pdfResponse.arrayBuffer();
  } else {
    data = documentResponse.documents[0];
  }

  return {
    contentType: `application/${document.format === 'pdf' ? 'pdf' : 'text'}`,
    data,
    documentId: params.id,
    documentMetadata: document,
  };
}
