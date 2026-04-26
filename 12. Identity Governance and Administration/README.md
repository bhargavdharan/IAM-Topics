# 12. Identity Governance and Administration (IGA)

## What Is IGA?

**Identity Governance and Administration (IGA)** is the set of policies, processes, and technologies that ensure the right people have the right access to the right resources at the right time — and that this access is continuously reviewed and audited.

While IAM focuses on authentication and authorization at the point of access, IGA focuses on the governance lifecycle:
- Who should have access?
- How was access granted?
- Is access still needed?
- Can we prove compliance?

IGA bridges the gap between IT operations and business accountability, ensuring that access decisions align with organizational policy and regulatory requirements.

---

## Why Learn This?

Organizations face constant access-related challenges:
- **Access creep:** Users accumulate permissions over time that they no longer need
- **Orphaned accounts:** Accounts belonging to departed employees remain active
- **Segregation of duties violations:** One person has conflicting permissions (e.g., can both approve and pay invoices)
- **Compliance requirements:** Regulators demand evidence of access governance
- **Audit findings:** Auditors flag inadequate access reviews and missing justifications

Understanding IGA is essential for:
- Designing sustainable access management
- Preparing for compliance audits
- Reducing insider threat risk
- Automating access reviews
- Implementing separation of duties

---

## Core Concepts

### IGA Core Functions

| Function | Description | Goal |
|----------|-------------|------|
| **Identity Lifecycle Management** | Managing users from onboarding to offboarding | Ensure timely access provisioning and deprovisioning |
| **Access Request & Approval** | Structured workflows for requesting and approving access | Business accountability for access decisions |
| **Access Certification** | Periodic review and attestation of access rights | Detect and remove unnecessary access |
| **Policy Enforcement** | Automated rules ensuring compliance | Prevent policy violations before they occur |
| **Audit & Reporting** | Comprehensive logging and analytics | Demonstrate compliance, detect anomalies |

### Access Certification (Recertification)

Access certification is the periodic review of who has access to what:

**Why it matters:**
- Users accumulate access over time (job changes, projects, temporary assignments)
- Former colleagues may have approved access that is no longer justified
- Compliance frameworks (SOX, HIPAA, PCI-DSS) require regular reviews
- Attackers exploit stale, overprivileged accounts

**The certification process:**
1. **Generate review:** System compiles list of users and their access
2. **Assign reviewers:** Managers or resource owners review their team's access
3. **Review access:** Reviewer evaluates each entitlement
4. **Make decisions:** Approve (access still needed) or Revoke (no longer needed)
5. **Execute decisions:** System automatically revokes approved-for-removal access
6. **Audit trail:** Complete record stored for compliance

**Review types:**
- **User-centric:** "What access does Alice have across all systems?"
- **Resource-centric:** "Who has access to the Finance database?"
- **Role-centric:** "Who is assigned to the Manager role?"
- **Exception-centric:** "What access was granted outside normal processes?"

### Separation of Duties (SoD)

**Separation of Duties** prevents any single individual from having conflicting permissions that could enable fraud or error.

**Examples of SoD conflicts:**

| Role A | Role B | Conflict | Risk |
|--------|--------|----------|------|
| Create vendor | Approve vendor payment | Same person can create fake vendor and pay them | Fraud |
| Request purchase | Approve purchase | Same person can authorize their own spending | Unauthorized spending |
| Write code | Deploy to production | Same person can introduce malicious code unchecked | Malware injection |
| Record transactions | Reconcile accounts | Same person can hide errors or fraud | Financial fraud |

**SoD enforcement approaches:**
1. **Preventive:** System blocks assignment of conflicting roles
2. **Detective:** System flags existing conflicts for remediation
3. **Compensating:** If SoD cannot be enforced technically, manual controls (supervisor review) compensate

**Managing SoD exceptions:**
- Some small teams cannot fully separate duties
- Exceptions require documented justification
- Exceptions are time-limited and reviewed more frequently
- Compensating controls mitigate residual risk

### Identity Lifecycle

IGA governs the complete user lifecycle:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Join    │───→│  Change  │───→│  Review  │───→│  Update  │───→│  Leave   │
│(Hire)    │    │(Transfer)│    │(Certify) │    │(Refresh) │    │(Terminate)│
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │               │
     ▼               ▼               ▼               ▼               ▼
Create account   Update roles   Verify access   Renew certs    Disable account
Assign roles     Remove old     Attest need     Update MFA     Revoke access
Provide access   Add new        Flag orphan     Refresh pwd    Archive data
Notify manager   Notify team    Remediate       Approve cont.  Retain audit log
```

**Key transitions:**
- **Join:** Automated provisioning based on HR data; manager notification
- **Change:** Role transitions trigger automatic access adjustments
- **Review:** Periodic certification ensures continued appropriateness
- **Update:** Credential refresh, MFA re-enrollment, policy changes
- **Leave:** Immediate deprovisioning with full audit trail

### Role Mining

**Role mining** is the process of analyzing existing user permissions to discover patterns and define roles:

1. **Collect data:** Export all user-permission assignments
2. **Analyze patterns:** Users with similar job functions have similar access
3. **Define candidate roles:** Group common permissions into roles
4. **Validate with business:** Confirm roles align with job functions
5. **Implement and refine:** Deploy roles; adjust based on exceptions

**Benefits:**
- Reduces complexity of managing individual permissions
- Improves consistency in access assignment
- Simplifies access reviews (review roles, not individual permissions)
- Reduces access provisioning errors

---

## How It Works

### Access Request Workflow

```
Employee requests access to Salesforce
           │
           ▼
    ┌─────────────┐
    │  Is there   │
    │  an SoD     │
    │  conflict?  │
    └─────────────┘
       Yes │   │ No
          ▼   ▼
    ┌──────────┐    ┌─────────────┐
    │  BLOCK   │    │ Route to    │
    │  Request │    │  Manager    │
    │  (Notify)│    │  for Approval│
    └──────────┘    └─────────────┘
                         │
                   Approved│Rejected
                    ┌──────┴──────┐
                    ▼             ▼
            ┌──────────┐   ┌──────────┐
            │ Provision│   │ Notify   │
            │ Access   │   │ Employee │
            │ Log Audit│   │ Log Audit│
            └──────────┘   └──────────┘
```

### Access Certification Campaign

```
Quarterly Access Review Campaign
           │
           ▼
┌──────────────────┐
│ System generates │
│ review list      │
│ (all users +     │
│  entitlements)   │
└──────────────────┘
           │
           ▼
┌──────────────────┐
│ Reviews assigned │
│ to managers/     │
│ resource owners  │
└──────────────────┘
           │
           ▼
┌──────────────────┐
│ Reviewers assess │
│ each entitlement │
│ Approve / Revoke │
└──────────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
┌────────┐   ┌──────────┐
│Approve │   │ Revoke   │
│Log     │   │ Access   │
│Decision│   │ Removed  │
└────────┘   │ Notify   │
             │ User     │
             └──────────┘
           │
           ▼
┌──────────────────┐
│ Audit report     │
│ generated for    │
│ compliance       │
└──────────────────┘
```

### SoD Policy Engine

SoD policies are enforced through rule engines:

```
Policy Definition:
IF user.has_role("Purchase Requestor")
   AND user.has_role("Purchase Approver")
THEN trigger SoD_violation("Purchase SoD")
     action = BLOCK_ASSIGNMENT
     notify = [manager, compliance_team]
```

**Remediation workflow:**
1. System detects potential conflict during role assignment
2. Assignment is blocked or flagged
3. Exception request can be submitted with justification
4. Exception requires elevated approval (e.g., CISO, compliance officer)
5. Exception is time-bound (e.g., expires in 90 days)
6. Compensating control assigned (e.g., monthly review)

---

## Where You See It

| Product | IGA Capability | Use Case |
|---------|---------------|----------|
| **SailPoint** | Enterprise IGA platform | Access certification, role management, SoD |
| **Microsoft Entitlement Management** | Azure AD IGA | Access packages, reviews, entitlement lifecycle |
| **Okta Identity Governance** | Cloud IGA | Access certification, lifecycle automation |
| **Saviynt** | Cloud-native IGA | SoD, access reviews, analytics |
| **Oracle Identity Governance** | Enterprise IGA | Role mining, certification, workflow |
| **One Identity** | Unified IAM/IGA | Access management with governance |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "IGA is just access reviews" | Access reviews are one component. IGA also includes lifecycle management, access requests, policy enforcement, and audit. |
| "SoD is only for finance" | SoD applies to any process where a single person could commit fraud or cause harm: code deployment, data modification, vendor management. |
| "Certification reviews are a checkbox exercise" | Effective reviews require manager engagement. Automated analytics can flag high-risk access for focused review. |
| "IGA slows down business" | Well-designed IGA with automated provisioning and self-service requests improves efficiency while maintaining control. |
| "Small companies don't need IGA" | Any organization with compliance requirements, sensitive data, or audit obligations needs IGA. Scale the implementation appropriately. |

---

## How to Practice

### Exercise 1: Map Access Lifecycle
Document the complete lifecycle for one role in your organization:
1. What triggers creation? (HR hire, contractor start, promotion)
2. What access is automatically provisioned?
3. What requires approval?
4. How is access reviewed?
5. How is access removed when the person leaves?
6. What gaps exist in this lifecycle?

### Exercise 2: Identify SoD Conflicts
For a small team (5-10 people), document:
1. All critical business processes
2. The roles involved in each step
3. Where one person holds multiple conflicting roles
4. How to mitigate (separation, review, compensating control)

### Exercise 3: Design a Certification Campaign
Design an access certification process:
- How often are reviews conducted?
- Who reviews what? (managers review team, app owners review resource)
- What happens to unreviewed access?
- How are revocations executed?
- What reporting is needed for auditors?

### Exercise 4: Run the Simulations
- `access_review_sim.py` — Certification campaign simulation
- `sod_policy_checker.py` — Separation of duties validation
- `lifecycle_automation.py` — Identity lifecycle orchestration

---

## Projects

### `access_review_sim.py`
Simulates access certification campaigns:
- Generates user access lists
- Routes reviews to managers
- Collects approve/revoke decisions
- Executes automatic revocations
- Generates compliance reports

### `sod_policy_checker.py`
Validates separation of duties policies:
- Defines SoD conflict matrices
- Detects conflicting role assignments
- Supports exception management
- Generates violation reports
- Recommends remediation

### `lifecycle_automation.py`
Models identity lifecycle automation:
- Join/Move/Leave triggers
- Automatic access provisioning based on role
- Deprovisioning workflows
- Audit logging of all lifecycle events
- Analytics on access patterns

### `role_mining_sim.py`
Discovers optimal roles from access data:
- Analyzes user-permission matrices
- Groups users by permission similarity
- Suggests candidate roles
- Evaluates role coverage vs. exceptions
- Compares before/after complexity

---

## IGA in Practice: COTS Products and Operations

### IGA COTS Products

| Product | Type | Best For | Key Differentiator |
|---------|------|----------|-------------------|
| **SailPoint IdentityNow** | Enterprise IGA (cloud) | Large organizations; complex compliance | Market leader; most comprehensive; expensive |
| **SailPoint IdentityIQ** | Enterprise IGA (on-prem) | Organizations requiring on-premises | Same features as IdentityNow; self-hosted |
| **Microsoft Entitlement Management** | Cloud IGA | Microsoft-heavy environments | Included with Azure AD P2; good for mid-market |
| **Okta Identity Governance** | Cloud IGA | Okta customers; cloud-native | Integrated with Okta Workforce; simpler than SailPoint |
| **Saviynt** | Cloud-native IGA | Cloud-first organizations | Modern UI; strong analytics; faster deployment |
| **Oracle Identity Governance** | Enterprise IGA | Oracle ecosystem customers | Deep Oracle integration; complex; powerful |
| **One Identity** | Unified IAM/IGA | Organizations wanting one vendor | Combines access management with governance |

### IGA Implementation vs Ongoing Operations

**IGA Implementation project (typically 6-12 months):**
- Connect to all target systems (AD, SAP, Salesforce, etc.)
- Configure connectors and provisioning rules
- Import existing users and entitlements
- Design role model (role mining)
- Configure access request workflows
- Set up SoD policies
- Configure certification campaigns
- Build reports and dashboards
- Train administrators and managers

**IGA Ongoing Operations (Support/Analyst):**
- Run quarterly access certification campaigns
- Review and approve access requests
- Investigate SoD violations
- Generate audit reports
- Update roles as organization changes
- Troubleshoot connector failures
- Handle user complaints about access

**The IGA analyst career path:**
Unlike Support (tickets) or Implementation (projects), IGA Analysts live in the **ongoing governance cycle**. Their work is cyclical — certification reviews happen quarterly, access requests happen daily, audit preparation happens annually.

**Implementation vs Operations skill difference:**

| Skill | Implementation | Operations |
|-------|---------------|------------|
| **Connector development** | High — build integrations | Low — troubleshoot existing |
| **Role modeling** | High — design from scratch | Medium — refine over time |
| **Policy configuration** | High — initial setup | Medium — adjust as needed |
| **Audit response** | Low | High — primary responsibility |
| **Reporting** | Medium — build dashboards | High — run and interpret |

---

## Check Your Understanding

1. What is the difference between IAM and IGA? Why do organizations need both?
2. What is access certification and why is it performed periodically rather than just at onboarding?
3. Define Separation of Duties. Give three real-world examples where SoD prevents fraud or error.
4. How does the access request workflow prevent SoD violations? What happens when a true business need conflicts with SoD policy?
5. What is role mining and how does it simplify access management? What are the risks of poorly defined roles?
6. An employee transfers from Engineering to Finance. Walk through the complete IGA lifecycle events that should occur.
7. An auditor asks: "Can you prove that no terminated employee retains system access?" What IGA capabilities and evidence would you provide?
8. Design an SoD policy for a company with these roles: Sales Rep, Sales Manager, Accountant, AP Clerk, CFO. Identify at least 5 potential conflicts.
9. What is the difference between preventive, detective, and compensating controls in IGA? Give an example of each.
10. A certification review reveals 200 users with access to a sensitive system, but only 50 use it regularly. What actions should the IGA process trigger?
