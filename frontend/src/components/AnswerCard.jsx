import './AnswerCard.css'

export function AnswerCard({ answer, sources }) {
  return (
    <div className="result">
      <h2>Answer</h2>
      <p className="answer">{answer}</p>

      <h3>Sources</h3>
      <ul className="sources">
        {sources.map((source, i) => (
          <li key={i}>{source}</li>
        ))}
      </ul>
    </div>
  )
}