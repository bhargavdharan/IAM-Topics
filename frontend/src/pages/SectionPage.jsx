import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

const API_URL = 'http://localhost:5000/api'

function SectionPage() {
  const { id } = useParams()
  const [section, setSection] = useState(null)
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [simOutput, setSimOutput] = useState('')
  const [activeTab, setActiveTab] = useState('content')
  const [quizMode, setQuizMode] = useState(false)
  const [currentQ, setCurrentQ] = useState(0)
  const [score, setScore] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)

  useEffect(() => {
    setLoading(true)
    setSimOutput('')
    setActiveTab('content')
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
    setSimOutput('Running simulation...')
    setActiveTab('simulation')
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

  const extractQuiz = (content) => {
    if (!content) return []
    const match = content.match(/## 📝 Quiz Questions([\s\S]*?)(?=## |$)/)
    if (!match) return []
    const lines = match[1].split('\n').filter(l => l.trim().match(/^\d+\./))
    return lines.map(l => l.replace(/^\s*\d+\.\s*/, '')).filter(l => l.length > 10)
  }

  const quizQuestions = extractQuiz(section?.content)

  const handleQuizAnswer = (correct) => {
    if (correct) setScore(s => s + 1)
    setShowAnswer(true)
    setTimeout(() => {
      setShowAnswer(false)
      setCurrentQ(q => q + 1)
    }, 2000)
  }

  if (loading) return (
    <div className="d-flex justify-content-center align-items-center" style={{height: '60vh'}}>
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  )
  if (!section) return <div className="container p-5 text-center">Section not found</div>

  const prevSection = parseInt(id) > 1 ? parseInt(id) - 1 : null
  const nextSection = parseInt(id) < 15 ? parseInt(id) + 1 : null

  return (
    <div className="container">
      {/* Navigation Breadcrumb */}
      <nav aria-label="breadcrumb" className="mb-3">
        <ol className="breadcrumb">
          <li className="breadcrumb-item"><Link to="/">Home</Link></li>
          <li className="breadcrumb-item active">Section {id}</li>
        </ol>
      </nav>

      {/* Section Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h2">Section {id}</h1>
        <div>
          {prevSection && (
            <Link to={`/section/${prevSection}`} className="btn btn-outline-secondary btn-sm me-2">
              ← Previous
            </Link>
          )}
          {nextSection && (
            <Link to={`/section/${nextSection}`} className="btn btn-outline-primary btn-sm">
              Next →
            </Link>
          )}
        </div>
      </div>

      {/* Tab Navigation */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button className={`nav-link ${activeTab === 'content' ? 'active' : ''}`}
            onClick={() => setActiveTab('content')}>
            📖 Content
          </button>
        </li>
        <li className="nav-item">
          <button className={`nav-link ${activeTab === 'simulation' ? 'active' : ''}`}
            onClick={() => setActiveTab('simulation')}>
            🎮 Simulations
          </button>
        </li>
        {quizQuestions.length > 0 && (
          <li className="nav-item">
            <button className={`nav-link ${activeTab === 'quiz' ? 'active' : ''}`}
              onClick={() => { setActiveTab('quiz'); setQuizMode(true); setCurrentQ(0); setScore(0); }}>
              🧠 Quiz ({quizQuestions.length})
            </button>
          </li>
        )}
      </ul>

      {/* Content Tab */}
      {activeTab === 'content' && (
        <div className="row">
          <div className="col-lg-8">
            <article className="prose bg-white p-4 rounded shadow-sm">
              <ReactMarkdown>{section.content}</ReactMarkdown>
            </article>
          </div>
          <div className="col-lg-4">
            <div className="card shadow-sm">
              <div className="card-header bg-primary text-white">
                🎮 Available Simulations
              </div>
              <div className="list-group list-group-flush">
                {section.projects.length === 0 ? (
                  <div className="list-group-item text-muted">No simulations yet</div>
                ) : (
                  section.projects.map(proj => (
                    <button key={proj.name}
                      className="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                      onClick={() => runSimulation(proj.name)}>
                      <span>▶️ {proj.name.replace('.py', '').replace(/_/g, ' ')}</span>
                      <span className="badge bg-success rounded-pill">Run</span>
                    </button>
                  ))
                )}
              </div>
            </div>

            <div className="card mt-3 shadow-sm">
              <div className="card-header bg-info text-white">
                📚 Learning Path
              </div>
              <div className="card-body">
                <div className="progress mb-2">
                  <div className="progress-bar" style={{width: `${(id/15)*100}%`}}>
                    {Math.round((id/15)*100)}%
                  </div>
                </div>
                <small className="text-muted">Section {id} of 15</small>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Simulation Tab */}
      {activeTab === 'simulation' && (
        <div className="row">
          <div className="col-lg-4">
            <div className="card shadow-sm">
              <div className="card-header bg-dark text-white">
                🎮 Simulations
              </div>
              <div className="card-body">
                {section.projects.length === 0 ? (
                  <p className="text-muted">No simulations available.</p>
                ) : (
                  section.projects.map(proj => (
                    <div className="mb-2" key={proj.name}>
                      <button 
                        className="btn btn-sm btn-success w-100"
                        onClick={() => runSimulation(proj.name)}
                        disabled={running}>
                        {running ? '⏳ Running...' : `▶️ ${proj.name.replace('.py', '').replace(/_/g, ' ')}`}
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
          <div className="col-lg-8">
            <div className="card shadow-sm">
              <div className="card-header d-flex justify-content-between align-items-center">
                <span>📟 Terminal Output</span>
                {simOutput && (
                  <button className="btn btn-sm btn-outline-secondary" onClick={() => setSimOutput('')}>
                    Clear
                  </button>
                )}
              </div>
              <div className="card-body p-0">
                {simOutput ? (
                  <pre className="small m-0 p-3 bg-dark text-light" style={{ maxHeight: '600px', overflow: 'auto', minHeight: '300px' }}>
                    <code>{simOutput}</code>
                  </pre>
                ) : (
                  <div className="p-5 text-center text-muted">
                    <p>Select a simulation to run</p>
                    <p className="small">Output will appear here</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quiz Tab */}
      {activeTab === 'quiz' && quizMode && (
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card shadow">
              <div className="card-header bg-warning text-dark d-flex justify-content-between">
                <span>🧠 Knowledge Check</span>
                <span>Score: {score}/{quizQuestions.length}</span>
              </div>
              <div className="card-body text-center p-5">
                {currentQ < quizQuestions.length ? (
                  <>
                    <div className="mb-4">
                      <span className="badge bg-secondary">Question {currentQ + 1} of {quizQuestions.length}</span>
                    </div>
                    <h4 className="mb-4">{quizQuestions[currentQ]}</h4>
                    
                    {showAnswer ? (
                      <div className="alert alert-info">
                        <strong>💡 Think about it!</strong>
                        <p className="mt-2">Review the content above to find the answer.</p>
                      </div>
                    ) : (
                      <div className="d-grid gap-2 d-md-flex justify-content-md-center">
                        <button className="btn btn-primary" onClick={() => handleQuizAnswer(true)}>
                          I Know This! ✅
                        </button>
                        <button className="btn btn-outline-secondary" onClick={() => handleQuizAnswer(false)}>
                          Need to Review 📖
                        </button>
                      </div>
                    )}
                  </>
                ) : (
                  <div>
                    <h3>🎉 Quiz Complete!</h3>
                    <div className="display-4 my-4">{score}/{quizQuestions.length}</div>
                    <p className="lead">
                      {score === quizQuestions.length ? 'Perfect! You mastered this section!' :
                       score >= quizQuestions.length * 0.7 ? 'Great job! Keep learning!' :
                       'Review the content and try again!'}
                    </p>
                    <button className="btn btn-primary" onClick={() => {setCurrentQ(0); setScore(0);}}>
                      Retry Quiz 🔄
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SectionPage
