import { useState } from 'react'
import './UploadPanel.css'

export function UploadPanel({ onUploadText, onUploadFile, uploading, uploadStatus }) {
  const [text, setText] = useState('')

  const handleTextSubmit = () => {
    onUploadText(text)
    setText('')
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) onUploadFile(file)
  }

  return (
    <div className="upload-section">
      <h3>Add Your Own Knowledge</h3>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste your own notes or text here..."
        className="upload-textarea"
        rows={4}
      />
      <div className="upload-actions">
        <button onClick={handleTextSubmit} disabled={uploading} className="upload-button">
          {uploading ? 'Uploading...' : 'Add Text'}
        </button>
        <label className="upload-file-label">
          Upload .txt / .md
          <input
            type="file"
            accept=".txt,.md"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
        </label>
      </div>
      {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
    </div>
  )
}