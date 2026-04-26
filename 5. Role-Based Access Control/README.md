# 5. Role-Based Access Control (RBAC)

## What Is RBAC?

**Role-Based Access Control (RBAC)** is an authorization model where permissions are assigned to **roles** rather than individual users. Users are then assigned to one or more roles based on their job functions, responsibilities, and organizational position.

This approach mirrors how organizations actually function: people are hired into positions with defined responsibilities, and those responsibilities determine what systems, data, and functions they need to access. Instead of managing hundreds or thousands of individual permission assignments, administrators manage a smaller set of roles.

RBAC is the most widely deployed access control model in enterprise environments, implemented in databases, operating systems, cloud platforms, and business applications.

---

## Why Learn This?

RBAC is foundational to enterprise security. It is the default authorization model in:
- Databases (PostgreSQL, Oracle, SQL Server)
- Cloud platforms (AWS IAM, Azure RBAC, Google Cloud IAM)
- Operating systems (Linux groups, Windows Active Directory)
- Business applications (SAP, Salesforce, Workday)

Understanding RBAC enables you to:
- Design scalable permission systems that align with organizational structure
- Audit who has access to what through role assignments
- Simplify onboarding (assign a role) and offboarding (remove role assignments)
- Implement Separation of Duties through role constraints
- Reduce administrative overhead compared to managing individual permissions

---

## Core Concepts

### RBAC Core Components

| Component | Definition | Example | Why It Matters |
|-----------|-----------|---------|---------------|
| **User** | A person or system entity that needs access | Alice, a senior developer; the CI/CD pipeline | The subject of access control |
| **Role** | A job function or responsibility that carries a set of permissions | "Senior Developer", "Finance Manager", "Contractor" | The bridge between users and permissions |
| **Permission** | An authorization to perform a specific operation on a specific resource | "read_code_repo", "approve_expenses", "delete_user" | The granular building block of access |
| **Session** | A mapping between a user and the subset of their roles they have activated | Alice logs in and activates "Developer" and "Code Reviewer" roles | Enables Dynamic SoD by limiting active roles |

### RBAC Levels (NIST RBAC96)

The NIST standard (ANSI/INCITS 359-2004) defines four levels of RBAC sophistication:

**RBAC0 — Core RBAC**
This is the foundation that all other levels build upon:
- Users are assigned to roles
- Roles are granted permissions
- Users activate roles in sessions
- Users receive the union of permissions from all active roles

**Example:**
- User: Alice
- Roles assigned: Developer, Code Reviewer
- Developer permissions: read_code, write_code, run_tests
- Code Reviewer permissions: read_code, approve_prs
- Alice's effective permissions: read_code, write_code, run_tests, approve_prs

**RBAC1 — Hierarchical RBAC**
Roles can inherit permissions from other roles. This creates a role hierarchy where senior roles automatically include junior role permissions.

**Example hierarchy:**
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

- Senior Developer inherits all Developer permissions
- CTO inherits all Senior Developer permissions (and thus all Developer permissions)
- Alice (Senior Developer) automatically has write_code without explicit assignment

**Benefits:**
- Reduces redundancy — permissions defined once at the junior level
- Ensures consistency — seniors always have what juniors have
- Simplifies administration — promote Alice to Senior Developer, she automatically gets new permissions

**RBAC2 — Constraint-Based RBAC**
Adds rules and restrictions to prevent abuse and enforce security policies.

**Types of constraints:**

| Constraint | Description | Example |
|-----------|-------------|---------|
| **Static SoD** | Mutually exclusive roles cannot be assigned to the same user | Cannot be both "Purchaser" and "Approver" |
| **Dynamic SoD** | Mutually exclusive roles cannot be activated in the same session | Can have both roles but cannot use both simultaneously |
| **Cardinality** | Limit how many users can hold a role | Maximum 3 "Domain Admin" users |
| **Prerequisite** | Must hold Role A before being assigned Role B | Must be "Junior Developer" before "Senior Developer" |

**RBAC3 — Combined RBAC**
The complete implementation combining RBAC1 (hierarchy) and RBAC2 (constraints). This is what most enterprise RBAC systems implement.

### Permission Granularity

| Granularity | Example | When to Use |
|------------|---------|-------------|
| **Coarse** | "Access Finance Module" | Small teams, simple applications, low-risk environments |
| **Medium** | "Read Finance Reports" | Most enterprise applications, standard risk |
| **Fine** | "Read Q4_2024_Revenue.csv" | High-security environments, compliance requirements |

**The granularity trade-off:**
- Too coarse: Violates least privilege, increases blast radius if compromised
- Too fine: Administrative overhead, role explosion, increased error rate
- Best practice: Start coarse, refine based on audit findings and compliance requirements

### The Role Engineering Process

**Role engineering** is the systematic process of designing roles that accurately reflect organizational structure and job functions. It is not guesswork — it follows a structured methodology.

**Why role engineering matters:**
- Poorly designed roles violate least privilege or create excessive administrative burden
- Well-designed roles scale with the organization and simplify audits
- Role engineering is a standard IAM practice in enterprise environments

**The Role Engineering Process (step by step):**

**Phase 1: Data Collection**
- Export current user-permission assignments from all systems
- Gather organizational data: org chart, job descriptions, department structures
- Interview managers and application owners about access needs
- Document compliance requirements that affect access (SOX, HIPAA, etc.)

**Phase 2: Analysis (Role Mining)**
- Create a user-permission matrix (rows = users, columns = permissions)
- Apply clustering algorithms or manual analysis to find natural groupings:
  - Users with similar permissions likely share a job function
  - Permissions that always appear together should be in the same role
- Identify outliers — users with unique permission combinations may indicate:
  - Special job functions deserving their own role
  - Access creep that should be cleaned up

**Example user-permission matrix:**
```
Permission      Alice  Bob  Carol  Dave  Eve  Frank
read_email        ✓     ✓     ✓     ✓     ✓     ✓
access_internet   ✓     ✓     ✓     ✓     ✓     ✓
read_finance      ✓     ✓     -     -     -     -
write_finance     ✓     -     -     -     -     -
approve_expense   -     ✓     -     -     -     -
read_code         -     -     ✓     ✓     ✓     -
write_code        -     -     ✓     ✓     -     -
deploy_prod       -     -     -     ✓     -     -
read_hr           -     -     -     -     ✓     ✓
write_hr          -     -     -     -     ✓     -
```

**Clustering observations:**
- Alice + Bob share finance access → "Finance" role candidate
- Carol + Dave + Eve share code access → "Developer" role candidate
- Eve + Frank share HR access → "HR" role candidate
- Alice has unique write_finance → maybe "Senior Finance" or just keep in Finance
- Dave has unique deploy_prod → "Senior Developer" or separate role

**Phase 3: Role Definition**
- Define candidate roles based on clustering
- Assign permissions to each role
- Name roles clearly and consistently
- Document the business justification for each role

**Phase 4: Validation**
- Review candidate roles with business stakeholders
- Verify roles align with actual job functions
- Check for SoD conflicts within and between roles
- Test role assignments against real users

**Phase 5: Implementation**
- Create roles in the IAM system
- Migrate users from direct permissions to role assignments
- Update provisioning workflows to use roles
- Communicate changes to users and managers

**Phase 6: Maintenance**
- Monitor role usage (are all roles actually used?)
- Review quarterly for relevance
- Adjust as organizational structure changes
- Retire roles that are no longer needed

**Role Mining Approaches:**

| Approach | How It Works | Best For |
|----------|-------------|----------|
| **Top-down** | Start with job descriptions and org chart; define roles theoretically | New IAM implementation, clean slate |
| **Bottom-up** | Analyze existing permissions; discover patterns | Existing environments with accumulated access |
| **Hybrid** | Combine both: use top-down for structure, bottom-up for validation | Most real-world implementations |

### RBAC Best Practices

1. **Start with role mining:** Before defining roles, analyze existing user-permission assignments to discover natural groupings. Data-driven role design is more effective than top-down guessing.

2. **Regular reviews:** Conduct quarterly audits of role definitions and assignments. Remove unused roles. Verify that role members still need their access.

3. **Least privilege:** Each role should contain the minimum permissions necessary. Avoid "god roles" that have access to everything.

4. **Avoid role explosion:** Do not create a unique role for each person. If every user has a unique role, you have simply renamed direct permissions.

5. **Template roles:** Start with industry-standard templates (Employee, Manager, Contractor, Admin) and customize for your organization.

6. **Naming conventions:** Use clear, descriptive role names. "FINANCE_REPORT_READER" is better than "ROLE_47".

---

## How It Works

### How Role Hierarchies Are Implemented

A role hierarchy is a **directed acyclic graph (DAG)** — a tree structure where roles can have multiple parents and multiple children.

**Permission resolution algorithm:**
```python
def get_all_permissions(user):
    """Get all permissions for a user through role hierarchy."""
    permissions = set()
    visited = set()
    
    def traverse(role):
        if role.name in visited:
            return  # Prevent infinite loops in cyclic graphs
        visited.add(role.name)
        
        # Add this role's direct permissions
        permissions.update(role.permissions)
        
        # Recursively add parent role permissions
        for parent in role.parents:
            traverse(parent)
    
    for role in user.active_roles:
        traverse(role)
    
    return permissions
```

**Example walkthrough:**
Alice is a Senior Developer. Senior Developer has parent Developer. Developer has parent Employee.

1. Start with Senior Developer → add {read_code, write_code, review_prs}
2. Traverse to Developer parent → add {read_code, write_code, run_tests}
3. Traverse to Employee parent → add {read_email, access_intranet}
4. Union: {read_code, write_code, review_prs, run_tests, read_email, access_intranet}

### Session Management and Dynamic SoD

When a user logs in, they do not automatically receive all permissions from all assigned roles. They **activate** a subset of roles in a **session**.

**Why sessions matter:**
- Alice is assigned both "Developer" and "Manager" roles
- During coding, she activates only "Developer"
- During code review, she activates only "Code Reviewer"
- She cannot activate both "Developer" and "Deployer" simultaneously (Dynamic SoD)
- This prevents her from approving her own code for production

**Session lifecycle:**
1. User authenticates
2. System presents available roles (based on role assignments)
3. User selects which roles to activate
4. System checks Dynamic SoD constraints
5. Session is created with activated roles
6. Permissions are computed from activated roles + hierarchy
7. On logout or timeout, session is destroyed

### RBAC in Databases

```sql
-- PostgreSQL RBAC example

-- Create roles
CREATE ROLE developer;
CREATE ROLE senior_developer;
CREATE ROLE manager;

-- Grant permissions to roles
GRANT SELECT, INSERT, UPDATE ON code_repository TO developer;
GRANT DELETE, TRUNCATE ON code_repository TO senior_developer;
GRANT ALL PRIVILEGES ON employee_data TO manager;

-- Create role hierarchy
GRANT developer TO senior_developer;  -- Senior dev inherits all dev permissions

-- Assign roles to users
GRANT senior_developer TO alice;
GRANT manager TO alice;

-- Alice's effective permissions:
-- On code_repository: SELECT, INSERT, UPDATE, DELETE, TRUNCATE
-- On employee_data: ALL PRIVILEGES
```

### RBAC in Cloud Platforms

**AWS IAM Roles:**
- IAM roles have policies (permissions)
- Users or services "assume" a role temporarily
- Assumption generates temporary credentials via STS (Security Token Service)
- Every assumption is logged in CloudTrail
- Roles can have trust policies defining who can assume them

**Azure AD Roles:**
- Built-in roles: Global Administrator, User Administrator, Billing Administrator
- Custom roles: Define your own permission sets at granular level
- PIM (Privileged Identity Management): Roles are "eligible" but not "active" by default
- Role activation requires approval and is time-limited

**Kubernetes RBAC:**
- Roles define permissions within a namespace
- ClusterRoles define permissions across the cluster
- RoleBindings/ClusterRoleBindings assign roles to users or service accounts

---

## Where You See It

| System | RBAC Implementation | How You Use It |
|--------|-------------------|----------------|
| **PostgreSQL** | CREATE ROLE, GRANT | Database permissions |
| **AWS IAM** | IAM Roles + Policies | Cross-account access, service roles |
| **Azure AD** | Directory roles + PIM | Admin role elevation |
| **Kubernetes** | Roles, RoleBindings | Pod and resource access |
| **GitHub** | Org roles, Team permissions | Repository access |
| **Salesforce** | Profiles, Permission Sets | Object and field-level access |
| **Linux** | Groups, sudoers | System access and privilege elevation |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "RBAC is just user groups" | RBAC includes role hierarchies, constraints, sessions, and permission inheritance — far more than simple groups |
| "More roles means better security" | Role explosion (too many roles) makes administration harder, increases errors, and complicates audits |
| "RBAC cannot handle context" | RBAC alone cannot evaluate time, location, or device. Hybrid RBAC+ABAC is the modern solution |
| "Role inheritance is always transitive" | Some systems support only single-level inheritance. Verify your platform's capabilities |
| "RBAC replaces the need for authentication" | RBAC is authorization, not authentication. Users must still prove their identity before roles are evaluated |
| "Senior roles should have all permissions" | Senior roles should have appropriate permissions for their responsibilities, not unlimited access |

---

## How to Practice

### Exercise 1: Map Roles in Your Organization
1. List 5-10 job titles in your organization (or a hypothetical one)
2. For each role, define 5-10 permissions they need
3. Identify inheritance relationships (e.g., Senior Developer → Developer)
4. Identify at least one SoD constraint
5. Check for role explosion — are any roles nearly identical?

### Exercise 2: Audit a Real RBAC System
If you have access to any RBAC-enabled system:
1. List all roles
2. Count how many users are assigned to each
3. Identify unused or underutilized roles
4. Check for users with excessive role assignments
5. Document findings in a one-page audit summary

### Exercise 3: Design RBAC for a SaaS Application
Design RBAC for a project management tool with:
- **Admin:** Full system control, user management, billing
- **Project Manager:** Create projects, assign tasks, view all team progress
- **Team Lead:** Manage their team's tasks, view team progress
- **Developer:** View and update assigned tasks, comment on others
- **Viewer:** Read-only access to specific projects
- **Contractor:** Time-limited access to one project only

Define: roles, permissions, hierarchy (if any), constraints, and session rules.

### Exercise 4: Run the Simulations
- `rbac_engine.py` — Full RBAC with hierarchy, sessions, and SoD
- `role_hierarchy_visualizer.py` — Visualize inheritance trees
- `rbac_audit_tool.py` — Check for compliance issues

---

## Projects

### `rbac_engine.py`
Full-featured RBAC implementation:
- User-role assignment and revocation
- Role-permission grants
- Role hierarchy with recursive inheritance
- Session management with role activation
- Static and Dynamic SoD enforcement
- Permission inheritance calculation

### `role_hierarchy_visualizer.py`
Visualizes role hierarchies:
- ASCII tree representation of inheritance
- Permission coverage analysis per role
- Identifies over-privileged roles
- Detects circular inheritance (which would cause infinite loops)
- Compares two roles for similarity and differences

### `rbac_audit_tool.py`
Audits RBAC configurations:
- Identifies orphaned permissions (no users have them)
- Finds inactive roles (no users assigned)
- Detects excessive permissions per role
- Generates role coverage reports
- Checks SoD violations across all users

### `role_mining_sim.py`
Demonstrates role mining algorithms:
- Analyzes user-permission assignments
- Discovers candidate roles through clustering
- Optimizes role-permission coverage
- Minimizes role count while covering all access needs

---

## Check Your Understanding

1. What are the four components of RBAC0? Describe each and explain how they relate to each other.
2. How does RBAC1 differ from RBAC0? Draw a role hierarchy for a technology company and explain the inheritance flow.
3. What is role explosion and how can it be prevented? Give specific examples of good and bad role design.
4. Explain Static vs Dynamic Separation of Duties. When would you use each? Give a real-world example of each.
5. Why might an organization migrate from RBAC to ABAC? What would they gain and what would they lose?
6. How does session-based role activation improve security? Describe a scenario where it prevents fraud.
7. Walk through the permission resolution algorithm for a user with three activated roles in a hierarchy with two levels of inheritance.
8. Design an RBAC system for a hospital with: Doctors, Nurses, Surgeons, Receptionists, Billing Staff, and Administrators. Include at least two hierarchy relationships and two SoD constraints.
9. A user is assigned to five roles but activates only two in their session. They try to perform an action that requires a permission from one of their inactive roles. What happens? Why is this behavior important?
10. Compare RBAC implementation in PostgreSQL, AWS IAM, and Kubernetes. What similarities and differences exist across these platforms?
