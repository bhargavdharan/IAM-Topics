# 1. Introduction to Identity and Access Management (IAM)

## What Is IAM?

**Identity and Access Management (IAM)** is the framework of policies, processes, and technologies that ensures the right individuals have the right access to the right resources at the right time — and for the right reasons.

At its core, IAM answers three fundamental questions:
1. **Who are you?** → Identity
2. **How do I know it's really you?** → Authentication
3. **What are you allowed to do?** → Authorization

Every time you log into an application, swipe an access badge, or use facial recognition to unlock your phone, you are interacting with an IAM system. IAM is the invisible security layer that protects organizations from unauthorized access while enabling legitimate users to do their work.

---

## Why Learn IAM?

Identity-related breaches are among the most common and damaging cybersecurity incidents:
- **81% of hacking-related breaches** involve stolen or weak credentials (Verizon DBIR)
- **Identity is the new perimeter** — cloud and remote work have dissolved traditional network boundaries
- **Compliance requirements** (SOX, HIPAA, PCI-DSS, GDPR) mandate strong identity controls
- **Insider threats** — both malicious and accidental — are managed through IAM

IAM skills are foundational for cybersecurity, system administration, cloud architecture, and compliance roles. Understanding IAM enables you to design secure systems, troubleshoot access issues, and protect organizational assets.

---

## Core Concepts

### Identity

An **identity** is a digital representation of a user, device, application, or system. Every entity that needs to interact with resources must have an identity.

**Types of identities:**

| Identity Type | Description | Example |
|--------------|-------------|---------|
| **Human Identity** | Individual person | Employee Alice, contractor Bob, customer Carol |
| **Machine Identity** | Non-human entity | Server, IoT device, container, virtual machine |
| **Service Account** | Application identity | Database service account, backup agent, API consumer |
| **Privileged Identity** | Account with elevated permissions | Domain administrator, root user, cloud owner |

**Identity Attributes:**
Identities carry attributes that describe them:
- **Unique Identifier:** Username, email, employee ID, UUID
- **Personal Information:** Name, department, job title, location
- **Organizational Attributes:** Manager, cost center, business unit
- **Security Attributes:** Group memberships, roles, clearance level
- **Lifecycle State:** Active, suspended, terminated, on-leave

These attributes are used to make access decisions — not just "who is Alice?" but "what department is Alice in?", "who is her manager?", "is her account active?"

### Authentication vs Authorization

These two concepts are foundational to IAM and are frequently confused. Understanding the difference is critical.

**Authentication (AuthN): Proving WHO you are**

Authentication is the process of verifying that a claimed identity is genuine. It answers: **"Are you really who you say you are?"**

Authentication mechanisms use **factors** — categories of evidence:

| Factor Category | What It Is | Examples |
|----------------|-----------|----------|
| **Something you KNOW** | Information only the user should know | Password, PIN, security question answer |
| **Something you HAVE** | Physical object in the user's possession | Smartphone, smart card, hardware token, YubiKey |
| **Something you ARE** | Biological characteristic | Fingerprint, face, iris, voice, palm print |
| **Something you DO** | Behavioral pattern | Typing rhythm, mouse movements, gait |
| **Somewhere you ARE** | Geographic location | GPS coordinates, IP address range |

**Single-factor authentication** uses one factor (typically password). **Multi-factor authentication (MFA)** uses two or more factors from different categories. MFA is significantly stronger because compromising one factor does not grant access.

**Authentication establishes trust:** After successful authentication, the system creates a **session** — a temporary trusted state that remembers the user is authenticated without requiring credentials for every action.

---

**Authorization (AuthZ): Determining WHAT you can do**

Authorization is the process of determining what actions an authenticated identity is permitted to perform. It answers: **"Now that I know who you are, what are you allowed to do?"**

Authorization happens **AFTER** authentication. You cannot authorize someone if you do not know who they are.

**Authorization decisions consider:**
- **Identity:** Who is requesting access?
- **Resource:** What are they trying to access?
- **Action:** What are they trying to do? (read, write, delete, execute)
- **Context:** When, where, and how is the request made?
- **Policy:** What rules govern this access?

**Example of the distinction:**

| Scenario | Authentication | Authorization |
|----------|---------------|---------------|
| Alice enters her password to log in | ✓ Verifies Alice's identity | — |
| Alice tries to view a document | — | ✓ Checks if Alice has read permission |
| Alice tries to delete a document | — | ✓ Checks if Alice has delete permission (denied) |
| Alice's manager tries to view the same document | ✓ Verifies manager's identity | ✓ Checks manager's permissions (granted) |

**Key insight:** Authentication is about identity verification. Authorization is about permission enforcement. Both are required for secure access.

### The Principle of Least Privilege (PoLP)

**The Principle of Least Privilege** is the foundational security principle that states: **every user, application, and system should have ONLY the minimum permissions necessary to perform their legitimate functions — and no more.**

**Why Least Privilege matters:**
- **Breach containment:** If an account is compromised, the damage is limited to what that account can access
- **Insider threat reduction:** Employees cannot accidentally or maliciously access data outside their role
- **Operational stability:** Restricted permissions prevent accidental configuration changes
- **Compliance:** Most regulatory frameworks require least privilege
- **Audit simplicity:** Fewer permissions mean simpler audits and clearer accountability

**What Least Privilege looks like in practice:**

| Role | What they NEED | What they should NOT have |
|------|---------------|--------------------------|
| **Marketing Employee** | Read marketing materials, write to shared drive | Access to financial systems, HR records, production servers |
| **Database Administrator** | Manage database instances, backups, user accounts | Domain admin rights, access to source code, ability to approve invoices |
| **Software Developer** | Read/write source code, deploy to staging | Production database access, ability to modify payroll, approve vendor payments |
| **Finance Analyst** | Read financial reports, run analysis queries | Ability to modify transactions, access customer PII, modify system configurations |
| **Help Desk L1** | Reset passwords, unlock accounts, view user info | Ability to create admin accounts, modify group memberships, access executive data |

**Implementing Least Privilege:**

1. **Start with zero access:** New users start with no permissions
2. **Grant only what is needed:** Add permissions based on job function
3. **Use roles, not individual permissions:** Define standard roles (e.g., "Marketing User", "DBA") with appropriate permissions
4. **Regular review:** Periodically audit permissions and remove unnecessary access
5. **Temporary elevation:** Use just-in-time access for rare elevated tasks
6. **Monitor and alert:** Flag unusual access patterns that suggest over-permission

**What happens WITHOUT Least Privilege:**

Consider a company where all employees have local administrator rights on their laptops:
- A marketing employee accidentally installs malware that encrypts all files
- Because they have admin rights, the malware can:
  - Disable antivirus
  - Install keyloggers
  - Access all files on the machine (including cached credentials)
  - Spread to network shares
  - Modify system configurations

With least privilege (standard user rights):
- The malware cannot install system-wide
- Cannot disable security tools
- Cannot access protected system areas
- Damage is contained to the user's own files

**Least Privilege is not just for users:**
- **Applications:** A web application should only have database read permissions for the tables it needs
- **Services:** A backup service should only have backup permissions, not delete permissions
- **APIs:** An API key should only have access to the specific endpoints required
- **Containers:** Containers should run with minimal capabilities and file system access

### Separation of Duties (SoD)

**Separation of Duties** is the principle that no single individual should have complete control over a critical process. Responsibilities are divided among multiple people to prevent fraud, errors, and abuse.

**Why SoD matters:**
- **Fraud prevention:** One person cannot both create a fake vendor AND pay that vendor
- **Error detection:** One person enters data, another verifies it
- **Insider threat mitigation:** No single person can cause catastrophic damage alone
- **Compliance:** SOX, PCI-DSS, and many frameworks require SoD

**How SoD works:**

A critical business process is broken into distinct steps, and different people perform each step:

**Example: Purchasing Process**

| Step | Action | Role | Why Separation Matters |
|------|--------|------|----------------------|
| 1 | Create purchase requisition | Department Employee | Initiates the need |
| 2 | Approve requisition | Department Manager | Verifies the need is legitimate and within budget |
| 3 | Issue purchase order | Procurement Officer | Formalizes the purchase; separate from approval |
| 4 | Receive goods | Receiving Clerk | Confirms goods arrived; separate from ordering |
| 5 | Verify invoice | Accounts Payable Clerk | Confirms invoice matches PO and receipt |
| 6 | Process payment | Payment Authorizer | Releases funds; highest risk step |

**If one person could do steps 1, 2, 3, and 6:** They could create a fake vendor, approve their own purchase, and pay themselves.

**Example: Software Development**

| Step | Action | Role | Why Separation Matters |
|------|--------|------|----------------------|
| 1 | Write code | Developer | Creates functionality |
| 2 | Review code | Peer Developer | Catches bugs, security issues, backdoors |
| 3 | Approve merge | Tech Lead | Authorizes code into main branch |
| 4 | Deploy to production | DevOps Engineer | Separate from code authorship |
| 5 | Verify deployment | QA Engineer | Confirms deployment works correctly |

**If one person could write, review, approve, and deploy:** They could introduce malicious code with no oversight.

**SoD in IAM Systems:**

IAM systems enforce SoD technically:

| Conflict | Role A | Role B | Risk |
|----------|--------|--------|------|
| Create user + Approve user | User Administrator | User Approval Manager | Create backdoor accounts |
| Grant access + Audit access | Access Administrator | Security Auditor | Grant unauthorized access; hide evidence |
| Request privilege + Approve privilege | Standard User | Privilege Approver | Self-approve elevated access |
| Backup data + Delete data | Backup Operator | Data Administrator | Delete data; restore to cover tracks |

**SoD enforcement approaches:**
- **Preventive:** System physically prevents conflicting role assignment ("You cannot have both roles")
- **Detective:** System flags existing conflicts for review ("Alert: User has conflicting roles")
- **Compensating:** When technical SoD is impossible (small teams), manual reviews or supervisor oversight compensate

### Core IAM Components

IAM systems consist of integrated components working together:

| Component | Function | Real-World Analogy |
|-----------|----------|-------------------|
| **Identity Store (Directory)** | Central repository of all identities and attributes | The employee database with names, departments, roles |
| **Authentication Service** | Verifies identity through credentials | The security guard checking your badge and face |
| **Authorization Engine** | Determines permissions based on policies | The access control system deciding which doors your badge opens |
| **Policy Store** | Stores access rules and policies | The building's access rulebook |
| **Audit & Logging** | Records all access events for review | Security camera footage and access logs |
| **Provisioning Service** | Creates, modifies, and removes accounts | HR onboarding/offboarding process |

### The CIA Triad and IAM

IAM directly supports the three pillars of information security:

| CIA Pillar | IAM Contribution | Example |
|-----------|------------------|---------|
| **Confidentiality** | Ensures only authorized users access sensitive data | Restricting financial records to Finance team |
| **Integrity** | Prevents unauthorized modification of data | Allowing only DBAs to modify database schemas |
| **Availability** | Ensures legitimate users can access resources when needed | Quick provisioning for new hires; self-service password reset |

---

## User Lifecycle Management (ULM): Joiner, Mover, Leaver (JML)

**User Lifecycle Management (ULM)** is the standard industry framework for managing identities throughout their organizational existence. The JML model — **Joiner, Mover, Leaver** — describes the three primary lifecycle states.

This framework ensures that access is granted appropriately when people join, adjusted correctly when their role changes, and revoked completely when they leave.

### 1. JOINER (Onboarding)

**When:** A new person starts — employee, contractor, partner, intern, vendor.

**What must happen:**

| Step | Action | Why Critical |
|------|--------|-------------|
| **Identity Creation** | Create unique digital identity (username, email, employee ID) | Foundation for all subsequent access |
| **Attribute Assignment** | Assign department, manager, job title, location | Determines what access is needed |
| **Credential Provisioning** | Set initial password, issue MFA token, create certificates | Enables authentication |
| **Role Assignment** | Assign roles based on job function | Determines authorization |
| **Access Provisioning** | Grant access to applications, systems, files needed for the role | Enables productivity; must follow least privilege |
| **Notification** | Inform manager, IT team, security team | Ensures accountability and oversight |
| **Training Assignment** | Assign security awareness training, policy acknowledgments | Reduces human risk |

**Joiner risks if poorly managed:**
- Delayed access = employee cannot work
- Excessive access = violation of least privilege from day one
- Missing access = employee finds workarounds (shadow IT)
- Orphaned pre-provisioned accounts = security gap

### 2. MOVER (Transfer / Change)

**When:** A person's role, department, location, or responsibilities change — promotion, lateral move, department transfer, temporary assignment.

**What must happen:**

| Step | Action | Why Critical |
|------|--------|-------------|
| **Old Access Review** | Document current access rights | Baseline for changes |
| **Remove Old Access** | Revoke permissions from previous role | Prevents access creep |
| **Add New Access** | Grant permissions for new role | Enables new responsibilities |
| **Attribute Update** | Update department, manager, job title, location | Ensures accurate identity data |
| **Notify Stakeholders** | Inform old manager, new manager, security team | Maintains accountability |
| **Compliance Check** | Verify no SoD conflicts with new role combinations | Prevents policy violations |

**Mover risks if poorly managed:**
- **Access creep:** User accumulates permissions from multiple roles (old + new)
- **SoD violations:** New role combination creates a conflict
- **Missing access:** Cannot perform new job functions
- **Stale data:** Old department/manager attributes cause wrong routing

**Access Creep is the silent killer of IAM:**

Consider an employee's journey:
- Year 1: Hired as Marketing Coordinator → gets marketing folder access
- Year 2: Transferred to Sales → keeps marketing access + gets CRM access
- Year 3: Promoted to Sales Manager → keeps all prior access + gets approval rights
- Year 4: Temporary IT project → gets admin access (never revoked)

By year 5, this employee has access to Marketing, Sales, CRM, and IT systems. If their account is compromised, the attacker has broad access. If they become malicious, they can access data across departments.

**The solution:** Mover processes must systematically REMOVE old access while adding new access.

### 3. LEAVER (Offboarding)

**When:** A person leaves the organization — resignation, termination, retirement, contract end, leave of absence.

**What must happen:**

| Step | Action | Why Critical |
|------|--------|-------------|
| **Account Disablement** | Disable account immediately upon notification | Prevents further access |
| **Access Revocation** | Revoke all system, application, and resource access | Removes authorization |
| **Credential Invalidation** | Disable passwords, tokens, certificates, API keys | Prevents authentication |
| **Session Termination** | Kill all active sessions across all systems | Stops ongoing access |
| **Asset Recovery** | Collect company devices, badges, tokens | Physical security |
| **Data Transfer** | Transfer ownership of files, emails, documents | Business continuity |
| **Archive Identity** | Retain identity record with termination reason | Audit trail, compliance |
| **Notify Stakeholders** | Inform manager, IT, security, compliance | Coordinated response |

**Leaver risks if poorly managed:**
- **Orphaned accounts:** Account remains active after departure
- **Ghost access:** Former employee can still log in weeks or months later
- **Session persistence:** Active sessions continue after account disablement
- **Data exfiltration:** Departing employee copies data before leaving
- **Revenge actions:** Terminated employee damages systems or data

**Critical timing:** For involuntary terminations, disablement must happen **BEFORE** the employee is notified, to prevent retaliation.

### JML Automation

Modern IAM systems automate JML workflows:

**Joiner automation:**
```
HR System (new hire recorded)
    ↓
IAM System (identity created, attributes populated)
    ↓
Provisioning Engine (access granted based on role rules)
    ↓
Notification Sent (manager informed, user receives welcome email)
```

**Mover automation:**
```
HR System (transfer recorded)
    ↓
IAM System (attributes updated)
    ↓
Access Review (current access catalogued)
    ↓
Old Access Revoked + New Access Granted
    ↓
SoD Check (verify no policy violations)
```

**Leaver automation:**
```
HR System (termination recorded)
    ↓
IAM System (account disabled IMMEDIATELY)
    ↓
Provisioning Engine (all access revoked)
    ↓
Session Manager (all sessions terminated)
    ↓
Audit Log (complete record preserved)
```

---

## IAM in Practice: Support, Implementation, and Development

This section explains how IAM actually works in real organizations — because most companies do not build IAM systems from scratch. They buy them, configure them, and maintain them.

### The IAM Technology Landscape

Organizations acquire IAM capabilities in three ways:

| Approach | What It Means | Examples | When Used |
|----------|--------------|----------|-----------|
| **Commercial Off-The-Shelf (COTS)** | Buy an existing product; configure and deploy it | Okta, Azure AD, SailPoint, CyberArk, Ping Identity | Most common; fastest time to value |
| **Custom Development** | Build IAM functionality in-house | Custom login portal, bespoke provisioning scripts, internal auth service | Unique requirements; regulatory constraints; large tech companies |
| **Hybrid** | COTS for core IAM; custom for specialized needs | Okta for SSO + custom provisioning connector for legacy ERP | Most enterprise environments |

**Reality check:** 90%+ of organizations use COTS products for core IAM. Building an identity provider, credential vault, or governance platform from scratch requires enormous investment and carries significant security risk. Even Google, Microsoft, and Amazon use their own commercial identity services rather than building custom alternatives.

### Support vs Implementation vs Development

These are three distinct career tracks within IAM, and understanding the difference is critical for career planning.

---

#### 1. IAM Support (Operating Existing Solutions)

**What Support Engineers do:**
Support engineers operate and troubleshoot IAM systems that are already deployed. The solution exists; their job is to keep it running and help users.

**Typical daily work:**
- Reset passwords and unlock accounts
- Troubleshoot SSO login failures ("Why can't I access Salesforce?")
- Resolve MFA issues ("My phone broke; I need MFA reset")
- Investigate failed authentication attempts in logs
- Handle access requests and provisioning tickets
- Respond to alerts from the IAM system
- Escalate complex issues to vendors or senior engineers

**What they work with:**
- **Identity Providers:** Okta, Azure AD, Ping Identity, OneLogin
- **Directories:** Active Directory, LDAP, Azure AD Connect
- **PAM tools:** CyberArk, BeyondTrust, Delinea (formerly Thycotic)
- **IGA platforms:** SailPoint, Saviynt, Microsoft Entitlement Management
- **SSO portals:** Company intranet login pages, app launchers

**Skills needed for Support:**

| Skill | Why It Matters | Depth Required |
|-------|---------------|---------------|
| **Active Directory / LDAP** | Most issues involve directory lookups, group membership, or replication | Deep — you need to read AD logs, understand OU structure, run LDAP queries |
| **SAML / OIDC basics** | SSO failures require understanding token flows and certificate issues | Intermediate — read SAML assertions, check metadata, identify certificate expiry |
| **Basic scripting** | Automate repetitive tasks (PowerShell for AD, Python for API calls) | Intermediate — write and modify scripts |
| **Log analysis** | Authentication logs tell you what happened and why | Intermediate — read and correlate logs from multiple systems |
| **Networking basics** | Connectivity issues cause many IAM problems | Intermediate — understand DNS, firewalls, TLS/SSL |
| **Communication** | You interact with frustrated users daily | Essential — explain technical issues to non-technical people |

**Key awareness for Support:**
- You do not decide which product to buy — that was decided before you joined
- You work within the product's limitations; you cannot redesign it
- Vendor documentation and support tickets are your primary tools
- Most problems have happened before — knowledge bases are valuable
- Escalation paths exist for bugs or product limitations

**Career levels in Support:**
- **L1:** Password resets, account unlocks, basic provisioning, ticket triage
- **L2:** Complex provisioning, SSO troubleshooting, MFA problems, group policy issues
- **L3:** Escalation handling, incident response, root cause analysis, vendor coordination

---

#### 2. IAM Implementation (Deploying and Configuring Solutions)

**What Implementation Engineers / Consultants do:**
Implementation engineers deploy new IAM solutions or reconfigure existing ones. They take a product (or multiple products) and make it work for the organization's specific requirements.

**Typical projects:**
- Deploy Okta or Azure AD for workforce SSO
- Implement SailPoint for access governance and certification
- Configure CyberArk for privileged access management
- Set up Azure AD Connect for hybrid identity synchronization
- Integrate a new SaaS application with corporate SSO
- Migrate from one IdP to another (e.g., on-premises AD FS to cloud Azure AD)
- Design and deploy MFA across all users
- Implement Identity Governance workflows (access requests, approvals, certifications)

**What they work with:**
- The **same products** as Support, but they configure them rather than operate them
- **Project documentation:** Requirements documents, design documents, test plans
- **Integration tools:** APIs, SCIM connectors, SAML/OIDC configuration, PowerShell scripts
- **Multiple stakeholders:** Security team, IT team, application owners, business users

**Skills needed for Implementation:**

| Skill | Why It Matters | Depth Required |
|-------|---------------|---------------|
| **Product-specific expertise** | Each IAM product has its own architecture, configuration language, and limitations | Deep for your primary products — you are the expert |
| **SAML / OIDC / OAuth** | Every SSO integration requires protocol configuration | Deep — you configure assertions, claims, scopes, grant types, metadata exchange |
| **Directory services** | Implementing IAM requires connecting to AD, LDAP, or cloud directories | Deep — design sync architecture, attribute mapping, replication |
| **API integration** | Connecting IAM to applications requires REST API work | Intermediate-Deep — read API docs, build connectors, handle errors |
| **Project management** | Implementations have timelines, milestones, and stakeholders | Intermediate — track progress, manage scope, communicate status |
| **Security architecture** | Design secure flows that meet organizational requirements | Intermediate — understand threat models, design mitigations |
| **Scripting / Automation** | Configure, migrate, and integrate using code | Intermediate-Deep — PowerShell, Python, or product-specific languages |

**Key awareness for Implementation:**
- Requirements gathering is half the job — you cannot implement what you do not understand
- Legacy systems are the hardest part — modern apps support SAML/OIDC; old ones do not
- Rollback plans are essential — if the go-live fails, you must restore service quickly
- Testing is critical — test every user type, every application, every edge case
- Change management matters — users need training on new login flows
- Documentation is your legacy — the support team will live with what you build

**Career levels in Implementation:**
- **Junior Implementation Engineer:** Configure simple integrations, follow runbooks, assist senior engineers
- **Implementation Engineer:** Lead medium projects, design integrations, troubleshoot complex configurations
- **Senior Implementation Engineer / Architect:** Design enterprise-wide IAM architecture, lead multi-product deployments, evaluate vendors

---

#### 3. IAM Development (Building Custom Solutions and Integrations)

**What IAM Developers do:**
IAM developers write code to build custom IAM functionality, integrate systems that do not have out-of-the-box connectors, and extend COTS products through APIs and plugins.

**Typical work:**
- Build custom provisioning connectors for legacy applications
- Develop CIAM (Customer IAM) features — user registration, login, profile management
- Write authentication middleware for custom applications
- Build automated access review and certification tools
- Develop custom workflows for access requests and approvals
- Integrate IAM systems with SIEM, ITSM, or HR systems
- Build identity synchronization tools between directories
- Develop custom reporting and analytics dashboards

**What they work with:**
- **Programming languages:** Python, Java, JavaScript/TypeScript, C#, Go
- **IAM protocols and libraries:** OAuth 2.0, OIDC, SAML, SCIM, LDAP, Kerberos
- **APIs:** REST, GraphQL, SOAP (for legacy systems)
- **Databases:** SQL and NoSQL for identity stores and audit logs
- **Cloud services:** AWS IAM APIs, Azure Graph API, Google Cloud IAM
- **Frameworks:** Spring Security, Passport.js, Auth0 SDKs, Okta SDKs

**Skills needed for Development:**

| Skill | Why It Matters | Depth Required |
|-------|---------------|---------------|
| **Software engineering** | You are building production systems that handle authentication | Deep — clean code, testing, security, scalability |
| **Cryptography basics** | You work with hashing, encryption, JWTs, certificates | Intermediate-Deep — understand what you are using and why |
| **IAM protocols** | Implementing OAuth, OIDC, SAML, SCIM requires protocol knowledge | Deep — you implement the specs, not just configure them |
| **API design** | Building IAM services means designing APIs others will use | Intermediate-Deep — RESTful design, versioning, error handling |
| **Security coding practices** | Authentication code is high-risk — vulnerabilities are critical | Deep — OWASP Top 10, secure coding, input validation, output encoding |
| **Database design** | Identity stores and audit logs require proper schema design | Intermediate — normalization, indexing, query optimization |
| **DevOps / CI/CD** | Deploy IAM components safely and reliably | Intermediate — containers, pipelines, infrastructure as code |

**Key awareness for Development:**
- Do not build what you can buy — custom IAM components are expensive to maintain and secure
- When you must build, follow standards (OAuth 2.0, OIDC, SCIM) rather than inventing protocols
- Security review is mandatory — authentication code must be reviewed by security experts
- Testing is non-negotiable — a bug in login code locks out all users
- Documentation is code — other developers and support staff depend on your docs
- You are building the keys to the kingdom — take that responsibility seriously

**Career levels in Development:**
- **Junior IAM Developer:** Write scripts and small features, fix bugs, maintain existing code
- **IAM Developer:** Build connectors and integrations, implement authentication flows, develop features
- **Senior IAM Developer / Engineer:** Design architecture, build core IAM services, lead technical decisions

---

### Support vs Implementation vs Development — Side by Side

| Aspect | Support | Implementation | Development |
|--------|---------|---------------|-------------|
| **Primary question** | "Why is it broken?" | "How do we deploy this?" | "How do we build this?" |
| **Code involvement** | Scripts for automation | Scripts for configuration | Full application development |
| **Product focus** | Operate existing products | Deploy and configure products | Build custom or extend products |
| **User interaction** | End users with problems | Project stakeholders | Product managers, other developers |
| **Documentation type** | Runbooks, KB articles | Design docs, test plans | API docs, code comments, architecture docs |
| **Primary deliverable** | Resolved tickets | Working IAM environment | Working code and integrations |
| **Typical employer** | Any organization with IAM | Consulting firms, system integrators, large enterprises | Tech companies, product vendors, enterprises with custom needs |
| **Entry barrier** | Lower — certifications help | Medium — product training required | Higher — computer science foundation needed |

### Career Progression Between Tracks

Movement between tracks is common and valuable:

```
Support Engineer → Implementation Engineer
         │                │
         │ (deep product knowledge enables better implementations)
         │                │
         └────────────────┘
                │
                ▼
     IAM Developer (understanding real-world problems helps build better solutions)
                │
                ▼
     IAM Architect / Consultant (combines all three perspectives)
```

**Why cross-track experience is valuable:**
- **Support → Implementation:** You know the common failure modes and design to avoid them
- **Implementation → Development:** You know what integrations are painful and build better APIs
- **Development → Support:** You understand the code and can debug faster than anyone

---

## How IAM Systems Work

### The Access Request Flow

When a user attempts to access a resource, the IAM system performs a sequence of operations:

```
User requests access to Resource X
           │
           ▼
    ┌─────────────┐
    │  Step 1:    │
    │ Authentication│
    │ "Who are you?"│
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ Verify      │
    │ credentials │
    │ (password,  │
    │ MFA, cert)  │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Step 2:    │
    │ Authorization│
    │ "What can you│
    │  do?"       │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ Evaluate    │
    │ policies    │
    │ against     │
    │ identity and│
    │ context     │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Step 3:    │
    │   Decision   │
    │ Allow / Deny │
    │ / Step-up    │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Step 4:    │
    │   Logging    │
    │ Record for   │
    │ audit        │
    └─────────────┘
```

### Authentication Flow Deep Dive

**Password-based authentication:**
```
1. User enters username and password
2. System looks up user's stored password hash
3. System hashes the entered password using the same algorithm
4. System compares the two hashes
5. If they match → authentication succeeds
6. If they don't match → authentication fails
```

**Why passwords are stored as hashes, not plaintext:**
- If the database is breached, attackers get hashes, not actual passwords
- Hashing is one-way: you cannot reverse a hash to get the password
- Each user should have a unique salt so identical passwords produce different hashes
- Modern algorithms (bcrypt, Argon2) are intentionally slow to resist brute force

---

## Where You See IAM

| Product/Service | IAM Function | Use Case |
|----------------|-------------|----------|
| **Active Directory / Azure AD** | Directory, authentication, group policy | Enterprise Windows domain authentication |
| **Okta** | Cloud identity, SSO, MFA | Workforce identity and SaaS application access |
| **AWS IAM** | Cloud resource access control | Managing who can access AWS services |
| **Google Workspace** | Identity, email, document access | Corporate email and collaboration |
| **CyberArk** | Privileged access management | Securing admin and service accounts |
| **SailPoint** | Identity governance | Access certification and compliance |
| **Duo / Microsoft Authenticator** | Multi-factor authentication | Adding second factor to logins |
| **Linux PAM** | Pluggable authentication | Unix/Linux system authentication |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "IAM is just about passwords" | IAM encompasses identity lifecycle, authentication, authorization, governance, audit, and privilege management. Passwords are one small piece. |
| "Authentication and authorization are the same thing" | Authentication proves identity. Authorization determines permissions. You need both. |
| "Least privilege slows down work" | Properly implemented least privilege through roles and automation enables quick, appropriate access while preventing misuse. |
| "SoD only matters in finance" | SoD applies to any process where one person could cause harm: code deployment, data management, system administration. |
| "Once authenticated, you're trusted forever" | Good IAM systems re-evaluate trust continuously: session timeouts, step-up authentication, risk-based re-verification. |
| "IAM is an IT problem, not a business problem" | IAM decisions require business input: who needs what access, what are the risks, what is the compliance requirement. |
| "Organizations build their own IAM from scratch" | 90%+ of organizations buy COTS products (Okta, Azure AD, SailPoint). Custom development is rare and reserved for unique requirements. |

---

## How to Practice

### Exercise 1: Authentication vs Authorization
For each scenario, identify whether it is authentication or authorization:
1. A user enters a username and password
2. The system checks if the user is in the "Managers" group
3. A fingerprint scan unlocks a smartphone
4. The application denies access to an admin page
5. An API key is validated against a database
6. The system checks if the user owns the document they are trying to edit

### Exercise 2: Apply Least Privilege
A new employee joins as a Junior Accountant. List:
1. What systems and data they NEED access to
2. What systems and data they should NOT have access to
3. What temporary access they might need occasionally (and how to handle it)

### Exercise 3: Identify SoD Conflicts
For each pair of permissions, determine if they create a separation of duties conflict:
1. Create purchase order + Approve purchase order
2. Read financial reports + Read marketing materials
3. Deploy code to production + Review code changes
4. Create user accounts + Reset user passwords
5. Approve invoices + Process payments
6. Read customer data + Read employee data

### Exercise 4: Map a JML Lifecycle
Document the complete JML lifecycle for one role in your organization or a hypothetical company:
- JOINER: What access is provisioned on day 1?
- MOVER: What happens when promoted or transferred?
- LEAVER: What is revoked and when?
- Identify any gaps in the current process

### Exercise 5: Career Track Analysis
Research three IAM job postings (one for Support, one for Implementation, one for Development). Compare:
- Required skills and certifications
- Years of experience expected
- Product knowledge required
- Coding requirements
- Salary ranges

### Exercise 6: Run the Simulations
- `identity_lifecycle_sim.py` — Simulates JML processes
- `iam_maturity_assessment.py` — Evaluates IAM program maturity
- `iam_concept_matcher.py` — Tests knowledge of IAM terminology

---

## Projects

### `identity_lifecycle_sim.py`
Simulates the complete JML lifecycle:
- Joiner: Identity creation, attribute assignment, role provisioning
- Mover: Access review, old access revocation, new access granting, SoD checking
- Leaver: Immediate disablement, access revocation, session termination, archiving
- Demonstrates access creep when mover processes fail
- Generates audit trail for compliance

### `iam_maturity_assessment.py`
Evaluates organizational IAM maturity across dimensions:
- Identity lifecycle management
- Authentication strength
- Authorization model
- Privileged access management
- Governance and compliance
- Provides maturity score and improvement recommendations

### `iam_concept_matcher.py`
Interactive quiz covering:
- Authentication vs authorization scenarios
- Least privilege application
- SoD conflict identification
- JML process stages
- IAM component matching

---

## Check Your Understanding

1. What is the difference between Authentication and Authorization? Give three real-world examples where both occur in sequence.
2. Explain the Principle of Least Privilege in your own words. Why is it a foundational security principle? What happens when it is ignored?
3. What is Separation of Duties? Give three examples from different domains (finance, software development, system administration) and explain the risk each prevents.
4. Describe the Joiner-Mover-Leaver (JML) lifecycle. What specific actions must occur at each stage? What are the risks if any stage is poorly executed?
5. What is access creep? How does it happen during the Mover stage? What process prevents it?
6. Why must leaver offboarding disable accounts BEFORE the employee is notified of termination? Describe a scenario where this timing matters.
7. Compare preventive, detective, and compensating SoD controls. When would you use each?
8. A new developer starts and is given full production database access "just in case." Identify all the problems with this decision using IAM principles.
9. How does the CIA Triad relate to IAM? Give one IAM example for each pillar (Confidentiality, Integrity, Availability).
10. Design an IAM onboarding process for a hospital: a new nurse needs access to patient records, scheduling systems, and the medication administration system. What access should be granted immediately, what should require approval, and what should be denied?
11. What is the difference between IAM Support, IAM Implementation, and IAM Development? Which skills overlap and which are unique to each track?
12. Why do most organizations buy COTS IAM products rather than building from scratch? What are the risks of building a custom identity provider?
13. A company wants to deploy SSO for 50 SaaS applications. Should they hire a Support engineer, an Implementation engineer, or a Developer? Justify your answer.
14. What skills would you need to move from IAM Support to IAM Implementation? What additional skills to move from Implementation to Development?
