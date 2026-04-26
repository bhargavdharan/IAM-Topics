# 4. Authorization Models and Access Control

## What Is Authorization?

**Authorization** is the process of determining whether an authenticated identity is permitted to perform a specific action on a specific resource.

If authentication answers the question "Who are you?", authorization answers the question "What are you allowed to do?"

When you attempt to open a file, access a database, view an admin panel, or call an API endpoint, authorization is the security check that occurs after your identity has already been verified. A failed authorization results in "Access Denied" — fundamentally different from an authentication failure which results in "Invalid Password" or "User Not Found."

Understanding authorization is critical because misconfigured authorization is one of the leading causes of data breaches, insider threats, and compliance failures.

---

## Why Learn This?

Every application, operating system, database, and cloud platform implements some form of authorization. Without proper authorization controls:
- Users can access data they should not see
- Insiders can modify or delete critical resources
- Applications can perform operations beyond their intended scope
- Auditors cannot verify compliance with regulatory requirements

Understanding authorization models enables you to:
- Design secure access architectures
- Audit existing systems for over-permissioning
- Select the appropriate model for your organization's needs
- Implement and troubleshoot access control policies

---

## Core Concepts

### Authentication vs Authorization

| Aspect | Authentication | Authorization |
|--------|---------------|---------------|
| Question answered | "Who are you?" | "What can you do?" |
| Process | Verifying identity credentials | Evaluating permissions against policies |
| Failure message | "Invalid credentials" / "User not found" | "Access denied" / "Forbidden" |
| Timing | First step in access control | Second step, after authentication succeeds |
| Analogy | Airport security checks your passport | Your visa stamp determines which countries you can enter |

**Why the distinction matters:** A system can authenticate you perfectly and still authorize you incorrectly. Being logged in does not mean you should have administrative access. Many security vulnerabilities arise from conflating these two steps — assuming that authenticated users are automatically trusted with all resources.

### Access Control Models

#### Discretionary Access Control (DAC)

In DAC, the **owner of a resource has discretion to decide who can access it** and what permissions they receive.

**How it works:**
- Alice creates a document and becomes its owner
- Alice decides that Bob can read and comment, Charlie can edit, and Diana cannot access it at all
- Alice can transfer ownership or revoke access at any time
- The system enforces Alice's decisions but does not override them

**Real-world examples:**
- Google Drive file sharing
- Unix/Linux file permissions (owner, group, others)
- Windows NTFS ACLs
- Social media privacy settings

**Strengths:**
- Flexible and intuitive — mirrors how people naturally share things
- Easy to understand and implement
- Users have control over their own resources

**Weaknesses:**
- Owners can make mistakes — granting access to the wrong person
- No centralized oversight — administrators cannot easily audit all sharing decisions
- Privilege escalation is possible — if Bob has access to Alice's file, and Alice's file contains a link to Charlie's restricted file, Bob might gain indirect access
- Does not scale well in large organizations

**When to use:** Small teams, personal file sharing, collaborative environments where resource owners need fine-grained control.

#### Mandatory Access Control (MAC)

In MAC, **system-enforced policies based on security labels control access**. Users cannot override these policies, even if they own the resource.

**How it works:**
- Every resource is assigned a security label (e.g., "Top Secret", "Secret", "Confidential", "Unclassified")
- Every user is assigned a clearance level
- The system enforces strict rules: a user can only access resources at or below their clearance level
- Even the CEO cannot read a "Top Secret" document if their clearance is only "Secret"

**Real-world examples:**
- Military and government classification systems
- SELinux (Security-Enhanced Linux)
- Bell-LaPadula confidentiality model
- Compartmented security systems

**Strengths:**
- Tamper-proof — users cannot bypass policies
- Highly secure — suitable for classified environments
- Centralized control — security administrators set all policies

**Weaknesses:**
- Extremely rigid — cannot accommodate exceptions
- Complex to administer — requires constant label management
- Poor usability — users frequently encounter access blocks for legitimate work
- Expensive to implement and maintain

**When to use:** Military, government intelligence, classified research, high-security environments where flexibility is less important than absolute control.

#### Role-Based Access Control (RBAC)

In RBAC, **permissions are assigned to roles, and users are assigned to roles** based on their job functions.

**How it works:**
- The organization defines roles: "Doctor", "Nurse", "Billing Specialist", "Admin"
- Each role is granted a set of permissions:
  - Doctor: read patient records, write prescriptions, view lab results
  - Nurse: read patient records, administer medication, update vitals
  - Billing Specialist: read billing information, process insurance claims
  - Admin: manage user accounts, configure system settings
- When Alice joins as a Doctor, she is assigned to the "Doctor" role
- Alice automatically receives all Doctor permissions
- If the Doctor role is updated, all Doctors receive the change

**Real-world examples:**
- Hospital information systems
- Enterprise resource planning (ERP) systems
- Database management systems (PostgreSQL, Oracle)
- Cloud IAM (AWS IAM roles, Azure RBAC)

**Strengths:**
- Scales well — roles match organizational structure
- Simplifies administration — update one role, affect all members
- Supports audit and compliance — easy to report "Who has the Admin role?"
- Aligns with business functions — intuitive for managers

**Weaknesses:**
- Role explosion — in complex organizations, the number of roles can become unmanageable
- Static — roles do not easily adapt to context (time, location, device)
- Granularity trade-off — too coarse violates least privilege; too fine creates complexity

**When to use:** Medium to large organizations with stable job functions. The most widely used model in enterprise environments.

#### Attribute-Based Access Control (ABAC)

In ABAC, **access decisions are based on attributes of the user, resource, action, and environment**.

**How it works:**
- Policies are expressed as Boolean rules using attributes:
  ```
  ALLOW IF user.department == resource.department
         AND user.level >= "manager"
         AND environment.time >= 09:00
         AND environment.time <= 17:00
         AND device.managed == true
  ```
- Every access request is evaluated against all applicable policies
- The decision is dynamic — it can change based on context

**Real-world examples:**
- AWS IAM policies with conditions
- Azure AD Conditional Access
- Google Cloud IAM conditions
- XACML (eXtensible Access Control Markup Language) implementations

**Strengths:**
- Highly flexible — adapts to any context
- Dynamic — can enforce time-based, location-based, or device-based rules
- Fine-grained — can express complex policies that RBAC cannot

**Weaknesses:**
- Complex to design — policies can become difficult to understand and debug
- Harder to audit — "Why was Alice denied?" requires evaluating all attributes
- Performance overhead — evaluating attributes takes longer than role lookups

**When to use:** Complex environments where context matters: remote work, multi-tenant systems, cloud platforms, or any situation where static roles are insufficient.

#### Policy-Based Access Control (PBAC)

PBAC uses a **centralized policy engine** that evaluates all access decisions. PBAC often combines RBAC and ABAC concepts into a unified policy framework.

**Real-world examples:**
- Enterprise IAM platforms (Okta, SailPoint, ForgeRock)
- Cloud policy engines (AWS Organizations SCPs, Azure Policy)
- Unified policy management systems

### Model Comparison Summary

| Model | Control | Flexibility | Complexity | Scalability | Best For |
|-------|---------|-------------|------------|-------------|----------|
| DAC | Owner decides | High | Low | Poor | Small teams, collaboration |
| MAC | System enforces | None | High | Medium | Military, classified data |
| RBAC | Role-based | Medium | Medium | High | Most enterprises |
| ABAC | Attribute-based | Very High | High | Medium | Dynamic, cloud, complex |
| PBAC | Centralized engine | High | Very High | High | Large enterprises |

### Access Control Structures

**Access Control Matrix:**
A theoretical table showing every user's permissions on every resource. While conceptually simple, these matrices are enormous and mostly empty (sparse) in practice.

```
          File_A  File_B  File_C  Printer
Alice     rw      r       -       print
Bob       r       rw      r       -
Charlie   -       -       rw      print
```

**Access Control List (ACL):**
Permissions stored with the resource.
- Efficient for: "Who can access this file?"
- Inefficient for: "What can Alice access?"
- Example: `File_A: Alice(rw), Bob(r)`

**Capability List:**
Permissions stored with the user.
- Efficient for: "What can Alice access?"
- Inefficient for: "Who can access this file?"
- Example: `Alice: File_A(rw), File_B(r), Printer(print)`

**Hybrid approach (used in practice):**
Most real systems combine approaches:
1. Users are assigned to groups/roles (RBAC)
2. Groups are referenced in resource ACLs
3. This provides efficiency for both "who can access this?" and "what can Alice access?"

---

## How It Works

### How Operating Systems Evaluate Access

**Unix/Linux permission model (simplified DAC):**
Every file has three permission sets:
- Owner permissions (rwx)
- Group permissions (rwx)
- Others permissions (rwx)

When Alice tries to read `/home/alice/report.txt`:
1. Kernel checks if Alice is the owner → if yes, apply owner permissions
2. If not owner, check if Alice is in the file's group → if yes, apply group permissions
3. If neither, apply others permissions
4. If read permission is present, allow; otherwise return `EACCES` (Permission Denied)

**Windows NTFS ACLs (richer DAC):**
- Each file has a list of Access Control Entries (ACEs)
- Each ACE specifies: user or group, allowed/denied, specific permissions
- Permissions are granular: Read, Write, Execute, Delete, Change Permissions, Take Ownership
- ACEs are evaluated in order; explicit Deny overrides Allow

### How Databases Enforce Authorization

```sql
-- PostgreSQL role-based authorization
CREATE ROLE analyst;
GRANT SELECT ON sales_data TO analyst;
GRANT INSERT ON sales_data TO analyst;
GRANT analyst TO alice;  -- Alice gets all analyst permissions

-- When Alice runs:
SELECT * FROM sales_data;
-- PostgreSQL checks: Does Alice (or any role Alice holds) have SELECT on sales_data?
-- If yes, execute; if no, return "permission denied"
```

### How Cloud IAM Policies Work

Cloud platforms use JSON policies that combine RBAC and ABAC:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::company-data-bucket/*"],
      "Condition": {
        "StringEquals": {"aws:RequestedRegion": "us-east-1"},
        "IpAddress": {"aws:SourceIp": "203.0.113.0/24"},
        "Bool": {"aws:MultiFactorAuthPresent": "true"}
      }
    }
  ]
}
```

**Policy evaluation logic:**
1. Collect all policies that apply to the principal (user/role)
2. Check for any explicit `Deny` statements that match the request
3. If any `Deny` matches → **DENY** (deny always wins)
4. Check for any explicit `Allow` statements that match
5. If any `Allow` matches → **ALLOW**
6. If no policy matches → **DENY** (default deny)

**Why default deny is critical:** In cloud environments, resources are created constantly. If the default were "allow," every new resource would be publicly accessible until someone explicitly locked it down. Default deny ensures that access must be explicitly granted.

---

## Where You See It

| System | Model | How You Interact |
|--------|-------|-----------------|
| **Linux/Unix** | DAC | `chmod 755 file`, `chown user:group file` |
| **Windows NTFS** | DAC | File Properties → Security → Permissions |
| **PostgreSQL** | RBAC | `CREATE ROLE`, `GRANT`, `REVOKE` |
| **AWS IAM** | RBAC + ABAC | JSON policies, roles, groups, conditions |
| **Azure RBAC** | RBAC | Role assignments at subscription/resource group/resource level |
| **Kubernetes** | RBAC | Roles, RoleBindings, ClusterRoles |
| **Google Drive** | DAC | Share button, permission levels |
| **SELinux** | MAC | Security contexts, policies, enforcement modes |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Authentication is enough security" | Being logged in does not mean you should have access to everything. Authorization is the second critical gate. |
| "RBAC and ABAC are competitors" | Most modern systems use both: RBAC for coarse-grained job functions, ABAC for fine-grained contextual constraints |
| "Deny is the default everywhere" | Some legacy systems default to allow. Modern cloud IAM uses default deny. Always verify your platform's behavior. |
| "ACLs are always stored with resources" | Capability lists store permissions with users. Most systems use a hybrid approach. |
| "MAC is just strict RBAC" | MAC uses security labels and mandatory system enforcement; users cannot override it. RBAC is discretionary at the role level. |
| "Authorization is a one-time check" | Modern systems evaluate authorization continuously — on every API call, every page load, every resource access. |

---

## How to Practice

### Exercise 1: Inspect File Permissions
**Linux/macOS:**
1. Open a terminal
2. Run `ls -la` in any directory
3. Interpret the permission string: `drwxr-xr-x`
   - `d` = directory
   - `rwx` = owner permissions (read, write, execute)
   - `r-x` = group permissions (read, execute)
   - `r-x` = others permissions (read, execute)
4. Run `ls -la /etc/shadow` — observe that only root can read it
5. Run `id` to see your user ID and group memberships

**Windows:**
1. Right-click any file → Properties → Security tab
2. Click Advanced to see the full ACL
3. Identify each ACE: who, what permission, allow or deny
4. Observe inheritance from parent folders

### Exercise 2: Design an Authorization Model
Design an authorization model for a 10-person company with three departments:
- **Engineering:** needs access to code repository, staging environment, documentation
- **Finance:** needs access to accounting system, payroll, financial reports
- **HR:** needs access to employee records, payroll (view-only), benefits system

Requirements:
- Engineers should not access financial data
- Finance should not access code
- HR should view payroll but not modify it
- The CEO needs read access to everything
- A contractor needs temporary access to documentation only

Choose DAC, RBAC, or ABAC and justify your decision. Define roles, permissions, and any constraints.

### Exercise 3: Run the Simulations
- `access_matrix_visualizer.py` — Explore matrix, ACL, and capability views
- `authorization_engine.py` — Switch between DAC, RBAC, and ABAC modes

---

## Projects

### `access_matrix_visualizer.py`
Creates and visualizes access control matrices:
- Defines users, resources, and permissions
- Generates ACL view (permissions per resource)
- Generates capability list view (permissions per user)
- Checks for privilege escalation paths
- Validates Separation of Duties constraints

### `authorization_engine.py`
Pluggable authorization engine supporting three modes:
- **DAC mode:** Resource owners grant access
- **RBAC mode:** Role-based permission evaluation with inheritance
- **ABAC mode:** Dynamic policy evaluation with attributes
- Evaluates access requests and logs decisions
- Demonstrates policy conflict resolution

### `policy_conflict_detector.py`
Analyzes authorization policies:
- Detects overlapping permissions
- Identifies implicit grants that violate SoD
- Finds redundant policies
- Suggests policy optimization

---

## Check Your Understanding

1. What is the fundamental difference between DAC and MAC? Give a real-world example where each would be appropriate.
2. How does RBAC simplify administration compared to managing individual user permissions? What problem does role explosion create?
3. Write an ABAC policy that allows access to financial reports only during business hours, from corporate devices, by users in the Finance department with Manager level or above.
4. What is Static Separation of Duties? How does it differ from Dynamic SoD? Give an example where each would be necessary.
5. Why might an organization use RBAC for coarse-grained access and ABAC for fine-grained constraints? What are the trade-offs of this hybrid approach?
6. Explain the difference between an Access Control List (ACL) and a Capability List. When is each more efficient?
7. Describe the policy evaluation logic in AWS IAM. Why does "explicit deny" override "explicit allow"?
8. A user has read access to a file through their group membership, but the file's ACL explicitly denies them read access. What happens in a typical DAC system? Why?
9. Design an authorization model for a hospital with Doctors, Nurses, Receptionists, and Administrators. Define roles, permissions, and at least two SoD constraints.
10. Compare MAC, RBAC, and ABAC for a cloud-native startup with 50 remote employees using AWS, Slack, and Google Workspace. Which model(s) would you recommend and why?
