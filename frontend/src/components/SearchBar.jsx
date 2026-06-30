import { useState } from 'react'
import './SearchBar.css'

export function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    onSearch(query)
  }

  return (
    <form onSubmit={handleSubmit} className="search-form">
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
  )
}