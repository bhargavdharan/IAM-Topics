# 6. Attribute-Based Access Control (ABAC)

## 🏠 Real-World Analogy: Smart Building Access

Imagine a futuristic office building with intelligent doors:

Instead of fixed badges, the building knows:
- **Who you are:** Name, department, clearance level
- **What you're trying to access:** Conference room, server room, CEO office
- **When it is:** Business hours vs. midnight
- **Where you are:** Inside the building vs. remote
- **What device you're using:** Company laptop vs. personal phone
- **Why you need access:** Scheduled meeting vs. random request

The door decides in real-time:
```
"ALLOW if:
  - User.department == 'Engineering'
  - AND Resource.type == 'development-server'
  - AND Time.hour BETWEEN 8 AND 20
  - AND Device.managed == true
  - AND Network.location == 'corporate-office'"
```

**This is ABAC: dynamic, context-aware access decisions based on multiple attributes.**

---

## 📋 Overview

ABAC is the most flexible and powerful access control model. Instead of asking "What role do you have?" (RBAC), ABAC asks "What are your attributes, the resource's attributes, the action's attributes, and the environment's attributes?"

**Why ABAC matters:**
- Modern work is dynamic (remote, contractors, project-based)
- Context matters (time, location, device trust)
- Compliance requires fine-grained control
- Cloud environments are too complex for simple roles

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain ABAC with real-world examples
- Identify the four attribute categories in ABAC
- Write ABAC policies using Boolean logic
- Compare ABAC vs RBAC and when to use each
- Understand XACML architecture
- Build a working ABAC policy engine

---

## 📚 Key Concepts

### The Four Attribute Categories

ABAC evaluates four types of attributes for every access decision:

| Category | Examples | Description |
|----------|----------|-------------|
| **Subject (User)** | Department, job title, clearance, age, certifications | Who is requesting access |
| **Resource** | Classification, owner, creation date, type | What is being accessed |
| **Action** | Read, write, delete, execute, approve | What operation is being attempted |
| **Environment** | Time, location, device type, threat level | The context of the request |

### ABAC Policy Examples

```
POLICY 1: "Contractors can only access project files during business hours"
IF user.type == "contractor"
AND resource.type == "project-file"
AND action == "read"
AND environment.time.hour BETWEEN 9 AND 17
THEN ALLOW

POLICY 2: "Finance data requires manager approval from company network"
IF resource.department == "finance"
AND user.department == "finance"
AND user.level >= "manager"
AND environment.network == "corporate"
THEN ALLOW

POLICY 3: "Deny access to classified docs from unmanaged devices"
IF resource.classification == "classified"
AND device.managed == false
THEN DENY
```

### ABAC vs RBAC: When to Use Which

| Scenario | Best Model | Why |
|----------|-----------|-----|
| Stable organization with clear job titles | RBAC | Simple, aligns with org chart |
| Remote/hybrid work with device trust | ABAC | Needs location and device attributes |
| Project-based teams with changing membership | ABAC | Roles change too frequently |
| Compliance requiring time-based access | ABAC | RBAC can't evaluate time |
| Small company, <50 employees | RBAC | ABAC is overkill |
| Large enterprise with complex compliance | ABAC + RBAC hybrid | RBAC for coarse, ABAC for fine-grained |

---

## 🔧 Under the Hood

### XACML Architecture

XACML (eXtensible Access Control Markup Language) is the standard for ABAC. It's like a court system:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PEP        │────→│   PDP        │────→│   PIP        │
│Policy         │     │Policy         │     │Policy        │
│Enforcement    │←────│Decision       │←────│Information   │
│Point          │     │Point          │     │Point         │
└──────────────┘     └──────────────┘     └──────────────┘
        ↑                                          ↑
        └──────────────────────────────────────────┘
                      PAP (Policy Administration Point)
```

| Component | Role | Analogy |
|-----------|------|---------|
| **PEP** | Intercepts access requests | Security guard at the door |
| **PDP** | Evaluates policies and decides | Judge making a ruling |
| **PIP** | Provides attribute values | Court clerk fetching records |
| **PAP** | Creates and manages policies | Legislature writing laws |

**How a request flows:**
1. User tries to open a file
2. **PEP** intercepts and creates a request: "Can Alice read file.doc?"
3. **PDP** looks up policies and asks **PIP** for attributes
4. **PIP** fetches: Alice's department, file's classification, current time, etc.
5. **PDP** evaluates all policies and returns: PERMIT, DENY, or NOT_APPLICABLE
6. **PEP** enforces the decision

### Policy Evaluation Logic

ABAC policies use Boolean logic with operators:

```
AND  → All conditions must be true
OR   → At least one condition must be true
NOT  → Condition must be false
```

**Conflict resolution:** What if one policy says ALLOW and another says DENY?
- **Deny-overrides:** If any policy says DENY, the result is DENY (most secure)
- **Permit-overrides:** If any policy says ALLOW, the result is ALLOW
- **First-applicable:** First matching policy wins
- **Only-one-applicable:** Error if multiple policies match

### ABAC in the Real World

**AWS IAM Policies:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::company-bucket/*",
    "Condition": {
      "StringEquals": {"aws:RequestedRegion": "us-east-1"},
      "IpAddress": {"aws:SourceIp": "203.0.113.0/24"}
    }
  }]
}
```

**Azure AD Conditional Access:**
- IF user.riskLevel == "high" → Require MFA
- IF device.compliance == "noncompliant" → Block access
- IF location.country NOT IN ["US", "CA"] → Require approval

---

## 🛠️ Projects in This Module

### `abac_policy_evaluator.py`
Evaluates ABAC policies against requests:
- Defines subjects, resources, actions, and environment attributes
- Parses Boolean policy expressions
- Resolves policy conflicts
- Returns PERMIT/DENY/NOT_APPLICABLE

### `abac_vs_rbac_comparator.py`
Compares ABAC and RBAC for the same scenario:
- Shows how RBAC requires many roles for the same result
- Demonstrates ABAC's flexibility
- Calculates administrative overhead

### `xacml_policy_generator.py`
Generates XACML-compliant policy XML:
- Creates policies from simple rules
- Validates policy syntax
- Exports for import into XACML engines

---

## 📝 Quiz Questions

1. **Name the four attribute categories in ABAC and give two examples of each.**
2. **Write an ABAC policy that allows access ONLY during business hours from company devices.**
3. **Why is ABAC more flexible than RBAC? What is the trade-off?**
4. **What is XACML? Describe the roles of PEP, PDP, PIP, and PAP.**
5. **How does "deny-overrides" conflict resolution work? Why is it the most secure default?**

---

## 🔗 Further Reading

- [NIST ABAC Guide](https://csrc.nist.gov/publications/detail/sp/800-178/final)
- [XACML 3.0 Specification](http://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html)
- [AWS IAM Policy Conditions](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html)

---

## 🏷️ Tags
`#ABAC` `#AttributeBasedAccessControl` `#XACML` `#PolicyEngine` `#RBAC` `#Authorization`
