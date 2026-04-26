# Identity and Access Management (IAM) Learning Platform

A comprehensive, interactive learning platform covering the full spectrum of Identity and Access Management — from foundational concepts to cutting-edge authentication technologies. Each module combines deep theoretical explanations with hands-on Python simulations and an interactive React frontend.

---

## What You Will Learn

This platform covers 15 IAM topics in depth:

| # | Module | Focus |
|---|--------|-------|
| 1 | **Introduction to IAM** | Core concepts, identity lifecycle, CIA triad, least privilege |
| 2 | **Authentication Methods** | Passwords, biometrics, FIDO2, risk-based auth, attack mitigation |
| 3 | **Multi-Factor Authentication** | TOTP, HOTP, push notifications, MFA bypass prevention |
| 4 | **Authorization Models** | ACL, RBAC, ABAC, MAC, DAC — how each model makes decisions |
| 5 | **Role-Based Access Control** | Role hierarchies, RBAC levels, role engineering, separation of duties |
| 6 | **Attribute-Based Access Control** | Policy evaluation, XACML, dynamic authorization, ABAC vs RBAC |
| 7 | **Privileged Access Management** | Credential vaults, JIT access, session recording, password rotation |
| 8 | **Single Sign-On and Federation** | SAML, OIDC, trust relationships, token flows |
| 9 | **OAuth 2.0 and OpenID Connect** | Authorization flows, scopes, JWTs, refresh tokens, PKCE |
| 10 | **SAML and Enterprise Federation** | Assertions, bindings, metadata, SP-initiated vs IdP-initiated |
| 11 | **Identity Providers and Directory Services** | Active Directory, LDAP, Kerberos, hybrid identity |
| 12 | **Identity Governance and Administration** | Access certification, SoD, role mining, lifecycle management |
| 13 | **Zero Trust Architecture** | Verify explicitly, least privilege, micro-segmentation, ZTNA |
| 14 | **Cloud IAM** | AWS, Azure, GCP IAM models, policies, cross-account access |
| 15 | **Future of IAM** | Passwordless, decentralized identity, AI-driven security, behavioral biometrics |

---

## IAM Career Roles & Responsibilities

Identity and Access Management offers multiple career paths. Understanding the differences helps you target your skill development.

### IAM Support Engineer

**What they do:** Troubleshoot and resolve day-to-day IAM issues.

| Level | Responsibilities | Typical Skills |
|-------|-----------------|---------------|
| **L1 (Junior)** | Password resets, account unlocks, basic user provisioning, ticket triage | Active Directory basics, ticketing systems, customer service |
| **L2 (Mid)** | Complex provisioning issues, group policy troubleshooting, MFA problems, access request fulfillment | LDAP, PowerShell, SAML/OIDC basics, SSO troubleshooting |
| **L3 (Senior)** | Escalation handling, incident response, root cause analysis, knowledge base creation, vendor coordination | Deep AD/Azure AD, PAM tools, federation debugging, scripting |

**Day-to-day:** Respond to tickets, troubleshoot login issues, provision/deprovision accounts, resolve MFA lockouts, document solutions.

### IAM Developer / Engineer

**What they do:** Build and integrate IAM systems, develop automation, and implement identity solutions.

| Level | Responsibilities | Typical Skills |
|-------|-----------------|---------------|
| **Junior** | Write scripts for user provisioning, maintain automation workflows, fix bugs in IAM integrations | Python/PowerShell, REST APIs, basic SAML/OIDC, SQL |
| **Mid** | Develop custom connectors, build CIAM features, implement MFA solutions, integrate applications with IdP | OAuth 2.0, OIDC, JWT, SCIM, SDK development, cloud IAM APIs |
| **Senior** | Architect IAM solutions, design custom IdP features, lead integration projects, evaluate technologies | System design, microservices, cryptography, security architecture |

**Day-to-day:** Write code for IAM integrations, build provisioning connectors, develop authentication flows, automate identity processes, maintain IAM infrastructure.

### IAM Analyst

**What they do:** Design policies, analyze access patterns, conduct audits, and ensure compliance.

| Level | Responsibilities | Typical Skills |
|-------|-----------------|---------------|
| **Junior** | Run access reports, assist with access reviews, document policies, support audit requests | Excel, basic SQL, IAM concepts, documentation |
| **Mid** | Design access policies, conduct access certifications, analyze role structures, recommend SoD improvements | RBAC/ABAC design, IGA tools (SailPoint, Okta), compliance frameworks |
| **Senior** | Lead access governance programs, design IGA strategy, manage audit responses, optimize role models | Risk management, audit methodology, GRC platforms, business analysis |

**Day-to-day:** Review access requests, design roles and policies, run certification campaigns, analyze access data, prepare audit evidence, recommend improvements.

### IAM Consultant / Architect

**What they do:** Design enterprise IAM strategies, lead implementations, and advise organizations.

| Level | Responsibilities | Typical Skills |
|-------|-----------------|---------------|
| **Consultant** | Implement IAM solutions for clients, configure IdP/IGA products, train client teams | Multiple IAM products, project implementation, client communication |
| **Senior Consultant** | Lead implementation projects, design architectures, manage client relationships, mentor juniors | Architecture design, cross-product expertise, stakeholder management |
| **Architect** | Define enterprise IAM strategy, design multi-year roadmaps, evaluate emerging technologies, set standards | Enterprise architecture, security strategy, vendor evaluation, C-level communication |

**Day-to-day:** Meet with clients, assess current state, design target architectures, lead implementation teams, present to executives, write proposals.

### Role Comparison

| Aspect | Support | Developer | Analyst | Consultant |
|--------|---------|-----------|---------|------------|
| **Primary focus** | Fix issues | Build solutions | Govern access | Design strategy |
| **Coding required** | Scripting | Heavy | Light (SQL/scripts) | Minimal |
| **Business interaction** | End users | Product teams | Managers/auditors | Executives |
| **Key deliverable** | Resolved tickets | Working integrations | Compliance reports | Architecture documents |
| **Career progression** | L3 → Team Lead | Senior → Staff/Principal | Senior → Manager | Senior → Architect → Director |

### Career Progression Paths

**Technical Track (Individual Contributor):**
```
Junior Support → L2 Support → L3 Support → IAM Engineer → Senior Engineer → Principal Engineer → IAM Architect
```

**Management Track:**
```
Analyst → Senior Analyst → IAM Manager → IAM Director → CISO / VP Identity
```

**Consulting Track:**
```
Consultant → Senior Consultant → Lead Consultant → Practice Lead → Partner / VP Consulting
```

**Crossover is common:** Many IAM Architects started in Support or Development. Understanding how systems work technically is invaluable for designing governance policies or consulting on implementations.

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.13, Flask 3.0 | REST API serving content and simulations |
| **Frontend** | React 18, Vite 5, Bootstrap 5 | Interactive learning interface |
| **Database** | MySQL 9.0 | User progress, quiz results |
| **Authentication** | PyJWT | JWT token handling |
| **Communication** | PyMySQL, Axios | Database and API connectivity |

---

## Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- MySQL 9.0+

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Database
```bash
mysql -u root -p < database/schema.sql
```

---

## How to Use This Platform

1. **Read the module README** — Each topic has a comprehensive guide with:
   - What the concept is and why it matters
   - Core concepts explained thoroughly
   - How it works under the hood
   - Real-world products and implementations
   - Common misconceptions to avoid
   - Hands-on exercises
   - Quiz questions to check understanding

2. **Run the simulations** — Every module includes Python scripts you can run:
   - CLI mode: `python projects/[simulation].py`
   - Web mode: Launch the Flask backend and React frontend, navigate to the module, and run simulations through the web interface

3. **Test your knowledge** — Each README includes Check Your Understanding questions. Use these to verify you've mastered the material.

---

## Repository Structure

```
Identity-Access-Management/
├── 1. Introduction to IAM/
│   ├── README.md          ← Comprehensive module guide
│   └── projects/           ← Python simulations
├── 2. Authentication Methods/
│   ├── README.md
│   └── projects/
├── ... (modules 3-15 follow same pattern)
├── backend/
│   ├── app.py              ← Flask REST API
│   ├── routes/
│   └── utils/
├── frontend/
│   └── src/                ← React application
├── database/
│   └── schema.sql          ← MySQL schema
└── README.md               ← This file
```

---

## Learning Approach

Each module is designed for deep understanding:

1. **Theory first** — Comprehensive explanations that answer "what is this?" and "why does it work?"
2. **How it works** — Technical details, flows, and architectures
3. **Real products** — Where you see these concepts in the industry
4. **Misconceptions** — Common errors and misunderstandings to avoid
5. **Practice** — Hands-on exercises you can do immediately
6. **Projects** — Runnable Python simulations
7. **Assessment** — Questions that test genuine understanding, not memorization

This structure ensures you can explain concepts to others, troubleshoot real issues, and make informed architecture decisions.

---

## Contributing

This is a living educational resource. Improvements, additional simulations, and corrections are welcome.
