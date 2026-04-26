# 14. Cloud IAM

## What Is Cloud IAM?

**Cloud IAM** refers to the identity and access management services provided by cloud platforms (AWS, Azure, Google Cloud). It governs who can access cloud resources, what they can do with them, and under what conditions.

While on-premises IAM manages users and systems within a corporate network, Cloud IAM operates across distributed, shared infrastructure where resources can be provisioned instantly from anywhere in the world.

Each major cloud provider implements IAM differently, but all share common concepts: identities, policies, resources, and permissions.

---

## Why Learn This?

Cloud IAM misconfigurations are a leading cause of data breaches:
- Overly permissive S3 buckets exposing data
- Service accounts with excessive permissions
- Unused credentials left active
- Lack of MFA on privileged cloud accounts
- Insufficient logging and monitoring

Understanding Cloud IAM is essential for:
- Securing cloud workloads
- Managing multi-cloud environments
- Implementing least privilege in the cloud
- Auditing cloud access
- Preparing for cloud compliance certifications

---

## Core Concepts

### Cloud IAM Identities

| Identity Type | AWS | Azure | GCP |
|--------------|-----|-------|-----|
| **User** | IAM User | Azure AD User | Google Account |
| **Group** | IAM Group | Azure AD Group | Google Group |
| **Service Account** | IAM Role (assumed by services) | Managed Identity | Service Account |
| **Federated Identity** | Identity Federation, SAML, OIDC | Azure AD B2B, B2C | Cloud Identity, Workspace |

**Service Accounts (Cloud context):**
- Used by applications and services, not humans
- Often have long-lived credentials (risk!)
- Should follow least privilege strictly
- Should use workload identity when possible (no long-lived secrets)

### Policy Structure

All cloud IAM policies share a common structure:

```
Policy = Who + What + Which Resource + (Optional: Conditions)
```

**AWS IAM Policy (JSON):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::123456789012:user/alice" },
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::company-reports",
        "arn:aws:s3:::company-reports/*"
      ],
      "Condition": {
        "Bool": { "aws:MultiFactorAuthPresent": "true" }
      }
    }
  ]
}
```

**Key elements:**
- **Principal (Who):** The identity the policy applies to
- **Action (What):** The operations allowed or denied
- **Resource (Which):** The specific resources the actions apply to
- **Effect:** Allow or Deny
- **Condition (Optional):** Additional requirements (MFA, time, IP, etc.)

### Implicit Deny vs Explicit Deny

| Rule | Behavior |
|------|----------|
| **Implicit deny** | If no policy explicitly allows an action, it is denied |
| **Explicit allow** | A policy must explicitly grant permission |
| **Explicit deny** | A Deny policy overrides all Allow policies |

**Order of evaluation:**
1. Check for explicit Deny → If found, deny immediately
2. Check for explicit Allow → If found, allow
3. If neither, implicitly deny

This means a single Deny can block access even if multiple Allows exist.

### AWS IAM Specifics

| Concept | Description |
|---------|-------------|
| **IAM Policy** | JSON document defining permissions |
| **IAM Role** | Set of permissions assumable by users or services |
| **IAM User** | Individual human identity |
| **IAM Group** | Collection of users with shared policies |
| **ARN** | Amazon Resource Name — unique identifier for all AWS resources |
| **Trust Policy** | Defines who can assume a role |
| **Permissions Policy** | Defines what the role can do |
| **Policy Evaluation** | AWS evaluates all applicable policies; explicit deny wins |

**AWS Best Practices:**
- Use roles instead of long-term access keys
- Enable MFA for root account and privileged users
- Use IAM Access Analyzer to identify unintended access
- Rotate credentials regularly
- Use AWS Organizations for multi-account governance

### Azure RBAC Specifics

| Concept | Description |
|---------|-------------|
| **Azure AD** | Identity and access management for Azure |
| **Management Group** | Container for subscriptions with inherited policies |
| **Subscription** | Billing and resource boundary |
| **Resource Group** | Logical container for related resources |
| **Role Assignment** | Links role definition + security principal + scope |
| **Role Definition** | Set of permissions (e.g., Contributor, Reader) |
| **Built-in Roles** | Predefined roles (Owner, Contributor, Reader, User Access Administrator) |
| **Custom Roles** | Organization-defined roles with specific permissions |

**Azure RBAC scope hierarchy:**
```
Management Group
    └── Subscription
            └── Resource Group
                    └── Resource
```

Access granted at a higher scope is inherited by lower scopes.

### GCP IAM Specifics

| Concept | Description |
|---------|-------------|
| **Organization** | Top-level resource for enterprise GCP |
| **Folder** | Optional grouping for projects |
| **Project** | Primary resource container (like AWS account) |
| **Resource** | Individual service instance |
| **Member** | Identity (user, service account, group, domain) |
| **Role** | Collection of permissions |
| **Policy** | Binds members to roles at a resource level |
| **Predefined Roles** | Google-managed (e.g., roles/storage.objectViewer) |
| **Custom Roles** | Organization-defined |

**GCP IAM Policy structure:**
```
bindings:
  - role: roles/storage.objectViewer
    members:
      - user:alice@company.com
      - serviceAccount:app@project.iam.gserviceaccount.com
  - role: roles/storage.objectAdmin
    members:
      - group:admins@company.com
```

---

## How It Works

### Cross-Account Access (AWS)

AWS allows one account to access resources in another:

```
Account A (Development)          Account B (Production)
    │                                   │
    │ Assume Role in Account B          │
    │──────────────────────────────────→│
    │                                   │
    │ Temporary credentials returned    │
    │←──────────────────────────────────│
    │                                   │
    │ Access S3 bucket in Account B     │
    │ (with Account B's permissions)    │
```

**Benefits:**
- No shared credentials
- Temporary access with automatic expiration
- Audit trail of cross-account access
- Different security policies per account

### Workload Identity

Instead of storing long-lived credentials, workloads use workload identity:

**AWS IAM Roles for Service Accounts (IRSA):**
- Kubernetes service account mapped to IAM role
- No AWS credentials stored in pods
- Short-lived tokens via OIDC

**Azure Managed Identities:**
- System-assigned: Tied to a specific Azure resource
- User-assigned: Shared across multiple resources
- No credentials in code; Azure handles token acquisition

**GCP Workload Identity:**
- Kubernetes service account linked to GCP service account
- Automatic credential injection
- No service account keys to manage

### Cloud IAM Policy Evaluation

```
User requests action on resource
           │
           ▼
    ┌─────────────────┐
    │ Gather all      │
    │ policies that   │
    │ apply to user   │
    │ and resource    │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │ Check for       │
    │ Explicit DENY   │
    └────────┬────────┘
        Yes  │   │ No
            ▼   ▼
    ┌──────────┐  ┌─────────────────┐
    │  DENY    │  │ Check for       │
    │  Access  │  │ Explicit ALLOW  │
    └──────────┘  └────────┬────────┘
                      Yes  │   │ No
                          ▼   ▼
                   ┌──────────┐  ┌──────────┐
                   │  ALLOW   │  │  DENY    │
                   │  Access  │  │  Access  │
                   └──────────┘  │(Implicit)│
                                 └──────────┘
```

---

## Where You See It

| Product | Platform | Use Case |
|---------|----------|----------|
| **AWS IAM** | AWS | Identity and access for all AWS services |
| **Azure RBAC** | Azure | Resource-level access control |
| **Google Cloud IAM** | GCP | Permission management across GCP services |
| **AWS Organizations** | AWS | Multi-account governance and SCPs |
| **Azure Policy** | Azure | Enforce organizational standards |
| **GCP Organization Policies** | GCP | Constraint enforcement |
| **IAM Access Analyzer** | AWS | Identify unintended external access |
| **Microsoft Defender for Cloud** | Azure | Cloud security posture management |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Root account access keys are acceptable for daily use" | Root credentials should never be used routinely. Create IAM users/roles with least privilege. |
| "Cloud IAM policies are the same across providers" | Each provider has different syntax, concepts, and evaluation logic. Skills are partially transferable but not identical. |
| "If I don't set a policy, access is open" | All cloud providers default to implicit deny. No policy = no access. |
| "Service accounts are safe because they're not human" | Service accounts often have excessive permissions and long-lived credentials. They require the same governance as human accounts. |
| "One account is enough" | Multi-account strategies improve security, blast radius containment, and billing separation. |

---

## How to Practice

### Exercise 1: Analyze an AWS IAM Policy
Given this policy, answer:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": "s3:DeleteBucket",
      "Resource": "*"
    }
  ]
}
```
- What can the user do?
- What can they NOT do?
- Is this policy well-designed? What are the risks?
- How would you improve it?

### Exercise 2: Design Azure RBAC for a Team
A team needs:
- 2 developers who can deploy to staging
- 1 lead who can deploy to production
- 1 DBA who can manage databases but not delete resources
- 1 auditor who can read everything but change nothing

Design the Azure RBAC assignments using built-in and custom roles.

### Exercise 3: Cloud IAM Comparison
Create a comparison table for AWS, Azure, and GCP covering:
- User identity types
- Service account equivalents
- Policy language (JSON, YAML, etc.)
- Default behavior (implicit deny)
- Cross-account/project access
- MFA enforcement

### Exercise 4: Run the Simulations
- `cloud_policy_sim.py` — Cloud IAM policy evaluation
- `least_privilege_analyzer.py` — Detect over-permissive policies
- `cross_cloud_mapper.py` — Compare IAM across providers

---

## Projects

### `cloud_policy_sim.py`
Simulates cloud IAM policy evaluation:
- Supports AWS, Azure, and GCP-style policies
- Evaluates allow/deny decisions
- Handles policy conditions
- Detects conflicting policies
- Recommends least-privilege adjustments

### `least_privilege_analyzer.py`
Analyzes cloud permissions for least privilege:
- Scans policy documents
- Identifies wildcard permissions (*)
- Detects unused permissions through log analysis
- Recommends specific actions instead of broad access
- Generates tightened policy alternatives

### `cross_cloud_mapper.py`
Maps IAM concepts across AWS, Azure, and GCP:
- Equivalent terms and concepts
- Policy structure comparison
- Role/permission mapping
- Migration considerations
- Best practices per provider

---

## Cloud IAM in Practice: Multi-Cloud Reality

### Cloud IAM Is Native — Not COTS in the Traditional Sense

Unlike PAM or IGA where you buy a product, **cloud IAM is built into each cloud platform**. You do not install AWS IAM or Azure RBAC — they are part of the platform.

**However, multi-cloud tools exist:**

| Tool Type | Products | Purpose |
|-----------|----------|---------|
| **Cloud Identity Platforms** | Okta, Azure AD, Ping Identity | Single identity across multiple clouds |
| **Cloud Security Posture Management (CSPM)** | Prisma Cloud, Dome9, Orca Security | Detect IAM misconfigurations across clouds |
| **Cloud Infrastructure Entitlement Management (CIEM)** | Cyral, Sonrai Security, Britive | Manage entitlements across AWS, Azure, GCP |
| **Multi-Cloud Policy Engines** | HashiCorp Sentinel, Open Policy Agent (OPA) | Enforce policies across cloud providers |

### Cloud IAM Career Tracks

**Cloud IAM Support:**
- Reset cloud console access
- Troubleshoot role assumption failures
- Investigate access denied errors
- Monitor for public S3 buckets or over-permissive policies
- Respond to cloud security alerts

**Cloud IAM Implementation:**
- Design multi-account strategy
- Implement SCPs (Service Control Policies) or Organization Policies
- Configure cross-account access and federation
- Deploy CIEM tools for visibility
- Set up automated policy scanning

**Cloud IAM Development:**
- Build Infrastructure as Code (Terraform, CloudFormation) for IAM
- Develop custom policy scanning tools
- Build automated remediation workflows
- Integrate cloud IAM with corporate IdP

**Cloud IAM is the fastest-growing IAM specialty** because:
- Every company moving to cloud needs cloud IAM expertise
- Cloud IAM skills are transferable across employers
- Certifications (AWS Security, Azure Security Engineer, GCP Professional Cloud Architect) are highly valued
- Demand exceeds supply — cloud IAM engineers command premium salaries

---

## Check Your Understanding

1. What is the difference between a Principal, Action, Resource, and Condition in an IAM policy? Give an example of each.
2. How does implicit deny work in cloud IAM? If a user has an Allow policy for S3 and no Deny policy, can they access S3? What if they have an explicit Deny?
3. Compare IAM Users, IAM Roles, and Service Accounts in AWS. When would you use each?
4. Why are long-lived access keys risky? What alternatives exist (roles, managed identities, workload identity)?
5. Design an AWS multi-account strategy for an organization with: development, staging, production, and shared services. How would you structure IAM across these accounts?
6. What is the Azure RBAC scope hierarchy? How does access at the Management Group level affect resources in a Subscription?
7. Compare GCP's IAM binding model with AWS's policy-based model. What are the advantages of each approach?
8. A developer created an S3 bucket with public read access "for testing" and forgot about it. What cloud IAM tools and practices would prevent or detect this?
9. An organization's cloud audit reveals 500 IAM users with access keys, but only 50 are actively used. What remediation steps should be taken?
10. Design a cross-cloud IAM strategy for a company using AWS for compute, Azure for databases, and GCP for analytics. How would you manage identities consistently?
