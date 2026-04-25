# 🔐 Identity and Access Management (IAM) — Complete Learning Platform

> **From Zero to IAM Hero** — A beginner-friendly, hands-on journey through Identity and Access Management. No prior cybersecurity knowledge required.

---

## 🎯 Who Is This For?

- **Students** studying cybersecurity, IT, or computer science
- **Career switchers** moving into tech or security roles
- **Non-technical professionals** (managers, auditors, compliance officers) who need to *understand* IAM without writing code
- **Developers** who want to build secure applications

> 💡 **You don't need to be a programmer.** Every concept is explained with real-world analogies first, then technical details.

---

## 🏠 The Big Picture: IAM Is Like a Hotel

Imagine a luxury hotel:

| Hotel Activity | IAM Equivalent |
|----------------|---------------|
| 📝 Check-in desk verifies your passport | **Authentication** — proving who you are |
| 🏷️ Room key card with access levels | **Authorization** — what you're allowed to do |
| 🎥 Security cameras in hallways | **Audit/Accounting** — tracking what happened |
| 🚪 Master keys for staff | **Privileged Access** — elevated permissions |
| 🔑 Safe deposit box needing two keys | **Multi-Factor Authentication (MFA)** |
| 📋 Guest list shared with partner hotels | **Federation / Single Sign-On (SSO)** |
| 🧹 Housekeeping only enters during work hours | **Attribute-Based Access Control (ABAC)** |

**IAM is simply the digital version of this hotel security system.**

---

## 📚 What You'll Learn (15 Topics)

| # | Topic | One-Line Summary |
|---|-------|-----------------|
| 1 | **Introduction to IAM** | The foundations: who are you and what can you do? |
| 2 | **Authentication Methods** | Passwords, biometrics, and proving your identity |
| 3 | **Multi-Factor Authentication** | Why one lock isn't enough |
| 4 | **Authorization Models** | The rules that decide "yes" or "no" |
| 5 | **Role-Based Access Control (RBAC)** | Using job titles to control access |
| 6 | **Attribute-Based Access Control (ABAC)** | Smart, dynamic access decisions |
| 7 | **Privileged Access Management (PAM)** | Protecting the "master keys" |
| 8 | **Single Sign-On & Federation** | One key for many doors |
| 9 | **OAuth 2.0 & OpenID Connect** | Securely letting apps access your data |
| 10 | **SAML & Enterprise Federation** | Big-company identity sharing |
| 11 | **Identity Providers & Directory Services** | The phonebook of the digital world |
| 12 | **Identity Governance & Administration** | Keeping everything compliant and clean |
| 13 | **Zero Trust Architecture** | Never trust, always verify |
| 14 | **Cloud IAM** | Identity in AWS, Azure, and Google Cloud |
| 15 | **Future of IAM** | AI, decentralized identity, and what's next |

---

## 🏗️ Repository Structure

```
Identity-Access-Management/
├── 1. Introduction to IAM/           ← Start here!
│   ├── README.md                     ← Theory + analogies
│   └── projects/                     ← Hands-on Python demos
├── 2. Authentication Methods/
│   ├── README.md
│   └── projects/
├── ... (all 15 topics follow same pattern)
├── backend/                          ← Flask REST API (for developers)
├── frontend/                         ← React web app (for developers)
└── database/                         ← MySQL schema
```

> 🎓 **Non-technical learners:** Focus on the `README.md` files. The analogies and explanations are written for you.
> 
> 💻 **Technical learners:** Run the Python projects in each `projects/` folder and explore the full-stack app.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.13, Flask 3.0 | REST API server |
| **Frontend** | React 18, Vite 5, Bootstrap 5 | Interactive web interface |
| **Database** | MySQL 9.0 | Storing users, roles, and audit logs |
| **Simulations** | Python CLI scripts | Standalone learning demos |

---

## 🚀 Quick Start

### For Non-Technical Learners (Just Reading)
Simply open any `README.md` file and start reading! No setup required.

### For Technical Learners (Running Code)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
# API runs on http://localhost:5000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# App runs on http://localhost:5173
```

**Database:**
```bash
mysql -u root -p < database/schema.sql
```

---

## 🎮 Interactive Simulations

Each topic includes runnable Python simulations:

| Topic | Simulation | What It Does |
|-------|-----------|--------------|
| 1 | `identity_lifecycle_sim.py` | Simulates hiring → working → leaving |
| 2 | `password_hash_demo.py` | Shows how passwords are securely stored |
| 3 | `totp_generator.py` | Generates Google Authenticator-style codes |
| 4 | `access_matrix_visualizer.py` | Visualizes who can access what |
| 5 | `rbac_engine.py` | Full role-based access control system |
| 6 | `abac_policy_evaluator.py` | Dynamic policy decisions |
| 7 | `pam_vault_sim.py` | Privileged credential vault |
| 8 | `sso_token_flow.py` | Simulates single sign-on |
| 9 | `oauth_flow_sim.py` | OAuth 2.0 login flow |
| 10 | `saml_assertion_gen.py` | Creates SAML assertions |
| 11 | `ldap_simulator.py` | Directory service queries |
| 12 | `access_review_sim.py` | Compliance access reviews |
| 13 | `zero_trust_engine.py` | Continuous trust verification |
| 14 | `cloud_policy_sim.py` | AWS IAM policy evaluator |
| 15 | `decentralized_id_demo.py` | Self-sovereign identity demo |

**Run any simulation:**
```bash
python "1. Introduction to IAM/projects/identity_lifecycle_sim.py"
```

---

## 🧠 How to Use This Repository

### Learning Path 1: The Manager (Non-Technical)
1. Read the **Real-World Analogy** in each README
2. Skim the **Key Concepts** tables
3. Read the **Under the Hood** sections only if curious
4. Try the quiz questions at the end

### Learning Path 2: The Analyst (Somewhat Technical)
1. Read everything in the README
2. Run the Python simulations and observe the output
3. Try modifying the simulation parameters

### Learning Path 3: The Engineer (Technical)
1. Complete all READMEs and simulations
2. Set up the full-stack application (backend + frontend + database)
3. Extend the simulations with new features
4. Contribute improvements!

---

## 🤝 Contributing

This is an open educational project. Contributions welcome:
- Better analogies or explanations
- New simulations or examples
- Translations to other languages
- Bug fixes and improvements

---

## 📜 License

MIT License — Free for educational and commercial use.

---

**Built with 💙 for learners everywhere.**
