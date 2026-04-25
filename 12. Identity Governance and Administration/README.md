# 12. Identity Governance and Administration (IGA)

## 🏠 Real-World Analogy: The Annual Home Inventory

Imagine owning a large house with many rooms, each containing valuable items:

- Over the years, you've given spare keys to friends, family, cleaners, and dog walkers
- Some people moved away but never returned their keys
- Some rooms contain sensitive documents that only certain people should access
- You have no idea who currently has access to what

**Identity Governance is the annual ritual of:**
1. Going through every room and checking who has keys
2. Asking "Does [Person X] still need access to [Room Y]?"
3. Collecting keys from people who no longer need them
4. Documenting who has access to what for insurance purposes
5. Setting rules so this doesn't happen again

**IGA is exactly this — but for an organization's digital identities and access rights.**

---

## 📋 Overview

Identity Governance and Administration (IGA) is the discipline of ensuring that the right people have the right access to the right resources — and proving it to auditors.

While IAM focuses on enabling access, IGA focuses on **controlling, monitoring, and reviewing** access over time.

**Why IGA is critical:**
- Compliance requirements (SOX, GDPR, HIPAA) demand proof of access control
- Orphaned accounts and excessive permissions are major security risks
- Manual access management doesn't scale
- Auditors will ask: "Who has access to financial data? Prove it."

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain IGA with real-world analogies
- Describe the identity lifecycle from governance perspective
- Understand access reviews, certifications, and recertification
- Explain segregation of duties (SoD) policies
- Understand compliance frameworks and how IGA supports them
- Implement an access review campaign simulator

---

## 📚 Key Concepts

### IGA Core Functions

| Function | Description | Real-World Analogy |
|----------|-------------|-------------------|
| **Identity Lifecycle** | Manage users from hire to retire | Onboarding → Role changes → Offboarding |
| **Access Request** | Users request access to resources | Requesting a key to a specific room |
| **Access Certification** | Managers review and approve access | Annual key audit with sign-off |
| **Provisioning** | Automatically grant approved access | Cutting a new key |
| **Deprovisioning** | Automatically revoke access | Collecting and destroying old keys |
| **Segregation of Duties** | Prevent conflicting access | Not letting the same person buy AND approve |
| **Reporting & Analytics** | Generate compliance reports | Inventory list for insurance |

### The Identity Lifecycle (Governance View)

```
Joiner ─────────────────────────────────────────────────────────→ Leaver
   │                                                                │
   ▼                                                                ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Hire    │───→│ Provision│───→│  Review  │───→│  Change  │───→│ Deprovision
│          │    │  Access  │    │  Access  │    │  Access  │    │   Access   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │               │               │
                     ▼               ▼               ▼
                Manager        Quarterly         Role change
                approves       access review     or transfer
```

### Access Reviews (Certifications)

Access reviews are periodic audits where managers validate that their team members still need their access:

**Types of Reviews:**

| Type | Scope | Frequency | Who Performs |
|------|-------|-----------|--------------|
| **User Access Review** | Everything one user has | Quarterly | User's manager |
| **Resource Access Review** | Everyone with access to a resource | Annually | Resource owner |
| **Role Access Review** | Everyone in a role | Semi-annually | Role owner |
| **SoD Review** | Conflicting access combinations | Quarterly | Compliance team |

**The Certification Process:**
1. System generates review campaign: "Manager Alice, please review your team's access"
2. Alice sees a list: Bob has [Finance, Developer, Admin]
3. Alice certifies: "Bob still needs Finance and Developer. Remove Admin."
4. System automatically revokes Admin access from Bob
5. Audit log records: "Alice certified Bob's access on 2024-01-15. Admin revoked."

### Segregation of Duties (SoD)

SoD prevents fraud by ensuring no single person can complete a sensitive process:

| Process | Conflicting Roles | Why |
|---------|-------------------|-----|
| Purchasing | Purchaser + Approver | Can't buy AND approve your own purchase |
| Payroll | Time Entry + Payment Authorization | Can't pay yourself extra hours |
| Development | Developer + Production Deployer | Can't push malicious code yourself |
| Banking | Wire Initiator + Wire Approver | Can't steal money alone |

**SoD Enforcement:**
- **Preventive:** System blocks conflicting role assignments
- **Detective:** System flags existing conflicts for review
- **Mitigating:** Compensating controls (additional approvals) when exceptions are needed

---

## 🔧 Under the Hood

### How Access Review Systems Work

**Data Collection:**
1. Query all identity sources (AD, LDAP, cloud directories)
2. Aggregate role assignments, group memberships, and direct permissions
3. Normalize data into a unified format
4. Identify ownership (who should certify this access?)

**Campaign Generation:**
1. Define review scope (users, resources, or roles)
2. Assign reviewers (managers, resource owners)
3. Set deadlines and escalation paths
4. Generate review tasks and send notifications

**Decision Processing:**
1. Reviewer logs into portal and sees assigned reviews
2. For each access item, reviewer chooses: Certify / Revoke / Reassign
3. System applies decisions automatically or queues for approval
4. Exceptions (keeping conflicting access) require additional justification

**Audit Trail:**
```json
{
  "campaign_id": "Q1-2024-Finance",
  "reviewer": "manager.alice",
  "subject": "developer.bob",
  "decisions": [
    {"resource": "Finance-Reports", "decision": "certified", "timestamp": "2024-01-15T10:00:00Z"},
    {"resource": "Admin-Panel", "decision": "revoked", "timestamp": "2024-01-15T10:05:00Z"}
  ],
  "justification": "Bob no longer administers servers."
}
```

### Compliance Frameworks and IGA

| Framework | IGA Requirement | Penalty for Non-Compliance |
|-----------|----------------|---------------------------|
| **SOX** | Prove only authorized users access financial systems | Criminal penalties for executives |
| **GDPR** | Track who accesses personal data | Up to 4% of global revenue |
| **HIPAA** | Ensure only necessary staff access patient records | Fines up to $1.5M per violation |
| **PCI-DSS** | Restrict cardholder data access to need-to-know | Loss of ability to process payments |
| **ISO 27001** | Regular access reviews and documented controls | Loss of certification |

### Identity Analytics

Modern IGA uses analytics to find risks:

- **Orphaned accounts:** Active accounts with no valid owner (former employees)
- **Excessive access:** Users with more permissions than 95% of peers
- **Privilege creep:** Gradual accumulation of access over time
- **SoD violations:** Users with conflicting role combinations
- **Dormant access:** Permissions unused for 90+ days
- **Shared accounts:** Multiple people using the same identity

---

## 🛠️ Projects in This Module

### `access_review_sim.py`
Simulates an access review campaign:
- Generates users, roles, and permissions
- Creates review assignments for managers
- Processes certification decisions
- Applies automatic revocations
- Generates compliance reports

### `sod_policy_checker.py`
Checks for Segregation of Duties violations:
- Defines conflicting role pairs
- Scans user-role assignments
- Identifies violations
- Suggests remediation actions
- Handles exception workflows

### `identity_lifecycle_governance.py`
Tracks users through the complete lifecycle:
- Onboarding workflows with approval
- Role change tracking
- Transfer and promotion handling
- Offboarding with access revocation
- Retention policy enforcement

### `compliance_report_generator.py`
Generates audit-ready compliance reports:
- User access inventory
- Privileged account reports
- Access review completion rates
- SoD violation summaries
- Orphaned account listings

---

## 📝 Quiz Questions

1. **What is the difference between IAM and IGA? Why do organizations need both?**
2. **Describe the access certification process. Who performs it and what decisions can they make?**
3. **What is privilege creep and why is it dangerous?**
4. **Give three examples of Segregation of Duties and explain why each prevents fraud.**
5. **How does IGA help with compliance audits? What evidence does it provide?**

---

## 🔗 Further Reading

- [NIST SP 800-53 - Access Control](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [Gartner IGA Magic Quadrant](https://www.gartner.com)
- [SOX Compliance and Access Control](https://www.coso.org/)

---

## 🏷️ Tags
`#IGA` `#IdentityGovernance` `#AccessReview` `#Compliance` `#SoD` `#Certification` `#Audit`
