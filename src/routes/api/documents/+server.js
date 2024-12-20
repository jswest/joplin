import { json } from "@sveltejs/kit";

import { FASTAPI_PORT } from "$lib/config.js";

export async function GET({ url }) {
  let documents;
  const semantic = url.searchParams.get("semantic")
  if (semantic) {
    const response = await fetch(`http://localhost:${FASTAPI_PORT}/documents/?semantic=${semantic}`);
    documents = await response.json();
  } else {
    const response = await fetch(`http://localhost:${FASTAPI_PORT}/documents/`);
    documents = await response.json();
  }
  return json(documents);
}
