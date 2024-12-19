import { json } from '@sveltejs/kit'

export async function POST({ request }) {
  const data = await request.json();
  
  const response = await fetch('http://localhost:8000/query/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  });
  
  const result = await response.json();
  return json(result);
}