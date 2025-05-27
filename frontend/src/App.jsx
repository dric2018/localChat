import { useState, useEffect } from 'react'

export default function App() {
  const [models, setModels] = useState([])
  const [selected, setSelected] = useState('')
  const [prompt, setPrompt] = useState('')
  const [response, setResponse] = useState('')
  const [history, setHistory] = useState([])

  useEffect(() => {
    fetch('/api/models')
      .then(res => res.json())
      .then(setModels)
  }, [])

  const loadModel = () => {
    fetch('/api/load', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: selected })
    })
  }

  const sendPrompt = () => {
    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    }).then(res => res.json())
      .then(data => {
        setResponse(data.response)
        setHistory(data.history)
      })
  }

  const handleDrop = async (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    const formData = new FormData()
    formData.append("file", file)
    await fetch('/api/upload', { method: 'POST', body: formData })
    alert(`Uploaded: ${file.name}`)
  }

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>🧠 Local GPT Chat</h2>

      <select value={selected} onChange={e => setSelected(e.target.value)} style={{ marginBottom: '0.5rem' }}>
        <option value="">Select model</option>
        {models.map(m => <option key={m}>{m}</option>)}
      </select>
      <button onClick={loadModel} style={{ marginLeft: '0.5rem' }}>Load</button>

      <textarea
        rows="4"
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        style={{ width: '100%', marginTop: '1rem' }}
      />
      <button onClick={sendPrompt} style={{ marginTop: '0.5rem' }}>Send</button>

      <div style={{ marginTop: '1rem', background: '#f0f0f0', padding: '0.5rem' }}>
        <strong>Response:</strong>
        <pre>{response}</pre>
      </div>

      <div style={{ marginTop: '1rem' }}>
        <h4>Chat History</h4>
        <ul style={{ fontSize: '0.9rem' }}>
          {history.map((h, i) => (
            <li key={i}>
              <b>User:</b> {h.q}<br />
              <b>AI:</b> {h.a}
            </li>
          ))}
        </ul>
      </div>

      <div
        onDrop={handleDrop}
        onDragOver={e => e.preventDefault()}
        style={{
          marginTop: '2rem',
          padding: '1rem',
          border: '2px dashed #ccc',
          textAlign: 'center',
          color: '#555'
        }}
      >
        Drag and drop a document here to upload
      </div>
    </div>
  )
}
