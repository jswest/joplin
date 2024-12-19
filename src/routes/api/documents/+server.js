import { json } from "@sveltejs/kit";

import { FASTAPI_PORT } from "$lib/config.js";

export async function GET() {
  const response = await fetch(`http://localhost:${FASTAPI_PORT}/documents/`);
  const documents = await response.json();
  return json(documents);
}
