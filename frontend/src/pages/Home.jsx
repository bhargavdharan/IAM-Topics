import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

function Home() {
  const [sections, setSections] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    axios.get(`${API_URL}/sections`)
      .then(res => {
        setSections(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  const filteredSections = sections.filter(s => 
    s.title.toLowerCase().includes(searchQuery.toLowerCase())
  )

  if (loading) return (
    <div className="d-flex justify-content-center align-items-center" style={{height: '60vh'}}>
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  )

  return (
    <div className="container">
      {/* Hero Section */}
      <div className="p-5 mb-4 bg-dark rounded-3 text-white">
        <div className="container-fluid py-5">
          <h1 className="display-5 fw-bold">🔐 Identity & Access Management</h1>
          <p className="col-md-8 fs-4">
            From <strong>Zero to IAM Hero</strong> — A complete learning journey with 
            real-world analogies, technical deep-dives, and hands-on simulations.
          </p>
          <div className="d-flex gap-3">
            <Link to="/section/1" className="btn btn-primary btn-lg">Start Learning →</Link>
            <a href="https://github.com" className="btn btn-outline-light btn-lg">⭐ Star on GitHub</a>
          </div>
        </div>
      </div>

      {/* Stats Row */}
      <div className="row align-items-md-stretch mb-5">
        <div className="col-md-4">
          <div className="h-100 p-5 text-white bg-primary rounded-3">
            <h2>15 Topics</h2>
            <p>From authentication fundamentals to Zero Trust and decentralized identity.</p>
          </div>
        </div>
        <div className="col-md-4">
          <div className="h-100 p-5 bg-light border rounded-3">
            <h2>🎮 30+ Simulations</h2>
            <p>Interactive Python demos you can run to see concepts in action.</p>
          </div>
        </div>
        <div className="col-md-4">
          <div className="h-100 p-5 text-white bg-success rounded-3">
            <h2>👥 For Everyone</h2>
            <p>Written for non-technical students with "Under the Hood" sections for engineers.</p>
          </div>
        </div>
      </div>

      {/* How to Use */}
      <div className="alert alert-info d-flex align-items-center mb-4">
        <div className="flex-shrink-0">
          <span className="fs-3">💡</span>
        </div>
        <div className="flex-grow-1 ms-3">
          <strong>How to use this platform:</strong>
          <ul className="mb-0">
            <li><strong>Non-technical?</strong> Read the analogies and key concept tables. Skip "Under the Hood" if you want.</li>
            <li><strong>Technical?</strong> Run the Python simulations in each section's <code>projects/</code> folder.</li>
            <li><strong>Developers?</strong> Start the Flask backend + React frontend for the full interactive experience.</li>
          </ul>
        </div>
      </div>

      {/* Search */}
      <div className="mb-4">
        <div className="input-group input-group-lg">
          <span className="input-group-text">🔍</span>
          <input 
            type="text" 
            className="form-control" 
            placeholder="Search topics..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Sections Grid */}
      <h2 className="mb-4">📚 Learning Modules</h2>
      <div className="row">
        {filteredSections.map(section => (
          <div className="col-md-6 col-lg-4 mb-4" key={section.id}>
            <div className="card h-100 shadow-sm border-0 hover-shadow">
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <span className="badge bg-primary rounded-pill">#{section.id}</span>
                  <span className="text-muted small">Module {section.id}/15</span>
                </div>
                <h5 className="card-title">{section.title}</h5>
                <p className="card-text text-muted small">
                  {section.title.includes('Introduction') && 'Foundations of IAM'}
                  {section.title.includes('Authentication') && 'Passwords, biometrics, and proving identity'}
                  {section.title.includes('Multi-Factor') && 'Why one lock is not enough'}
                  {section.title.includes('Authorization') && 'The rules that decide yes or no'}
                  {section.title.includes('Role-Based') && 'Using job titles to control access'}
                  {section.title.includes('Attribute-Based') && 'Smart, dynamic access decisions'}
                  {section.title.includes('Privileged') && 'Protecting the master keys'}
                  {section.title.includes('Single Sign-On') && 'One key for many doors'}
                  {section.title.includes('OAuth') && 'Securely sharing your data'}
                  {section.title.includes('SAML') && 'Enterprise identity federation'}
                  {section.title.includes('Identity Providers') && 'The phonebook of the digital world'}
                  {section.title.includes('Governance') && 'Compliance and access reviews'}
                  {section.title.includes('Zero Trust') && 'Never trust, always verify'}
                  {section.title.includes('Cloud') && 'Identity in AWS, Azure, and GCP'}
                  {section.title.includes('Future') && 'Passwordless, AI, and decentralized ID'}
                </p>
                <Link to={`/section/${section.id}`} className="btn btn-outline-primary btn-sm w-100">
                  Start Learning →
                </Link>
              </div>
              <div className="card-footer bg-transparent border-0">
                <small className="text-muted">
                  {section.id <= 5 ? '🟢 Beginner' : section.id <= 10 ? '🟡 Intermediate' : '🔴 Advanced'}
                </small>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Home
