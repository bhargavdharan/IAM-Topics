# Identity and Access Management — Complete Learning Guide

> A structured, practical guide to understanding IAM from the ground up. Written for learners who want to **understand first, then implement**.

---

## How to Use This Guide

This repository is organized into **15 progressive topics**. Each topic follows the same learning structure:

| Section | Purpose |
|---------|---------|
| **What is it?** | Clear definition in plain English |
| **Why learn this?** | Why it matters in real systems |
| **Core Concepts** | The theory you need to know |
| **How It Works** | Under-the-hood technical explanation |
| **Where You See It** | Real products, protocols, and daily life |
| **Common Misconceptions** | What beginners often get wrong |
| **How to Practice** | Specific steps to build understanding |
| **Projects** | Code you can run to see it in action |
| **Check Your Understanding** | Questions to test yourself |

### Two Ways to Read

**Path A — Conceptual Learner (Managers, Students, Career Switchers)**
- Read "What is it?", "Why learn this?", and "Core Concepts"
- Skim "How It Works" if curious
- Read "Where You See It" to anchor concepts to real products
- Run the simulations to observe behavior

**Path B — Hands-On Learner (Engineers, Developers)**
- Read everything including "How It Works"
- Run the Python projects and modify the code
- Set up the Flask backend + React frontend
- Extend the simulations with new features

---

## Learning Path

| # | Topic | What You Will Understand |
|---|-------|-------------------------|
| 1 | **Introduction to IAM** | The full identity lifecycle and core vocabulary |
| 2 | **Authentication Methods** | How systems prove who you are |
| 3 | **Multi-Factor Authentication** | Why passwords alone fail and how MFA fixes it |
| 4 | **Authorization Models** | How systems decide what you can do |
| 5 | **Role-Based Access Control** | Using roles to manage access at scale |
| 6 | **Attribute-Based Access Control** | Dynamic, context-aware permissions |
| 7 | **Privileged Access Management** | Protecting admin and root accounts |
| 8 | **Single Sign-On & Federation** | Logging in once across many systems |
| 9 | **OAuth 2.0 & OpenID Connect** | How apps access your data without your password |
| 10 | **SAML & Enterprise Federation** | How big companies share identities |
| 11 | **Identity Providers & Directories** | The databases that store who everyone is |
| 12 | **Identity Governance** | Keeping access clean, compliant, and audited |
| 13 | **Zero Trust Architecture** | The "never trust, always verify" security model |
| 14 | **Cloud IAM** | How AWS, Azure, and GCP handle identity |
| 15 | **Future of IAM** | Passwordless, AI-driven, and decentralized identity |

---

## Repository Structure

```
Identity-Access-Management/
├── 1. Introduction to IAM/
│   ├── README.md              # Theory + learning guidance
│   └── projects/              # Hands-on Python code
├── 2. Authentication Methods/
│   ├── README.md
│   └── projects/
├── ... (all 15 topics)
├── backend/                   # Flask API (optional)
├── frontend/                  # React app (optional)
└── database/                  # MySQL schema (optional)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Simulations | Python 3.13 (no external dependencies for most) |
| Backend API | Flask 3.0 + PyMySQL |
| Frontend | React 18 + Vite + Bootstrap 5 |
| Database | MySQL 9.0 |

---

## Quick Start

### Read Only (No Setup)
Open any `README.md` and start reading. No installation needed.

### Run Simulations
```bash
# Any individual simulation
python "1. Introduction to IAM/projects/identity_lifecycle_sim.py"
python "3. Multi-Factor Authentication/projects/totp_generator.py"
```

### Full Application
```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## Contributing

This is an open learning resource. Improvements welcome:
- Clearer explanations
- Better real-world examples
- Additional simulations
- Translations

## License

MIT — Free for educational and commercial use.
