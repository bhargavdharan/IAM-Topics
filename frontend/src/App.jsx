import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import SectionPage from './pages/SectionPage'

function App() {
  return (
    <div className="container-fluid">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div className="container">
          <Link className="navbar-brand" to="/">🔐 IAM Learning Platform</Link>
          <div className="navbar-nav">
            <Link className="nav-link" to="/">Home</Link>
          </div>
        </div>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/section/:id" element={<SectionPage />} />
      </Routes>
      
      <footer className="mt-5 py-4 text-center text-muted border-top">
        <small>Built with 💙 for the cybersecurity community</small>
      </footer>
    </div>
  )
}

export default App
