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

## Common COTS IAM Products in Industry

Organizations rarely build IAM from scratch. They buy **Commercial Off-The-Shelf (COTS)** products and configure them. Here are the products you will actually work with:

| IAM Function | Leading COTS Products | What They Do |
|-------------|----------------------|-------------|
| **Identity Provider (IdP)** | Okta, Azure AD, Ping Identity, ForgeRock, Auth0 | Authenticate users; issue tokens; manage profiles |
| **Directory Services** | Active Directory, Azure AD, OpenLDAP, FreeIPA | Store and organize identity data |
| **Single Sign-On (SSO)** | Okta, Azure AD, PingFederate, IBM Security Verify | One-login access to multiple applications |
| **Multi-Factor Authentication** | Duo, Microsoft Authenticator, RSA SecurID, YubiKey | Second-factor verification |
| **Privileged Access Management** | CyberArk, Delinea (Thycotic), BeyondTrust, HashiCorp Vault | Vault credentials; control admin access |
| **Identity Governance** | SailPoint, Saviynt, Oracle Identity Governance | Access reviews; certifications; SoD |
| **Customer Identity (CIAM)** | Auth0, Okta Customer Identity, PingOne, Amazon Cognito | Customer registration, login, preferences |
| **Cloud IAM** | AWS IAM, Azure RBAC, Google Cloud IAM | Control access to cloud resources |
| **Password Management** | 1Password Business, LastPass Enterprise, Bitwarden | Team password storage and sharing |

**Trend:** Major vendors are becoming suites. Okta now covers IdP + SSO + MFA + Governance. Microsoft offers Azure AD + PIM + Conditional Access + Entitlement Management. Organizations increasingly buy suites rather than best-of-breed point solutions.

---

## IAM Career Roles, Responsibilities, and Implementation Reality

Identity and Access Management offers multiple career paths. Understanding the differences — and how IAM actually works in industry — helps you target your skill development effectively.

### The IAM Industry Reality: Buy, Don't Build

**Critical insight for career planning:** 90%+ of organizations do **not** build IAM systems from scratch. They purchase Commercial Off-The-Shelf (COTS) products and hire people to **support**, **implement**, or **integrate** them.

| Approach | What It Means | Examples | Who Does It |
|----------|--------------|----------|-------------|
| **COTS Products** | Buy existing IAM software; configure and deploy | Okta, Azure AD, SailPoint, CyberArk, Ping Identity | **Implementation Engineers** |
| **Support & Operations** | Operate and troubleshoot deployed COTS products | Daily admin of Okta, AD, PAM tools | **Support Engineers** |
| **Custom Development** | Build connectors, workflows, or CIAM features | Custom provisioning scripts, API integrations, login portals | **IAM Developers** |
| **Architecture & Strategy** | Design enterprise-wide IAM roadmap, select products | Multi-year IAM strategy, vendor evaluation | **Consultants / Architects** |

**Why this matters for your career:**
- If you want to work in IAM, you need product expertise (Okta, Azure AD, SailPoint) more than theoretical knowledge
- Support roles are the most common entry point — every company with IAM needs support
- Implementation roles require deep product knowledge plus project skills
- Development roles are rarer and require strong coding skills — but pay well
- Most organizations use a **hybrid**: COTS for core IAM, custom code for integrations

---

### 1. IAM Support Engineer (Operating Existing Solutions)

**What they do:** Operate and troubleshoot IAM systems that are already deployed. The product exists; their job is to keep it running.

**Typical daily work:**
- Reset passwords, unlock accounts, resolve MFA issues
- Troubleshoot SSO failures ("Why can't I access Salesforce?")
- Investigate failed authentication attempts in logs
- Handle access requests and provisioning tickets
- Respond to alerts from the IAM system
- Escalate complex issues to vendors or senior engineers

**Products they work with:**
- **Identity Providers:** Okta, Azure AD, Ping Identity, OneLogin
- **Directories:** Active Directory, LDAP, Azure AD Connect
- **PAM tools:** CyberArk, BeyondTrust, Delinea
- **IGA platforms:** SailPoint, Saviynt, Microsoft Entitlement Management

| Level | Responsibilities | Skills Needed |
|-------|-----------------|---------------|
| **L1 (Junior)** | Password resets, account unlocks, basic provisioning, ticket triage | AD basics, ticketing systems, customer service, basic PowerShell |
| **L2 (Mid)** | Complex provisioning, SSO troubleshooting, MFA problems, group policy issues | LDAP, PowerShell, SAML/OIDC basics, log analysis, networking |
| **L3 (Senior)** | Escalation handling, incident response, root cause analysis, vendor coordination | Deep AD/Azure AD, PAM tools, federation debugging, automation scripting |

**Key awareness:**
- You work within the product's limitations; you cannot redesign it
- Vendor documentation and support tickets are your primary tools
- Most problems have happened before — knowledge bases are valuable
- Communication skills are essential — you talk to frustrated users daily

---

### 2. IAM Implementation Engineer (Deploying and Configuring Solutions)

**What they do:** Deploy new IAM solutions or reconfigure existing ones. They take COTS products and make them work for the organization's specific requirements.

**Typical projects:**
- Deploy Okta or Azure AD for workforce SSO
- Implement SailPoint for access governance and certification
- Configure CyberArk for privileged access management
- Integrate a new SaaS application with corporate SSO
- Migrate from one IdP to another (e.g., AD FS to Azure AD)
- Design and deploy MFA across all users

**What they work with:**
- Same products as Support, but they **configure** them rather than operate them
- Requirements documents, design documents, test plans
- APIs, SCIM connectors, SAML/OIDC configuration
- Multiple stakeholders: Security, IT, application owners, business users

| Level | Responsibilities | Skills Needed |
|-------|-----------------|---------------|
| **Junior** | Configure simple integrations, follow runbooks, assist senior engineers | Product basics, SAML/OIDC concepts, basic scripting |
| **Implementation Engineer** | Lead medium projects, design integrations, troubleshoot complex configurations | Deep product expertise, SAML/OIDC/OAuth, directory services, API integration, project management |
| **Senior / Architect** | Design enterprise-wide IAM architecture, lead multi-product deployments, evaluate vendors | Multi-product expertise, security architecture, stakeholder management, vendor evaluation |

**Key awareness:**
- Requirements gathering is half the job — you cannot implement what you do not understand
- Legacy systems are the hardest part — modern apps support SAML/OIDC; old ones do not
- Rollback plans are essential — if go-live fails, you must restore service quickly
- Testing is critical — test every user type, every application, every edge case
- Documentation is your legacy — the Support team will live with what you build

---

### 3. IAM Developer (Building Custom Solutions and Integrations)

**What they do:** Write code to build custom IAM functionality, integrate systems without out-of-the-box connectors, and extend COTS products through APIs.

**Typical work:**
- Build custom provisioning connectors for legacy applications
- Develop CIAM features — user registration, login, profile management
- Write authentication middleware for custom applications
- Build automated access review and certification tools
- Integrate IAM systems with SIEM, ITSM, or HR systems
- Develop custom reporting and analytics dashboards

**What they work with:**
- **Languages:** Python, Java, JavaScript/TypeScript, C#, Go
- **Protocols:** OAuth 2.0, OIDC, SAML, SCIM, LDAP
- **APIs:** REST, GraphQL, product-specific SDKs
- **Databases:** SQL and NoSQL for identity stores

| Level | Responsibilities | Skills Needed |
|-------|-----------------|---------------|
| **Junior** | Write scripts and small features, fix bugs, maintain existing code | Python/PowerShell, REST APIs, basic SAML/OIDC, SQL |
| **Developer** | Build connectors and integrations, implement authentication flows, develop features | OAuth 2.0, OIDC, JWT, SCIM, SDK development, cloud IAM APIs, secure coding |
| **Senior / Principal** | Design architecture, build core IAM services, lead technical decisions | System design, microservices, cryptography, security architecture, mentoring |

**Key awareness:**
- Do not build what you can buy — custom IAM components are expensive to maintain
- When you must build, follow standards (OAuth 2.0, OIDC, SCIM) rather than inventing protocols
- Security review is mandatory — authentication code must be reviewed by security experts
- You are building the keys to the kingdom — take that responsibility seriously
- Development roles are rarer than Support or Implementation, but typically higher-paying

---

### 4. IAM Analyst (Governance and Compliance)

**What they do:** Design policies, analyze access patterns, conduct audits, and ensure compliance.

| Level | Responsibilities | Skills Needed |
|-------|-----------------|---------------|
| **Junior** | Run access reports, assist with access reviews, document policies, support audit requests | Excel, basic SQL, IAM concepts, documentation |
| **Mid** | Design access policies, conduct access certifications, analyze role structures, recommend SoD improvements | RBAC/ABAC design, IGA tools (SailPoint, Okta), compliance frameworks (SOX, HIPAA) |
| **Senior** | Lead access governance programs, design IGA strategy, manage audit responses, optimize role models | Risk management, audit methodology, GRC platforms, business analysis, stakeholder management |

**Day-to-day:** Review access requests, design roles and policies, run certification campaigns, analyze access data, prepare audit evidence, recommend improvements.

---

### 5. IAM Consultant / Architect (Strategy and Design)

**What they do:** Design enterprise IAM strategies, lead implementations, and advise organizations.

| Level | Responsibilities | Skills Needed |
|-------|-----------------|---------------|
| **Consultant** | Implement IAM solutions for clients, configure IdP/IGA products, train client teams | Multiple IAM products, project implementation, client communication |
| **Senior Consultant** | Lead implementation projects, design architectures, manage client relationships, mentor juniors | Architecture design, cross-product expertise, stakeholder management |
| **Architect** | Define enterprise IAM strategy, design multi-year roadmaps, evaluate emerging technologies, set standards | Enterprise architecture, security strategy, vendor evaluation, C-level communication |

**Day-to-day:** Meet with clients, assess current state, design target architectures, lead implementation teams, present to executives, write proposals.

---

### Career Track Comparison

| Aspect | Support | Implementation | Development | Analyst | Consultant |
|--------|---------|---------------|-------------|---------|------------|
| **Primary focus** | Fix issues | Deploy solutions | Build solutions | Govern access | Design strategy |
| **Code involvement** | Scripts | Scripts / Config | Full development | SQL / Scripts | Minimal |
| **Product interaction** | Operate existing | Configure and deploy | Extend via APIs | Report on | Select and design |
| **User interaction** | End users | Project stakeholders | Other developers | Managers/auditors | Executives |
| **Key deliverable** | Resolved tickets | Working environment | Working code | Compliance reports | Architecture docs |
| **Most common role?** | Yes — every org needs support | Yes — during projects | No — rarer | Medium | Medium |
| **Entry barrier** | Lower | Medium | Higher | Medium | Higher |

### Career Progression Paths

**Support Track:**
```
L1 Support → L2 Support → L3 Support → Team Lead → IAM Manager
```

**Implementation Track:**
```
Junior Implementation → Implementation Engineer → Senior Implementation → IAM Architect
```

**Development Track:**
```
Junior Developer → IAM Developer → Senior Developer → Principal Engineer → IAM Architect
```

**Crossover is common and valuable:**
- **Support → Implementation:** Deep product knowledge + understanding of failure modes
- **Implementation → Development:** Knowing what integrations are painful helps build better solutions
- **Development → Support/Implementation:** Code-level understanding enables faster debugging
- **Any track → Consultant/Architect:** Combining multiple perspectives makes you a better strategist

### Certifications by Track

| Track | Relevant Certifications |
|-------|------------------------|
| **Support** | Microsoft AZ-500, AWS Security Specialty, CompTIA Security+, product-specific certs (Okta Certified Admin) |
| **Implementation** | Okta Certified Professional, SailPoint IdentityNow Engineer, Azure Identity & Access Administrator, Ping Identity Certified Professional |
| **Development** | Relevant cloud certs (AWS/Azure/GCP developer), security coding certifications, OAuth/OIDC knowledge |
| **Analyst** | CISA, CRISC, CISSP, product-specific governance certs |
| **Consultant/Architect** | CISSP, CISM, SABSA, TOGAF, vendor solution architect certs |

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
