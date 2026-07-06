import { useEffect, useState } from 'react'
import { getNotes, addNote, deleteNote } from './api'

export default function App() {
  const [notes, setNotes] = useState([])
  const [text, setText] = useState('')

  const load = async () => setNotes(await getNotes())

  useEffect(() => { load() }, [])

  const handleAdd = async (e) => {
    e.preventDefault()
    if (!text.trim()) return
    await addNote(text.trim())
    setText('')
    load()
  }

  const handleDelete = async (id) => {
    await deleteNote(id)
    load()
  }

  return (
    <div style={{ maxWidth: 480, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>📝 Notes — CI/CD Lab</h1>
      <form onSubmit={handleAdd} style={{ display: 'flex', gap: 8 }}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Nhập ghi chú..."
          style={{ flex: 1, padding: 8 }}
        />
        <button type="submit">Thêm</button>
      </form>
      <ul>
        {notes.map((n) => (
          <li key={n.id} style={{ margin: '8px 0' }}>
            {n.content}
            <button onClick={() => handleDelete(n.id)} style={{ marginLeft: 8 }}>Xoá</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
