# 14. Cloud IAM

## 🏠 Real-World Analogy: The Co-Working Space

Imagine a massive co-working space with hundreds of companies:

**Traditional data center (on-prem):**
- Your company owns the building
- You control the locks, elevators, and security guards
- You're responsible for everything — including mistakes

**Cloud (AWS/Azure/GCP):**
- You rent desks in a massive shared building
- The building owner (cloud provider) handles physical security, elevators, and HVAC
- But YOU control who can access YOUR desks, files, and meeting rooms
- You can rent more desks instantly or downsize tomorrow
- Other companies in the building can't access your stuff (isolation)
- You pay only for what you use

**Cloud IAM is the digital version of managing access in this co-working space.**

---

## 📋 Overview

Cloud IAM is the identity and access management system built into cloud platforms (AWS, Azure, Google Cloud). It governs who can do what on which cloud resources.

**Why Cloud IAM is different:**
- Resources are ephemeral (created and destroyed instantly)
- Scale is massive (millions of resources)
- Everything is API-driven
- Multi-tenant (shared infrastructure, isolated access)
- Pay-per-use model requires granular access control

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain Cloud IAM with real-world analogies
- Compare IAM across AWS, Azure, and Google Cloud
- Understand cloud identities: users, roles, service accounts, and policies
- Describe policy structure and evaluation
- Implement least privilege in cloud environments
- Simulate cloud IAM policy evaluation

---

## 📚 Key Concepts

### Cloud Identity Types

| Identity Type | AWS | Azure | GCP | Description |
|--------------|-----|-------|-----|-------------|
| **Human User** | IAM User | Entra ID User | Google Account | Person logging into console |
| **Group** | IAM Group | Entra ID Group | Google Group | Collection of users |
| **Role** | IAM Role | Azure Role | IAM Role | Temporary permission set |
| **Service Account** | IAM Role / User | Managed Identity | Service Account | Identity for applications |
| **Federated User** | IAM Identity Center | Entra ID Federation | Cloud Identity | External identity provider |

### The Principle of Least Privilege in Cloud

**Common mistake:** Giving everyone "Admin" access because "it's easier."

**Why this is dangerous in cloud:**
- Accidental deletion of production resources
- Malicious insider actions
- Compromised credentials have unlimited power
- Compliance violations

**Best practice:** Start with zero permissions, add only what's needed.

### AWS IAM Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3Read",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::company-data-bucket",
        "arn:aws:s3:::company-data-bucket/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "us-east-1"
        },
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    }
  ]
}
```

| Element | Description |
|---------|-------------|
| **Effect** | Allow or Deny |
| **Action** | What operation is permitted |
| **Resource** | What resource the action applies to |
| **Condition** | Optional constraints (time, IP, etc.) |

### Cross-Cloud IAM Comparison

| Feature | AWS IAM | Azure RBAC | GCP IAM |
|---------|---------|-----------|---------|
| **Policy format** | JSON | JSON | JSON / YAML |
| **Inheritance** | Identity-based + Resource-based | Subscription → RG → Resource | Organization → Folder → Project → Resource |
| **Deny policies** | Explicit Deny overrides Allow | Deny assignments (preview) | Deny policies |
| **Temporary access** | IAM Roles (STS) | PIM (Privileged Identity Management) | Service account impersonation |
| **Permission boundaries** | IAM Permissions Boundaries | Management Groups | IAM Conditions |

---

## 🔧 Under the Hood

### How Cloud IAM Policy Evaluation Works

When a user tries to access a cloud resource, the IAM engine evaluates policies in this order:

```
1. Is there an explicit DENY? 
   → YES → ACCESS DENIED (Deny always wins)
   
2. Is there an explicit ALLOW?
   → YES → ACCESS ALLOWED
   
3. Is there no matching policy?
   → ACCESS DENIED (default deny — implicit denial)
```

**This is called "default deny" or "implicit deny."** If no policy explicitly allows an action, it is denied.

### AWS STS (Security Token Service)

STS enables temporary credentials:

```python
import boto3

# Assume a role for temporary access
sts = boto3.client('sts')
response = sts.assume_role(
    RoleArn='arn:aws:iam::123456789:role/ReadOnlyRole',
    RoleSessionName='AliceSession',
    DurationSeconds=3600  # 1 hour
)

temp_credentials = response['Credentials']
# Now use temp_credentials to access AWS resources
# After 1 hour, credentials expire automatically
```

**Why temporary credentials are safer:**
- No long-lived access keys to leak
- Automatic expiration
- Every session is logged in CloudTrail
- Can be revoked immediately if suspicious

### Azure RBAC and PIM

**Azure RBAC Hierarchy:**
```
Management Group (Root)
└── Subscription
    └── Resource Group
        └── Resource (VM, Storage, etc.)
```

Permissions flow down the hierarchy. A role assignment at the Subscription level applies to all resources in that subscription.

**Privileged Identity Management (PIM):**
- Roles are "eligible" but not "active" by default
- User must activate the role (with approval if configured)
- Role activation is time-limited (e.g., 4 hours)
- Requires MFA to activate
- Every activation is audited

### GCP IAM and Resource Hierarchy

```
Organization (example.com)
└── Folder (Engineering)
    └── Folder (Backend Team)
        └── Project (production-api)
            └── Resources (VMs, buckets, etc.)
```

**Policy inheritance:** Permissions granted at the Organization level apply to ALL resources below. This is powerful but dangerous — use sparingly.

**Service Account Impersonation:**
- Instead of downloading service account keys (which can leak)
- A human or service account "impersonates" another service account
- No key files needed
- Every impersonation is logged

### Cloud IAM Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|-------------|-------------|----------------|
| **Root account for daily use** | Unlimited power, no audit trail | Use IAM users/roles with MFA |
| **Hardcoded access keys** | Keys leak in code repositories | Use IAM roles / instance profiles |
| **Overly permissive policies** | Violates least privilege | Start restrictive, add as needed |
| **Shared credentials** | No accountability | Individual identities |
| **Never rotating keys** | Old keys are more likely leaked | Automated rotation or temporary creds |
| **Ignoring service accounts** | Invisible privileged accounts | Regular audits and naming conventions |

---

## 🛠️ Projects in This Module

### `cloud_policy_sim.py`
Simulates cloud IAM policy evaluation:
- Parses AWS-style IAM policies
- Evaluates access requests against policies
- Handles explicit deny, allow, and implicit deny
- Supports conditions (time, IP, resource tags)
- Generates policy decision explanations

### `cross_cloud_mapper.py`
Maps IAM concepts across AWS, Azure, and GCP:
- Translates policies between cloud providers
- Compares equivalent features
- Identifies gaps in multi-cloud IAM strategies

### `least_privilege_analyzer.py`
Analyzes cloud permissions for least privilege:
- Identifies unused permissions from CloudTrail logs
- Suggests policy refinements
- Detects overly permissive wildcards (`*`)
- Generates least-privilege policy recommendations

### `service_account_auditor.py`
Audits service accounts across cloud platforms:
- Lists all service accounts
- Identifies accounts with excessive permissions
- Finds unused or stale service accounts
- Checks for key rotation compliance

---

## 📝 Quiz Questions

1. **How is Cloud IAM different from on-premises IAM? Name three key differences.**
2. **What is "default deny" in cloud IAM policy evaluation? Why is it safer than default allow?**
3. **Why are temporary credentials (like AWS STS) considered more secure than long-lived access keys?**
4. **What is Azure PIM and how does it enforce just-in-time access?**
5. **Name three Cloud IAM anti-patterns and how to fix each.**

---

## 🔗 Further Reading

- [AWS IAM Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [Azure RBAC Documentation](https://docs.microsoft.com/en-us/azure/role-based-access-control/overview)
- [Google Cloud IAM Documentation](https://cloud.google.com/iam/docs/overview)
- [Cloud Security Alliance - IAM Guidance](https://cloudsecurityalliance.org/)

---

## 🏷️ Tags
`#CloudIAM` `#AWS` `#Azure` `#GCP` `#LeastPrivilege` `#STS` `#PIM` `#ServiceAccount` `#MultiCloud`
