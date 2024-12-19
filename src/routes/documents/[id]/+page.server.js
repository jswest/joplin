import { error } from "@sveltejs/kit";
import { FASTAPI_PORT } from "$lib/config";

export async function load({ params }) {
  const response = await fetch(
    `http://localhost:${FASTAPI_PORT}/documents/${params.id}/pdf`
  );

  if (!response.ok) {
    throw error(response.status, "Could not load PDF");
  }

  const pdfData = await response.arrayBuffer();

  return {
    pdfData: pdfData,
    contentType: "application/pdf",
  };
}
