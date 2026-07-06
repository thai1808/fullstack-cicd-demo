const BASE_URL = '/api'

export async function getNotes() {
  const res = await fetch(`${BASE_URL}/notes`)
  return res.json()
}

export async function addNote(content) {
  const res = await fetch(`${BASE_URL}/notes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content }),
  })
  return res.json()
}

export async function deleteNote(id) {
  const res = await fetch(`${BASE_URL}/notes/${id}`, { method: 'DELETE' })
  return res.json()
}
