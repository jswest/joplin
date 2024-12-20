import { json } from "@sveltejs/kit";

import { FASTAPI_PORT } from "$lib/config.js";

export async function GET({ params }) {
  const response = await fetch(
    `http://localhost:${FASTAPI_PORT}/documents/${params.id}}`
  );
  const documents = await response.json();
  return json(documents);
}
