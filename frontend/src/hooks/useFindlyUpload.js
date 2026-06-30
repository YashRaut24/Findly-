import { useState } from 'react'

const API_URL = 'http://localhost:8000'

export function useFindlyUpload() {
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState('')

  const uploadText = async (text) => {
    if (!text.trim()) return
    setUploading(true)
    setUploadStatus('')

    try {
      const response = await fetch(`${API_URL}/upload/text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      })
      const data = await response.json()
      setUploadStatus(data.message)
    } catch (err) {
      setUploadStatus('Upload failed. Is the backend running?')
    } finally {
      setUploading(false)
    }
  }

  const uploadFile = async (file) => {
    if (!file) return
    setUploading(true)
    setUploadStatus('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_URL}/upload/file`, {
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

  return { uploading, uploadStatus, uploadText, uploadFile }
}