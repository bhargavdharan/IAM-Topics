import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

function Home() {
  const [sections, setSections] = useState([])
  const [loading, setLoading] = useState(true)

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

  if (loading) return <div className="text-center p-5">Loading...</div>

  return (
    <div className="container">
      <div className="text-center mb-5">
        <h1>🔐 Identity and Access Management</h1>
        <p className="lead">From Zero to IAM Hero — A hands-on learning journey</p>
        <div className="alert alert-info">
          <strong>For non-technical learners:</strong> Start with Section 1 and read the analogies. 
          No coding required to understand the concepts!
        </div>
      </div>

      <div className="row">
        {sections.map(section => (
          <div className="col-md-6 col-lg-4 mb-4" key={section.id}>
            <div className="card h-100 shadow-sm">
              <div className="card-body">
                <h5 className="card-title">
                  <span className="badge bg-primary me-2">{section.id}</span>
                  {section.title}
                </h5>
                <Link to={`/section/${section.id}`} className="btn btn-outline-primary btn-sm">
                  Learn More →
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Home
