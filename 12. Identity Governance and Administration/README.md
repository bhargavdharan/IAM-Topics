# 12. Identity Governance and Administration (IGA)

## What Is IGA?

**Identity Governance and Administration (IGA)** is the discipline of ensuring that the right people have the right access to the right resources — and proving it.

While IAM focuses on enabling access, IGA focuses on **controlling, monitoring, and reviewing** access over time. It answers questions like:
- Who has access to what?
- Should they still have it?
- Can we prove it to auditors?

---

## Why Learn This?

Compliance regulations (SOX, GDPR, HIPAA, PCI-DSS) require organizations to demonstrate control over access. Orphaned accounts, excessive permissions, and missing audit trails are common findings in security assessments.

IGA is essential for:
- Passing compliance audits
- Preventing privilege creep
- Detecting insider threats
- Automating access reviews

---

## Core Concepts

### IGA Core Functions

| Function | Purpose | Example |
|----------|---------|---------|
| **Identity Lifecycle** | Manage users from hire to retire | Onboarding → Role changes → Offboarding |
| **Access Request** | Users request access to resources | Requesting access to a specific system |
| **Access Certification** | Managers review and approve access | Quarterly review of team permissions |
| **Provisioning** | Automatically grant approved access | Creating accounts in target systems |
| **Deprovisioning** | Automatically revoke access | Disabling accounts on termination |
| **Segregation of Duties** | Prevent conflicting access | Same person cannot buy and approve |
| **Reporting** | Generate compliance evidence | Access certification reports |

### The Identity Lifecycle (Governance View)

```
Joiner ──→ Provision ──→ Review ──→ Change ──→ Deprovision
```

At each stage, governance asks:
- **Joiner:** What access does this person need based on their role?
- **Provision:** Was access granted according to policy?
- **Review:** Does this person still need this access?
- **Change:** When roles change, is access adjusted appropriately?
- **Deprovision:** Is all access removed on termination?

### Access Reviews (Certifications)

Access reviews are periodic audits where managers validate that their team members still need their access:

| Type | Scope | Frequency |
|------|-------|-----------|
| **User Access Review** | Everything one user has | Quarterly |
| **Resource Access Review** | Everyone with access to a resource | Annually |
| **Role Access Review** | Everyone in a role | Semi-annually |
| **SoD Review** | Conflicting access combinations | Quarterly |

**The certification process:**
1. System generates review campaign
2. Manager sees list of access items
3. Manager certifies or revokes each item
4. System automatically applies revocations
5. Audit log records all decisions

### Segregation of Duties (SoD)

SoD prevents fraud by ensuring no single person can complete a sensitive process:

| Process | Conflicting Roles | Why |
|---------|-------------------|-----|
| Purchasing | Purchaser + Approver | Can't buy AND approve own purchase |
| Payroll | Time Entry + Payment Authorization | Can't pay yourself extra hours |
| Development | Developer + Production Deployer | Can't push malicious code alone |

**Enforcement types:**
- **Preventive:** System blocks conflicting role assignments
- **Detective:** System flags existing conflicts for review
- **Mitigating:** Compensating controls when exceptions are needed

---

## How It Works

### How Access Review Systems Work

1. **Data Collection:** Query all identity sources and aggregate role assignments
2. **Campaign Generation:** Define scope, assign reviewers, set deadlines
3. **Decision Processing:** Reviewers certify, revoke, or reassign access
4. **Remediation:** System applies decisions and creates exceptions if needed
5. **Audit Trail:** All decisions logged with timestamps and justifications

### Compliance Frameworks and IGA

| Framework | IGA Requirement |
|-----------|----------------|
| **SOX** | Prove only authorized users access financial systems |
| **GDPR** | Track who accesses personal data |
| **HIPAA** | Ensure only necessary staff access patient records |
| **PCI-DSS** | Restrict cardholder data access to need-to-know |
| **ISO 27001** | Regular access reviews and documented controls |

### Identity Analytics

Modern IGA uses analytics to find risks:
- **Orphaned accounts:** Active accounts with no valid owner
- **Excessive access:** Users with more permissions than peers
- **Privilege creep:** Gradual accumulation of access over time
- **SoD violations:** Users with conflicting role combinations
- **Dormant access:** Permissions unused for 90+ days

---

## Where You See It

| Product | IGA Feature |
|---------|------------|
| **SailPoint** | Access certification campaigns |
| **Oracle Identity Governance** | SoD policy enforcement |
| **Microsoft Identity Manager** | Identity lifecycle management |
| **Saviynt** | Cloud-native IGA |
| **Okta Identity Governance** | Access requests and reviews |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "IGA is just access reviews" | IGA includes lifecycle management, SoD, reporting, and analytics |
| "Compliance is the only reason for IGA" | IGA also prevents breaches, reduces risk, and improves efficiency |
| "Access reviews are annual only" | Best practice is quarterly or continuous |
| "IGA replaces IAM" | IGA complements IAM by adding governance |

---

## How to Practice

1. **Conduct a mock access review**
   - List all accounts and permissions in a small system
   - Ask: Does each person still need each permission?
   - Document your decisions

2. **Identify SoD violations in a scenario**
   - Create a list of users and their roles
   - Check for conflicting combinations
   - Propose remediation

3. **Run the simulations**
   - `access_review_sim.py` simulates a certification campaign
   - `sod_policy_checker.py` detects violations

---

## Projects

### `access_review_sim.py`
Simulates an access review campaign:
- Generates users, roles, and permissions
- Creates review assignments for managers
- Processes certification decisions
- Applies automatic revocations

### `sod_policy_checker.py`
Checks for Segregation of Duties violations:
- Defines conflicting role pairs
- Scans user-role assignments
- Identifies violations and suggests remediation

### `identity_lifecycle_governance.py`
Tracks users through the complete lifecycle:
- Onboarding workflows with approval
- Role change tracking
- Offboarding with access revocation

### `compliance_report_generator.py`
Generates audit-ready compliance reports:
- User access inventory
- Privileged account reports
- SoD violation summaries

---

## Check Your Understanding

1. What is the difference between IAM and IGA? Why do organizations need both?
2. Describe the access certification process. Who performs it and what decisions can they make?
3. What is privilege creep and why is it dangerous?
4. Give three examples of Segregation of Duties and explain why each prevents fraud.
5. How does IGA help with compliance audits? What evidence does it provide?
