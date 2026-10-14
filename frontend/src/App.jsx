
import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const initialForm = {
  title: '',
  description: '',
  service: '',
  severity: 'high',
  reported_at: new Date().toISOString().slice(0, 16),
}

function App() {
  const [form, setForm] = useState(initialForm)
  const [investigation, setInvestigation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function updateField(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function submitIncident(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setInvestigation(null)

    try {
      const response = await fetch(`${API_URL}/investigations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          reported_at: new Date(form.reported_at).toISOString(),
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          typeof data.detail === 'string'
            ? data.detail
            : JSON.stringify(data.detail || 'Request failed'),
        )
      }

      setInvestigation(data)
    } catch (err) {
      setError(
        `${err.message}. Check that the backend is running and accessible.`,
      )
    } finally {
      setLoading(false)
    }
  }

  const report = investigation?.final_report

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/">
          <span className="brand-mark">II</span>
          <span>Incident Investigator</span>
        </a>
        <span className="system-label">
          <span className="status-dot" />
          AI investigation system
        </span>
      </header>

      <section className="intro">
        <p className="eyebrow">INCIDENT RESPONSE / INVESTIGATION</p>
        <h1>Find the cause.<br /><span>Not just the symptoms.</span></h1>
        <p className="intro-copy">
          Submit a production incident and let the investigation agent
          gather evidence, examine system signals, and generate a
          structured root-cause report.
        </p>
      </section>

      <div className="workspace">
        <section className="panel form-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">STEP 01</p>
              <h2>Incident details</h2>
            </div>
            <span className="step-number">01</span>
          </div>

          <form onSubmit={submitIncident}>
            <label htmlFor="title">Incident title</label>
            <input
              id="title"
              name="title"
              value={form.title}
              onChange={updateField}
              placeholder="e.g. Payment API failures"
              required
            />

            <label htmlFor="service">Affected service</label>
            <input
              id="service"
              name="service"
              value={form.service}
              onChange={updateField}
              placeholder="e.g. payment-api"
              required
            />

            <label htmlFor="description">What happened?</label>
            <textarea
              id="description"
              name="description"
              value={form.description}
              onChange={updateField}
              placeholder="Describe symptoms, impact, and when the issue began."
              rows={4}
              required
            />

            <div className="field-row">
              <div>
                <label htmlFor="severity">Severity</label>
                <select
                  id="severity"
                  name="severity"
                  value={form.severity}
                  onChange={updateField}
                >
                  <option value="critical">Critical</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>

              <div>
                <label htmlFor="reported_at">Reported at</label>
                <input
                  id="reported_at"
                  name="reported_at"
                  type="datetime-local"
                  value={form.reported_at}
                  onChange={updateField}
                  required
                />
              </div>
            </div>

            <button className="submit-button" type="submit" disabled={loading}>
              {loading ? (
                <>Investigation in progress <span className="spinner" /></>
              ) : (
                <>Start investigation <span aria-hidden="true">→</span></>
              )}
            </button>

            <p className="form-note">
              The agent will use the backend's configured investigation tools.
            </p>
          </form>

          {error && (
            <div className="error-message" role="alert">
              <strong>Investigation request failed</strong>
              <p>{error}</p>
            </div>
          )}
        </section>

        <section className="panel results-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">STEP 02</p>
              <h2>Investigation report</h2>
            </div>
            {investigation && (
              <span className={`status-badge ${investigation.status}`}>
                {investigation.status}
              </span>
            )}
          </div>

          {!investigation && !loading && (
            <div className="empty-state">
              <div className="empty-icon" aria-hidden="true">⌕</div>
              <h3>Awaiting an incident</h3>
              <p>
                Your investigation findings will appear here after you
                submit the incident details.
              </p>
              <div className="empty-checks">
                <span>01</span> Evidence collection
                <span>02</span> Root-cause analysis
                <span>03</span> Recommended actions
              </div>
            </div>
          )}

          {loading && (
            <div className="loading-state" role="status">
              <span className="large-spinner" />
              <h3>Investigating incident</h3>
              <p>The agent is collecting evidence and evaluating findings.</p>
              <p className="muted">This may take several seconds.</p>
            </div>
          )}

          {investigation && (
            <div className="report-content">
              <div className="report-summary">
                <p className="eyebrow">SUMMARY</p>
                <p>{report?.summary || 'No summary was returned.'}</p>
              </div>

              <div className="metric-grid">
                <div className="metric">
                  <span>Confidence</span>
                  <strong>
                    {Math.round(
                      (report?.confidence ?? investigation.confidence ?? 0) * 100,
                    )}%
                  </strong>
                </div>
                <div className="metric">
                  <span>Iterations</span>
                  <strong>{investigation.iteration}</strong>
                </div>
                <div className="metric">
                  <span>Tool calls</span>
                  <strong>{investigation.tool_calls?.length ?? 0}</strong>
                </div>
              </div>

              <div className="report-section">
                <h3>Probable root cause</h3>
                <p>{report?.root_cause || 'No root cause established.'}</p>
              </div>

              <div className="report-section">
                <h3>Evidence from final report</h3>
                {report?.evidence?.length ? (
                  <ul className="evidence-list">
                    {report.evidence.map((item, index) => (
                      <li key={`${item.source}-${index}`}>
                        <span className="evidence-source">{item.source}</span>
                        <p>{item.observation}</p>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted">No evidence items were returned.</p>
                )}
              </div>

              <div className="report-section">
                <h3>Recommended actions</h3>
                {report?.recommended_actions?.length ? (
                  <ul className="action-list">
                    {report.recommended_actions.map((item, index) => (
                      <li key={`${item.action}-${index}`}>
                        <span className={`priority ${item.priority.toLowerCase()}`}>
                          {item.priority}
                        </span>
                        <p>{item.action}</p>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted">No actions were recommended.</p>
                )}
              </div>

              <div className="report-section">
                <h3>Conclusion</h3>
                <p>{report?.conclusion || 'No conclusion was returned.'}</p>
              </div>

              <details className="technical-details">
                <summary>Investigation activity</summary>
                <ul>
                  {(investigation.tool_calls || []).map((call, index) => (
                    <li key={`${call.tool_name}-${index}`}>
                      <code>{call.tool_name}</code>
                      <span>{JSON.stringify(call.arguments)}</span>
                    </li>
                  ))}
                </ul>
              </details>
            </div>
          )}
        </section>
      </div>

      <footer className="footer">
        <span>AI Incident Investigator</span>
        <span>Evidence-led incident analysis</span>
      </footer>
    </main>
  )
}

export default App