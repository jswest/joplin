import { json } from "@sveltejs/kit";

import { FASTAPI_PORT } from "$lib/config.js";

export async function POST({ request }) {
  const data = await request.json();

  const response = await fetch(`http://localhost:${FASTAPI_PORT}/query/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();
  return json(result);
}
