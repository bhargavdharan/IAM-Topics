# 14. Cloud IAM

## What Is Cloud IAM?

**Cloud IAM** is the identity and access management system built into cloud platforms (AWS, Azure, Google Cloud). It governs who can do what on which cloud resources.

While the principles of IAM are universal, cloud IAM has unique characteristics: resources are ephemeral, scale is massive, everything is API-driven, and infrastructure is shared across tenants.

---

## Why Learn This?

Cloud misconfiguration is a leading cause of data breaches. Understanding cloud IAM enables you to:
- Secure cloud resources effectively
- Implement least privilege in dynamic environments
- Audit cross-cloud permissions
- Pass cloud security assessments

---

## Core Concepts

### Cloud Identity Types

| Identity Type | AWS | Azure | GCP | Description |
|--------------|-----|-------|-----|-------------|
| **Human User** | IAM User | Entra ID User | Google Account | Person logging into console |
| **Group** | IAM Group | Entra ID Group | Google Group | Collection of users |
| **Role** | IAM Role | Azure Role | IAM Role | Temporary permission set |
| **Service Account** | IAM Role/User | Managed Identity | Service Account | Identity for applications |
| **Federated User** | IAM Identity Center | Entra ID Federation | Cloud Identity | External identity provider |

### Cloud IAM Policy Evaluation

When a user tries to access a cloud resource:
1. Is there an explicit **DENY**? → If yes, DENY
2. Is there an explicit **ALLOW**? → If yes, ALLOW
3. If neither → **DENY** (default deny)

**This "default deny" is critical.** If no policy explicitly allows an action, it is denied.

### AWS IAM Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "AllowS3Read",
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::company-data-bucket", "arn:aws:s3:::company-data-bucket/*"],
    "Condition": {
      "StringEquals": {"aws:RequestedRegion": "us-east-1"},
      "IpAddress": {"aws:SourceIp": "203.0.113.0/24"}
    }
  }]
}
```

| Element | Purpose |
|---------|---------|
| **Effect** | Allow or Deny |
| **Action** | What operation is permitted |
| **Resource** | What resource the action applies to |
| **Condition** | Optional constraints (time, IP, tags) |

### Cross-Cloud Comparison

| Feature | AWS IAM | Azure RBAC | GCP IAM |
|---------|---------|-----------|---------|
| Policy format | JSON | JSON | JSON/YAML |
| Inheritance | Identity + Resource-based | Subscription → RG → Resource | Organization → Folder → Project → Resource |
| Temporary access | IAM Roles (STS) | PIM | Service account impersonation |

---

## How It Works

### AWS STS (Security Token Service)

STS enables temporary credentials:
```python
# Assume a role for temporary access
sts.assume_role(
    RoleArn='arn:aws:iam::123456789:role/ReadOnlyRole',
    RoleSessionName='AliceSession',
    DurationSeconds=3600  # 1 hour
)
```

**Why temporary credentials are safer:**
- No long-lived access keys to leak
- Automatic expiration
- Every session is logged
- Can be revoked immediately

### Azure PIM (Privileged Identity Management)

- Roles are "eligible" but not "active" by default
- User must activate the role (with approval if configured)
- Activation is time-limited (e.g., 4 hours)
- Requires MFA to activate
- Every activation is audited

### GCP IAM and Resource Hierarchy

```
Organization (example.com)
└── Folder (Engineering)
    └── Project (production-api)
        └── Resources (VMs, buckets, etc.)
```

Permissions granted at the Organization level apply to ALL resources below.

---

## Where You See It

| Product | IAM Feature |
|---------|------------|
| **AWS IAM** | Policies, roles, users, groups |
| **Azure RBAC** | Role assignments, PIM |
| **Google Cloud IAM** | Organization policies, custom roles |
| **Terraform** | Infrastructure-as-code for IAM |
| **Pulumi** | Programmatic cloud IAM management |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Root account is fine for daily use" | Root should never be used for daily operations |
| "Wildcards make administration easier" | `*` in policies violates least privilege |
| "Hardcoded keys in code are acceptable" | Use IAM roles and instance profiles instead |
| "Cloud IAM is separate from corporate IAM" | Most organizations federate corporate identity into cloud IAM |

---

## How to Practice

1. **Analyze an IAM policy**
   - Write a policy that allows read access to one S3 bucket
   - Add a condition that restricts access to a specific IP range
   - Verify that access to other buckets is denied

2. **Compare temporary vs long-lived credentials**
   - List the risks of access keys stored in code
   - Document the benefits of IAM role assumption

3. **Run the simulations**
   - `cloud_policy_sim.py` evaluates cloud IAM policies
   - `least_privilege_analyzer.py` suggests policy improvements

---

## Projects

### `cloud_policy_sim.py`
Simulates cloud IAM policy evaluation:
- Parses AWS-style IAM policies
- Evaluates access requests
- Handles explicit deny, allow, and implicit deny
- Supports conditions

### `least_privilege_analyzer.py`
Analyzes cloud permissions:
- Identifies unused permissions from logs
- Detects overly permissive wildcards
- Generates least-privilege recommendations

### `service_account_auditor.py`
Audits service accounts:
- Lists all service accounts
- Identifies excessive permissions
- Finds unused or stale accounts

---

## Check Your Understanding

1. How is Cloud IAM different from on-premises IAM? Name three key differences.
2. What is "default deny" in cloud IAM policy evaluation?
3. Why are temporary credentials (like AWS STS) more secure than long-lived access keys?
4. What is Azure PIM and how does it enforce just-in-time access?
5. Name three Cloud IAM anti-patterns and how to fix each.
