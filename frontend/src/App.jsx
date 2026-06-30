import { useState } from 'react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [uploadText, setUploadText] = useState('')
  const [uploadStatus, setUploadStatus] = useState('')
  const [uploading, setUploading] = useState(false)

  const handleTextUpload = async () => {
    if (!uploadText.trim()) return
    setUploading(true)
    setUploadStatus('')

    try {
      const response = await fetch('http://localhost:8000/upload/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: uploadText })
      })
      const data = await response.json()
      setUploadStatus(data.message)
      setUploadText('')
    } catch (err) {
      setUploadStatus('Upload failed. Is the backend running?')
    } finally {
      setUploading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUploading(true)
    setUploadStatus('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/upload/file', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      setUploadStatus(data.message)
    } catch (err) {
      setUploadStatus('Upload failed. Is the backend running?')
    } finally {
      setUploading(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })

      if (!response.ok) {
        throw new Error('Search failed')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Something went wrong. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>Findly</h1>
      <p className="subtitle">Intelligent search powered by RAG</p>

      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask anything about your documents..."
          className="search-input"
        />
        <button type="submit" disabled={loading} className="search-button">
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>
      <div className="upload-section">
        <h3>Add Your Own Knowledge</h3>
        <textarea
          value={uploadText}
          onChange={(e) => setUploadText(e.target.value)}
          placeholder="Paste your own notes or text here..."
          className="upload-textarea"
          rows={4}
        />
        <div className="upload-actions">
          <button onClick={handleTextUpload} disabled={uploading} className="upload-button">
            {uploading ? 'Uploading...' : 'Add Text'}
          </button>
          <label className="upload-file-label">
            Upload .txt / .md
            <input
              type="file"
              accept=".txt,.md"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
          </label>
        </div>
        {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
      </div>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h2>Answer</h2>
          <p className="answer">{result.answer}</p>

          <h3>Sources</h3>
          <ul className="sources">
            {result.sources.map((source, i) => (
              <li key={i}>{source}</li>
            ))}
          </ul>
        </div>
      )}

      {result && result.resources && (
        <div className="external-resources">
          <h3>Explore Further</h3>
          <div className="resource-links">
            <a href={result.resources.youtube.url} target="_blank" rel="noopener noreferrer" className="resource-link youtube">
              ▶ {result.resources.youtube.is_direct_video ? result.resources.youtube.title : "Search YouTube"}
            </a>

            {result.resources.official_docs && (
              <a href={result.resources.official_docs} target="_blank" rel="noopener noreferrer" className="resource-link docs">
                📘 Official Docs
              </a>
            )}

          {result.resources.websites && result.resources.websites.length > 0 && (
          <div className="dropdown-container">
            <button className="resource-link website-trigger">
              🌐 Top Websites ▾
            </button>
            <div className="dropdown-menu">
              {result.resources.websites.map((site, i) => (
                <a key={i} href={site.url} target="_blank" rel="noopener noreferrer" className="dropdown-item">
                  {site.title}
                </a>
              ))}
            </div>
          </div>
        )}
            <a href={result.resources.google_ai_mode} target="_blank" rel="noopener noreferrer" className="resource-link google-ai">
              ✦ Google AI Mode
            </a>
          </div>
        </div>
      )}
    </div>
  )
}

export default App