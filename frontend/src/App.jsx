import { useFindlySearch } from './hooks/useFindlySearch'
import { useFindlyUpload } from './hooks/useFindlyUpload'
import { SearchBar } from './components/SearchBar'
import { AnswerCard } from './components/AnswerCard'
import { ExternalResources } from './components/ExternalResources'
import { UploadPanel } from './components/UploadPanel'
import './App.css'

function App() {
  const { result, loading, error, search } = useFindlySearch()
  const { uploading, uploadStatus, uploadText, uploadFile } = useFindlyUpload()

  return (
    <div className="app">
      <h1>Findly</h1>
      <p className="subtitle">Intelligent search powered by RAG</p>

      <SearchBar onSearch={search} loading={loading} />

      <UploadPanel
        onUploadText={uploadText}
        onUploadFile={uploadFile}
        uploading={uploading}
        uploadStatus={uploadStatus}
      />

      

      {error && <div className="error">{error}</div>}

      {result && (
        <>
          <AnswerCard answer={result.answer} sources={result.sources} />
          <ExternalResources resources={result.resources} />
        </>
      )}
    </div>
  )
}

export default App