# 4. Authorization Models and Access Control

## What Is Authorization?

**Authorization** is the process of determining what actions an authenticated identity is permitted to perform on which resources.

If authentication answers "Who are you?", authorization answers "What are you allowed to do?"

When you try to open a file, access a database, or view an admin panel, authorization is the check that happens after you have already proven your identity. A failed authorization results in "Access Denied" — not "Invalid Password."

---

## Why Learn This?

Every application, operating system, and cloud platform implements some form of authorization. Misconfigured authorization is one of the leading causes of security breaches. Understanding the models, their tradeoffs, and their failure modes enables you to:
- Design secure applications
- Audit existing systems for over-permissioning
- Choose the right model for your organization's needs
- Understand compliance requirements

---

## Core Concepts

### Authentication vs Authorization

| Aspect | Authentication | Authorization |
|--------|---------------|---------------|
| Question | "Who are you?" | "What can you do?" |
| Process | Verifying identity | Granting or denying permissions |
| Failure message | "Invalid credentials" | "Access denied" |
| Analogy | Showing your passport at immigration | Your visa stamp determining where you can go |

**Why the distinction matters:** A system can authenticate you perfectly and still authorize you incorrectly. Being logged in does not mean you should have admin access.

### Access Control Models

#### Discretionary Access Control (DAC)

In DAC, the **owner of a resource decides who can access it**.

- **Example:** In Google Drive, you own a document and choose who can view, comment, or edit it.
- **Strength:** Flexible and intuitive
- **Weakness:** Owners can grant access to the wrong people; privilege escalation is possible
- **Common in:** File systems (Unix permissions, Windows ACLs), cloud storage

#### Mandatory Access Control (MAC)

In MAC, **system-enforced policies control access based on security labels**. Users cannot override these policies.

- **Example:** Military documents labeled "Top Secret," "Secret," or "Confidential." A general cannot unilaterally share a Top Secret document with a Private.
- **Strength:** Tamper-proof, highly secure
- **Weakness:** Rigid, complex to administer
- **Common in:** Government, military, SELinux

#### Role-Based Access Control (RBAC)

In RBAC, **permissions are assigned to roles, and users are assigned to roles**.

- **Example:** In a hospital, the "Doctor" role can view patient records and prescribe medication. The "Nurse" role can view records and administer medication. The "Receptionist" role can schedule appointments but cannot view medical records.
- **Strength:** Scales well; aligns with organizational structure
- **Weakness:** Can lead to "role explosion" in complex organizations
- **Common in:** Enterprise applications, databases, cloud platforms

#### Attribute-Based Access Control (ABAC)

In ABAC, **access decisions are based on attributes of the user, resource, action, and environment**.

- **Example:** "Allow access IF user.department == resource.department AND time.hour >= 9 AND time.hour <= 17 AND device.managed == true"
- **Strength:** Highly flexible and dynamic
- **Weakness:** Complex to design, debug, and audit
- **Common in:** Cloud IAM policies, XACML implementations

#### Policy-Based Access Control (PBAC)

PBAC uses a **centralized policy engine** that evaluates all access decisions, often combining RBAC and ABAC concepts.

- **Common in:** Enterprise IAM platforms like Okta, Azure AD, SailPoint

### Model Comparison

| Model | Decided By | Flexibility | Complexity | Best For |
|-------|-----------|-------------|------------|----------|
| DAC | Resource owner | High | Low | Personal files, collaboration |
| MAC | System administrator | None | High | Military, high-security environments |
| RBAC | Role assignments | Medium | Medium | Most organizations |
| ABAC | Dynamic attributes | Very high | High | Complex, changing environments |
| PBAC | Centralized policies | High | Very high | Large enterprises |

### Access Control Structures

**Access Control Matrix:**
A theoretical table showing every user's permissions on every resource. In practice, these matrices are enormous and mostly empty.

**Access Control List (ACL):**
Permissions stored with the resource. Efficient for asking "Who can access this file?" Inefficient for asking "What can Alice access?"

**Capability List:**
Permissions stored with the user. Efficient for asking "What can Alice access?" Inefficient for asking "Who can access this file?"

Most real systems use a **hybrid approach**: users are assigned to groups/roles, and resources reference those groups in their ACLs.

---

## How It Works

### How Operating Systems Evaluate Access

When a process tries to open a file on Linux:
1. The kernel identifies the user and group ownership of the process
2. It checks the file's permission bits (read, write, execute) for owner, group, and others
3. It applies the most specific match (owner > group > others)
4. If the permission is granted, the operation proceeds; otherwise, `EACCES` (permission denied) is returned

Windows uses **ACLs** stored as metadata on each file, allowing much more granular control than Unix permissions.

### How Databases Enforce Authorization

```sql
-- PostgreSQL example
CREATE ROLE analyst;
GRANT SELECT ON sales_data TO analyst;
GRANT analyst TO alice;  -- Alice gets all analyst permissions
```

The database maintains an internal ACL for each table. When Alice queries `sales_data`, the query planner checks whether the `analyst` role (which Alice holds) has `SELECT` permission.

### How Cloud IAM Policies Work

Cloud platforms like AWS use JSON policies that combine RBAC and ABAC:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::company-bucket/*",
  "Condition": {
    "StringEquals": {"aws:RequestedRegion": "us-east-1"},
    "IpAddress": {"aws:SourceIp": "203.0.113.0/24"}
  }
}
```

**Evaluation logic:**
1. Is there an explicit `Deny`? → If yes, deny immediately
2. Is there an explicit `Allow`? → If yes, allow
3. If neither, deny by default (implicit deny)

---

## Where You See It

| System | Model | How You Interact With It |
|--------|-------|-------------------------|
| **Linux file permissions** | DAC | `chmod`, `chown`, `ls -l` |
| **Windows NTFS ACLs** | DAC | File Properties → Security tab |
| **PostgreSQL / MySQL** | RBAC | `GRANT`, `REVOKE`, roles |
| **AWS IAM** | RBAC + ABAC | JSON policies, roles, groups |
| **Azure RBAC** | RBAC | Role assignments on subscriptions |
| **Kubernetes RBAC** | RBAC | Roles, RoleBindings, ClusterRoles |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Authentication is enough" | Being logged in does not mean you should have access to everything |
| "RBAC and ABAC are competitors" | Most modern systems use both: RBAC for coarse-grained, ABAC for fine-grained |
| "Deny is the default in all systems" | Some legacy systems default to allow; modern systems (cloud IAM) default to deny |
| "ACLs are always stored with resources" | Capability lists store permissions with users; most systems use a hybrid |

---

## How to Practice

1. **Inspect file permissions on your computer**
   - Linux/macOS: Run `ls -la` and interpret the permission bits
   - Windows: Check file Properties → Security → Advanced
   - Identify who has access and whether it follows least privilege

2. **Design an authorization model for a small company**
   - 10 employees across Engineering, Sales, and Finance
   - Resources: code repository, CRM, financial system, shared drive
   - Choose DAC, RBAC, or ABAC and justify your decision

3. **Run the simulations**
   - `access_matrix_visualizer.py` shows how permissions are structured
   - `authorization_engine.py` lets you switch between DAC, RBAC, and ABAC

---

## Projects

### `access_matrix_visualizer.py`
Creates and visualizes access control matrices:
- Defines users, resources, and permissions
- Generates ACL and capability list views
- Checks for privilege escalation paths
- Validates Separation of Duties constraints

### `authorization_engine.py`
Implements a pluggable authorization engine:
- Supports DAC, RBAC, and ABAC modes
- Evaluates access requests against policies
- Logs all access decisions for audit
- Demonstrates policy conflict resolution

### `policy_conflict_detector.py`
Analyzes authorization policies for conflicts:
- Detects overlapping permissions
- Identifies implicit grants that violate SoD
- Finds redundant policies
- Suggests policy optimization

---

## Check Your Understanding

1. What is the key difference between DAC and MAC? Give a real-world example of each.
2. How does RBAC simplify administration compared to managing individual user permissions?
3. Give an example of an ABAC policy that uses environmental attributes (time, location, etc.).
4. What is Static Separation of Duties? How does it differ from Dynamic SoD?
5. Why might an organization migrate from RBAC to ABAC? What are the trade-offs?
6. Explain the difference between an Access Control List (ACL) and a Capability List.
