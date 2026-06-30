import './ExternalResources.css'

export function ExternalResources({ resources }) {
  if (!resources) return null

  return (
    <div className="external-resources">
      <h3>Explore Further</h3>
      <div className="resource-links">
        <a href={resources.youtube.url} target="_blank" rel="noopener noreferrer" className="resource-link youtube">
          ▶ {resources.youtube.is_direct_video ? resources.youtube.title : "Search YouTube"}
        </a>

        {resources.official_docs && (
          <a href={resources.official_docs} target="_blank" rel="noopener noreferrer" className="resource-link docs">
            📘 Official Docs
          </a>
        )}

        {resources.websites && resources.websites.length > 0 && (
          <div className="dropdown-container">
            <button className="resource-link website-trigger">🌐 Top Websites ▾</button>
            <div className="dropdown-menu">
              {resources.websites.map((site, i) => (
                <a key={i} href={site.url} target="_blank" rel="noopener noreferrer" className="dropdown-item">
                  {site.title}
                </a>
              ))}
            </div>
          </div>
        )}

        <a href={resources.google_ai_mode} target="_blank" rel="noopener noreferrer" className="resource-link google-ai">
          ✦ Google AI Mode
        </a>
      </div>
    </div>
  )
}