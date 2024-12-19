import { json } from '@sveltejs/kit'

export async function GET() {
  const response = await fetch('http://localhost:8000/documents/');
  const documents = await response.json();
  return json(documents);
}