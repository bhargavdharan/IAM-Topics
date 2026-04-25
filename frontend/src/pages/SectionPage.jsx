import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

const API_URL = 'http://localhost:5000/api'

function SectionPage() {
  const { id } = useParams()
  const [section, setSection] = useState(null)
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [simOutput, setSimOutput] = useState('')

  useEffect(() => {
    setLoading(true)
    axios.get(`${API_URL}/sections/${id}`)
      .then(res => {
        setSection(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [id])

  const runSimulation = (projectName) => {
    setRunning(true)
    setSimOutput('Running...')
    axios.post(`${API_URL}/sections/${id}/run`, { project: projectName })
      .then(res => {
        setSimOutput(res.data.stdout || res.data.stderr || 'No output')
        setRunning(false)
      })
      .catch(err => {
        setSimOutput('Error: ' + (err.response?.data?.error || err.message))
        setRunning(false)
      })
  }

  if (loading) return <div className="text-center p-5">Loading...</div>
  if (!section) return <div className="text-center p-5">Section not found</div>

  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-8">
          <article className="prose">
            <ReactMarkdown>{section.content}</ReactMarkdown>
          </article>
        </div>
        
        <div className="col-lg-4">
          <div className="sticky-top" style={{ top: '20px' }}>
            <div className="card mb-4">
              <div className="card-header bg-dark text-white">
                🎮 Interactive Simulations
              </div>
              <div className="card-body">
                {section.projects.length === 0 ? (
                  <p className="text-muted">No simulations available for this section.</p>
                ) : (
                  section.projects.map(proj => (
                    <div className="mb-3" key={proj.name}>
                      <button 
                        className="btn btn-sm btn-success w-100"
                        onClick={() => runSimulation(proj.name)}
                        disabled={running}
                      >
                        ▶️ Run {proj.name}
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
            
            {simOutput && (
              <div className="card">
                <div className="card-header">Output</div>
                <div className="card-body">
                  <pre className="small" style={{ maxHeight: '400px', overflow: 'auto' }}>
                    <code>{simOutput}</code>
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default SectionPage
