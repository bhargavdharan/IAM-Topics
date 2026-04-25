# 5. Role-Based Access Control (RBAC)

## 🏠 Real-World Analogy: Hospital Staff Badges

Imagine a hospital where every employee wears a color-coded badge:

| Badge Color | Access |
|-------------|--------|
| 🔴 Red | Doctors — patient records, prescribe meds, operating rooms |
| 🟡 Yellow | Nurses — patient records, administer meds, patient rooms |
| 🟢 Green | Receptionists — scheduling, billing, waiting areas |
| 🔵 Blue | Janitors — all hallways, storage closets, NOT patient records |
| ⚫ Black | IT Admin — everything, including system configuration |

When a new doctor joins, the hospital doesn't create custom permissions for them. They simply get a **red badge** — instantly inheriting all doctor permissions.

When a nurse gets promoted to head nurse, their badge changes from yellow to **gold** — which includes all yellow permissions PLUS extra ones.

**This is RBAC: using job roles (not individual names) to control access.**

---

## 📋 Overview

RBAC is the **most widely deployed** access control model in enterprise environments. By assigning permissions to roles rather than individual users, RBAC dramatically simplifies administration while enforcing the Principle of Least Privilege.

**Why RBAC is so popular:**
- Aligns with how organizations actually work (people have job titles)
- Easy to audit ("Who has the Admin role?")
- Simplifies onboarding/offboarding (assign/remove a role)
- Reduces errors (standardized permission sets)

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain RBAC core concepts: users, roles, permissions, sessions
- Describe RBAC levels (RBAC0 through RBAC3)
- Understand role hierarchies and inheritance
- Implement constraints: SoD, cardinality, prerequisites
- Build a working RBAC engine

---

## 📚 Key Concepts

### RBAC Core Components

| Component | Simple Definition | Hospital Example |
|-----------|-------------------|------------------|
| **User** | A person or system entity | Dr. Smith, Nurse Jones |
| **Role** | A job function or responsibility | "Doctor", "Nurse", "Admin" |
| **Permission** | Authorization to perform an operation | "Read patient records", "Prescribe medication" |
| **Session** | A mapping between a user and their active roles | Dr. Smith logs in and activates "Doctor" role |

### RBAC Levels (NIST RBAC96)

The NIST standard defines four levels of RBAC sophistication:

#### RBAC0 — Core RBAC
The foundation:
- Users assigned to roles
- Roles granted permissions
- Users activate roles in sessions

```
User: Alice
Roles: [Developer, TeamLead]
Permissions for Developer: [read_code, write_code, run_tests]
Permissions for TeamLead: [read_code, write_code, run_tests, approve_merge, deploy_prod]
```

#### RBAC1 — Hierarchical RBAC
Roles can inherit from other roles:

```
CEO
└── CTO
    └── Senior Developer
        └── Junior Developer
```

- **Senior Developer** automatically gets all **Junior Developer** permissions
- **CTO** gets all **Senior Developer** permissions (and all below)
- No need to manually assign every permission at every level

**Real-world example:** A "Senior Manager" inherits all "Manager" permissions plus extra ones.

#### RBAC2 — Constraint-Based RBAC
Adds rules and restrictions:

- **Static SoD:** Alice cannot be both "Purchaser" AND "Approver"
- **Dynamic SoD:** Alice can have both roles, but cannot activate both in the same session
- **Cardinality:** Maximum 3 people can hold the "System Admin" role
- **Prerequisite:** Must be "Junior Developer" for 1 year before getting "Senior Developer"

#### RBAC3 — Combined RBAC
The full package: **RBAC1 (hierarchy) + RBAC2 (constraints)**

### Permission Granularity

| Level | Example | When to Use |
|-------|---------|-------------|
| **Coarse** | "Access Finance Module" | Small teams, simple applications |
| **Medium** | "Read Finance Reports" | Most enterprise applications |
| **Fine** | "Read Q4_2024_Revenue.csv" | High-security environments, compliance |

> ⚠️ **Trade-off:** Fine-grained permissions are more secure but harder to manage. Coarse permissions are easier but may violate least privilege.

### RBAC Best Practices

1. **Role Mining:** Analyze existing permissions to discover optimal roles
2. **Regular Reviews:** Quarterly audits of who has what roles
3. **Least Privilege:** Roles should have minimum necessary permissions
4. **Avoid Role Explosion:** Don't create a unique role for each person
5. **Template Roles:** Start with industry-standard templates (e.g., "Employee", "Manager", "Contractor")

### RBAC vs ABAC

| Factor | RBAC | ABAC |
|--------|------|------|
| **Complexity** | Lower | Higher |
| **Flexibility** | Less (static roles) | More (dynamic attributes) |
| **Performance** | Faster (simple lookup) | Slower (evaluate expressions) |
| **Scale** | Medium organizations | Large, complex organizations |
| **Context-aware** | No | Yes (time, location, device) |
| **Example rule** | "Developers can read code" | "Developers can read code IF on company laptop AND during business hours" |

---

## 🔧 Under the Hood

### How Role Hierarchies Are Implemented

A role hierarchy is a **directed acyclic graph (DAG)** — a tree structure where roles inherit from other roles.

```
                Admin
                  │
        ┌─────────┴─────────┐
        │                   │
    Manager            Auditor
        │
   ┌────┴────┐
   │         │
Developer  Tester
   │
Junior Dev
```

**Algorithm to find all permissions for a user:**
1. Get all roles assigned to the user
2. For each role, recursively find all parent roles
3. Collect all permissions from all roles in the hierarchy
4. Remove duplicates
5. Return the union

```python
# Conceptual permission resolution
def get_all_permissions(user):
    permissions = set()
    visited = set()
    
    def traverse(role):
        if role in visited:
            return
        visited.add(role)
        permissions.update(role.permissions)
        for parent in role.parents:
            traverse(parent)
    
    for role in user.roles:
        traverse(role)
    
    return permissions
```

### Session Management in RBAC

When a user logs in, they don't automatically get all their role permissions. They **activate** specific roles in a **session**.

**Why this matters:**
- A manager might have "Manager" and "Developer" roles
- During a coding session, they activate only "Developer"
- During a review session, they activate only "Manager"
- This implements **Dynamic Separation of Duties**

```python
# Session-based role activation
session = create_session(user=alice)
session.activate_role("Developer")
# Alice now has Developer permissions only
# She cannot approve her own code because Manager role is inactive
```

### RBAC in Databases

Most databases implement RBAC:

```sql
-- PostgreSQL example
CREATE ROLE analyst;
GRANT SELECT ON sales_data TO analyst;
GRANT analyst TO alice;  -- Alice gets all analyst permissions
```

### RBAC in Cloud Platforms

**AWS IAM Roles:**
- Users or services "assume" roles temporarily
- Roles have policies (permissions)
- Assumption is logged in CloudTrail

**Azure AD Roles:**
- Built-in roles: Global Administrator, User Administrator
- Custom roles: Define your own permission sets
- PIM (Privileged Identity Management): Just-in-time role activation

---

## 🛠️ Projects in This Module

### `rbac_engine.py`
Full-featured RBAC implementation:
- User-role assignment and revocation
- Role-permission grants
- Role hierarchy with inheritance
- Session management with role activation
- Static and Dynamic SoD enforcement
- Permission inheritance calculation

### `role_hierarchy_visualizer.py`
Visualizes role hierarchies and permission flows:
- Graph representation of role inheritance
- Permission coverage analysis
- Identifies over-privileged roles
- Detects circular inheritance

### `rbac_audit_tool.py`
Audits RBAC configurations for compliance:
- Identifies orphaned permissions (no users have them)
- Finds inactive roles (no users assigned)
- Detects excessive permissions
- Generates role coverage reports
- Checks SoD violations

### `role_mining_sim.py`
Demonstrates role mining algorithms:
- Analyzes user-permission assignments
- Discovers candidate roles
- Optimizes role-permission coverage
- Minimizes role count while covering all access needs

---

## 📝 Quiz Questions

1. **What are the four components of RBAC0? Describe each with a real-world example.**
2. **How does RBAC1 differ from RBAC0? Why is inheritance useful?**
3. **What is role explosion and how can it be prevented?**
4. **Explain Static vs Dynamic Separation of Duties in RBAC. When would you use each?**
5. **Why might an organization migrate from RBAC to ABAC? What would they lose and gain?**
6. **How does session-based role activation improve security?**

---

## 🔗 Further Reading

- [NIST RBAC Standard (ANSI/INCITS 359-2004)](https://csrc.nist.gov/projects/role-based-access-control)
- [RBAC on Wikipedia](https://en.wikipedia.org/wiki/Role-based_access_control)
- [AWS IAM Roles Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

---

## 🏷️ Tags
`#RBAC` `#RoleBasedAccessControl` `#AccessManagement` `#SoD` `#RoleHierarchy` `#IAM` `#NIST`
