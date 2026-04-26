# 5. Role-Based Access Control (RBAC)

## What Is RBAC?

**Role-Based Access Control (RBAC)** is an authorization model where permissions are assigned to **roles** rather than individual users. Users are then assigned to roles based on their job functions.

This mirrors how organizations actually work: people are hired into positions with defined responsibilities, and those responsibilities determine what they need to access.

---

## Why Learn This?

RBAC is the **most widely deployed access control model** in enterprise environments. It is the default approach in databases, cloud platforms, and operating systems. Understanding RBAC enables you to:
- Design scalable permission systems
- Audit who has access to what
- Simplify onboarding and offboarding
- Implement Separation of Duties

---

## Core Concepts

### RBAC Components

| Component | Definition | Example |
|-----------|-----------|---------|
| **User** | A person or system entity | Alice, the CI/CD pipeline |
| **Role** | A job function or responsibility | "Senior Developer", "Finance Manager" |
| **Permission** | Authorization to perform an operation | "Read Q4 report", "Deploy to production" |
| **Session** | A mapping between a user and their active roles | Alice logs in and activates "Developer" and "Code Reviewer" |

### RBAC Levels (NIST RBAC96)

The NIST standard defines four levels of RBAC sophistication:

**RBAC0 — Core RBAC**
- Users assigned to roles
- Roles granted permissions
- Users activate roles in sessions
- This is the foundation everything else builds on

**RBAC1 — Hierarchical RBAC**
- Roles can inherit from other roles
- Example: "Senior Developer" automatically gets all "Developer" permissions plus extras
- Reduces redundancy and simplifies administration

**RBAC2 — Constraint-Based RBAC**
- Adds rules and restrictions
- Static SoD: Cannot be both "Purchaser" and "Approver"
- Dynamic SoD: Cannot activate both roles in the same session
- Cardinality: Maximum 3 "System Admin" users

**RBAC3 — Combined RBAC**
- Full hierarchical roles with constraints
- The complete implementation used in enterprise systems

### Role Hierarchy Example

```
                    CEO
                     │
            ┌────────┴────────┐
            │                 │
        CTO                 CFO
            │                 │
      ┌─────┴─────┐     ┌─────┴─────┐
      │           │     │           │
  Senior      Junior  Senior    Junior
  Developer   Developer Analyst Analyst
      │
   Developer
```

In this hierarchy:
- A Senior Developer inherits all Developer permissions automatically
- The CTO inherits all Senior Developer permissions
- The CEO inherits everything below

### Permission Granularity

| Level | Example | When to Use |
|-------|---------|-------------|
| Coarse | "Access Finance Module" | Small teams, simple applications |
| Medium | "Read Finance Reports" | Most enterprise applications |
| Fine | "Read Q4_2024_Revenue.csv" | High-security environments |

**Trade-off:** Fine-grained permissions are more secure but harder to manage. Coarse permissions are easier but may violate least privilege.

### RBAC Best Practices

1. **Role mining:** Analyze existing permissions to discover optimal roles
2. **Regular reviews:** Quarterly audits of who has what roles
3. **Least privilege:** Roles should have minimum necessary permissions
4. **Avoid role explosion:** Do not create a unique role for each person
5. **Template roles:** Start with industry-standard templates

---

## How It Works

### How Role Hierarchies Are Implemented

A role hierarchy is a **directed acyclic graph (DAG)**. Each role can have multiple parents and multiple children.

**Algorithm to resolve permissions:**
1. Start with the user's directly assigned roles
2. For each role, recursively collect all parent roles
3. Gather all permissions from all roles in the hierarchy
4. Remove duplicates
5. Return the union

```python
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

When a user logs in, they do not automatically get all their role permissions. They **activate** specific roles in a **session**.

**Why this matters:**
- A manager might have "Manager" and "Developer" roles
- During a coding session, they activate only "Developer"
- During a review session, they activate only "Manager"
- This implements **Dynamic Separation of Duties** — they cannot approve their own code because both roles are not active simultaneously

### RBAC in Databases

```sql
-- PostgreSQL
CREATE ROLE analyst;
GRANT SELECT ON sales_data TO analyst;
GRANT analyst TO alice;  -- Alice gets all analyst permissions
```

### RBAC in Cloud Platforms

**AWS IAM:**
- Users or services "assume" roles temporarily
- Roles have policies (permissions)
- Assumption is logged in CloudTrail

**Azure AD:**
- Built-in roles: Global Administrator, User Administrator
- Custom roles: Define your own permission sets
- PIM (Privileged Identity Management): Just-in-time role activation

---

## Where You See It

| System | RBAC Feature | How It Works |
|--------|-------------|--------------|
| **PostgreSQL** | Roles and grants | `CREATE ROLE`, `GRANT` |
| **AWS IAM** | IAM Roles | AssumeRole, policy attachment |
| **Azure AD** | Directory roles | Built-in and custom roles |
| **Kubernetes** | RBAC API | Roles, RoleBindings, ClusterRoles |
| **GitHub** | Organization roles | Owner, Member, Outside Collaborator |
| **Salesforce** | Profiles and roles | Object-level and field-level permissions |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "RBAC is just groups" | RBAC includes role hierarchies, constraints, and sessions — more than simple groups |
| "More roles = better security" | Role explosion (too many roles) makes administration harder and increases error risk |
| "RBAC cannot handle dynamic access" | RBAC alone cannot; hybrid RBAC+ABAC is the modern approach |
| "Role inheritance is always transitive" | Some systems support only single-level inheritance; check your platform |

---

## How to Practice

1. **Map roles in an organization you know**
   - List 5-10 job titles
   - Define what each role should access
   - Identify inheritance relationships
   - Check for SoD violations

2. **Audit a real RBAC system**
   - If you have access to AWS IAM, Azure AD, or a database, review role assignments
   - Look for orphaned roles (no users assigned)
   - Look for over-permissioned roles

3. **Run the simulations**
   - `rbac_engine.py` implements full RBAC with hierarchies and SoD
   - `role_hierarchy_visualizer.py` shows permission inheritance
   - `rbac_audit_tool.py` checks for compliance issues

---

## Projects

### `rbac_engine.py`
Full-featured RBAC implementation:
- User-role assignment and revocation
- Role-permission grants
- Role hierarchy with inheritance
- Session management with role activation
- Static and Dynamic SoD enforcement

### `role_hierarchy_visualizer.py`
Visualizes role hierarchies:
- ASCII tree representation
- Permission coverage analysis
- Identifies over-privileged roles
- Detects circular inheritance

### `rbac_audit_tool.py`
Audits RBAC configurations:
- Identifies orphaned permissions
- Finds inactive roles
- Detects excessive permissions
- Generates role coverage reports
- Checks SoD violations

### `role_mining_sim.py`
Demonstrates role mining algorithms:
- Analyzes user-permission assignments
- Discovers candidate roles
- Optimizes role-permission coverage

---

## Check Your Understanding

1. What are the four components of RBAC0? Describe each with a real-world example.
2. How does RBAC1 differ from RBAC0? Why is inheritance useful?
3. What is role explosion and how can it be prevented?
4. Explain Static vs Dynamic Separation of Duties in RBAC. When would you use each?
5. Why might an organization migrate from RBAC to ABAC? What would they lose and gain?
6. How does session-based role activation improve security?
