# 4. Authorization Models and Access Control

## 🏠 Real-World Analogy: Office Building Access

Imagine a large office building:

- **The lobby** has a receptionist who checks your ID. That's **authentication**.
- **Your key card** determines which floors, rooms, and elevators you can use. That's **authorization**.

Different buildings use different authorization rules:

1. **DAC (Discretionary):** The corner office manager decides who can enter their office. Flexible, but what if they give access to the wrong person?

2. **MAC (Mandatory):** The building owner sets strict rules. "Only people with Top Secret clearance can enter Floor 10." No manager can override this.

3. **RBAC (Role-Based):** Your job title determines access. All "Accountants" can enter the Finance floor. All "Developers" can enter the Tech floor.

4. **ABAC (Attribute-Based):** Smart rules. "Accountants can enter Finance floor ONLY during business hours AND from company laptops."

**Authorization answers: "What are you allowed to do?"**

---

## 📋 Overview

While authentication proves who you are, authorization decides what you can do. Authorization models are the **rules engine** of security — they evaluate every request to open a file, access a database, or view a page.

Choosing the right model is critical:
- Too restrictive → Users can't do their jobs
- Too permissive → Security breaches happen
- Too complex → Administrators make mistakes

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Clearly distinguish authentication from authorization
- Explain DAC, MAC, RBAC, ABAC, and PBAC with real-world examples
- Understand access control matrices, ACLs, and capability lists
- Describe Static and Dynamic Separation of Duties
- Choose the right authorization model for a given scenario

---

## 📚 Key Concepts

### Authentication vs Authorization

| Question | Authentication | Authorization |
|----------|---------------|---------------|
| Asks | "Who are you?" | "What can you do?" |
| Process | Verifying identity | Granting or denying permissions |
| Example | Fingerprint scan at door | Door opens only certain floors |
| Failure message | "Invalid credentials" | "Access denied" |
| Analogy | Showing your passport | Visa stamp determining where you can go |

> **Analogy:** Authentication is like proving you're 21+ at a bar. Authorization is the bouncer deciding whether you can enter the VIP section.

### Access Control Models

#### 1. Discretionary Access Control (DAC)

**Concept:** Resource owners decide who can access their resources.

**Real-world example:** Google Drive — you own a document and decide who can view, comment, or edit it.

**Pros:** Flexible, easy to understand
**Cons:** Can lead to privilege escalation (if you give access to someone who shouldn't have it)

**Common in:** File systems (Unix permissions, Windows ACLs), cloud storage

#### 2. Mandatory Access Control (MAC)

**Concept:** System-enforced policies based on security labels. Users CANNOT override policies.

**Real-world example:** Military documents labeled "Top Secret," "Secret," "Confidential." A general cannot choose to show a Top Secret document to a Private.

**Pros:** Highly secure, tamper-proof
**Cons:** Rigid, complex to administer

**Common in:** Government, military, SELinux, Bell-LaPadula model

#### 3. Role-Based Access Control (RBAC)

**Concept:** Permissions are assigned to roles; users are assigned to roles.

**Real-world example:** In a hospital:
- "Doctor" role → can view patient records, prescribe medication
- "Nurse" role → can view patient records, administer medication
- "Receptionist" role → can view scheduling, NOT medical records

**Pros:** Simplifies administration, aligns with organizational structure
**Cons:** Can lead to "role explosion" in complex organizations

**Common in:** Enterprise applications, databases, cloud platforms

#### 4. Attribute-Based Access Control (ABAC)

**Concept:** Access decisions based on attributes of user, resource, action, and environment.

**Real-world example:** "Allow access IF:
- User.department == Resource.department
- AND User.location == 'office'
- AND Time is between 9 AM and 6 PM
- AND User.clearance >= Resource.classification"

**Pros:** Highly flexible, dynamic, fine-grained
**Cons:** Complex to design and debug

**Common in:** Cloud IAM (AWS IAM policies), XACML implementations

#### 5. Policy-Based Access Control (PBAC)

**Concept:** Centralized policy engine evaluates all access decisions. Combines RBAC and ABAC concepts.

**Real-world example:** A corporate legal department sets a single policy: "No one under 'Manager' level can access contracts older than 7 years." This policy is enforced across all systems.

**Common in:** Enterprise IAM platforms (Okta, Azure AD, SailPoint)

### Model Comparison

| Model | Decided By | Flexibility | Complexity | Best For |
|-------|-----------|-------------|------------|----------|
| **DAC** | Resource owner | High | Low | Personal files, collaboration |
| **MAC** | System administrator | None | High | Military, high-security environments |
| **RBAC** | Role assignments | Medium | Medium | Most organizations |
| **ABAC** | Dynamic attributes | Very High | High | Complex, changing environments |
| **PBAC** | Centralized policies | High | Very High | Large enterprises |

---

## 🔧 Under the Hood

### Access Control Structures

#### Access Control Matrix

The theoretical foundation: a big table showing who can do what.

```
              File_A    File_B    File_C    Printer
Alice         rw        r         -         print
Bob           r         rw        r         -
Charlie       -         -         rw        print
Admin         rwx       rwx       rwx       admin
```

- `r` = read, `w` = write, `x` = execute, `-` = no access

**Problem:** In a system with 100,000 users and 1,000,000 files, this matrix is enormous and mostly empty (sparse).

#### Access Control List (ACL)

Store permissions WITH the resource:

```
File_A:
  Alice: read, write
  Bob: read
  Admin: read, write, execute
```

**Pros:** Efficient when asking "Who can access this file?"
**Cons:** Slow when asking "What can Alice access?"

**Used in:** File systems (Windows NTFS, Linux ext4), cloud storage

#### Capability List

Store permissions WITH the user:

```
Alice:
  File_A: read, write
  File_B: read
  Printer: print
```

**Pros:** Efficient when asking "What can Alice access?"
**Cons:** Hard to audit who has access to a specific resource

**Used in:** Operating system capabilities, API tokens

#### How Modern Systems Actually Work

Most systems use a **hybrid approach**:

1. **User → Groups/Roles:** Alice is in "Finance" group
2. **Groups → Permissions:** "Finance" group has read access to `finance/*`
3. **Resource ACLs:** Each file has an ACL referencing groups, not individuals
4. **Evaluation:** When Alice requests `Q4-report.pdf`, the system:
   - Looks up Alice's groups: ["Finance", "Employees"]
   - Checks the file's ACL: `Finance: read, Employees: read`
   - Determines: ALLOW read

### Constraints

| Constraint | Description | Example |
|------------|-------------|---------|
| **Static SoD** | Mutually exclusive roles (never at same time) | Cannot be both "Purchaser" and "Approver" |
| **Dynamic SoD** | Mutually exclusive permissions in same session | Cannot approve your own purchase request |
| **Cardinality** | Limit role membership | Maximum 3 people can be "System Admin" |
| **Prerequisite** | Must have Role A before Role B | Need "Junior Developer" before "Senior Developer" |

---

## 🛠️ Projects in This Module

### `access_matrix_visualizer.py`
Creates and visualizes access control matrices:
- Defines users, resources, and permissions
- Generates ACL and capability list views
- Checks for privilege escalation paths
- Validates SoD constraints

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

## 📝 Quiz Questions

1. **What is the key difference between DAC and MAC? Give a real-world example of each.**
2. **How does RBAC simplify administration compared to managing individual permissions?**
3. **Give an example of an ABAC policy that uses environmental attributes (like time or location).**
4. **What is Static Separation of Duties? How does it differ from Dynamic SoD?**
5. **Why might an organization migrate from RBAC to ABAC? What are the trade-offs?**
6. **Explain the difference between an Access Control List (ACL) and a Capability List.**

---

## 🔗 Further Reading

- [NIST RBAC Standard](https://csrc.nist.gov/projects/role-based-access-control)
- [XACML Specification](http://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html)
- [ABAC Overview - NIST](https://csrc.nist.gov/projects/abac/)

---

## 🏷️ Tags
`#Authorization` `#AccessControl` `#RBAC` `#ABAC` `#MAC` `#DAC` `#PBAC` `#SoD` `#ACL`
