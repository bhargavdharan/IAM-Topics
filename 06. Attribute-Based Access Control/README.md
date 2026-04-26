# 6. Attribute-Based Access Control (ABAC)

## What Is ABAC?

**Attribute-Based Access Control (ABAC)** is an authorization model where access decisions are determined by evaluating attributes of the user (subject), the resource, the requested action, and the environment.

Unlike RBAC, which asks "What role does this user have?", ABAC asks "What are the user's attributes, the resource's attributes, the action's attributes, and the current environmental context?" This enables fine-grained, dynamic, context-aware access control that adapts to real-time conditions.

ABAC is the most flexible authorization model and is increasingly used in cloud environments, zero-trust architectures, and complex enterprise systems.

---

## Why Learn This?

Modern IT environments are dynamic and complex:
- Remote workers need access from home, coffee shops, and airports
- Contractors need time-limited access to specific projects
- Cloud resources spin up and down automatically
- Regulatory requirements demand context-aware controls

RBAC struggles with this complexity because roles are static. ABAC addresses it by making access decisions based on current context. Understanding ABAC enables you to:
- Design context-aware security policies
- Implement fine-grained cloud IAM policies
- Build zero-trust architectures
- Evaluate and select policy engines

---

## Core Concepts

### The Four Attribute Categories

ABAC evaluates four types of attributes for every access request:

| Category | What It Describes | Examples |
|----------|-------------------|----------|
| **Subject (User)** | Who is requesting access | Department, job title, clearance level, employment type, certifications |
| **Resource** | What is being accessed | Classification, owner, data type, sensitivity, creation date, location |
| **Action** | What operation is being attempted | Read, write, delete, execute, approve, share |
| **Environment** | The context of the request | Time, date, location, device type, network, threat level |

### ABAC Policy Structure

ABAC policies are Boolean expressions that combine attributes using logical operators:

```
POLICY: Allow Finance Access
IF user.department == "Finance"
AND user.status == "active"
AND resource.type == "financial_report"
AND action == "read"
AND environment.time.hour >= 9
AND environment.time.hour <= 17
AND environment.network == "corporate"
THEN ALLOW

POLICY: Deny Classified from Personal Devices
IF resource.classification == "classified"
AND device.managed == false
THEN DENY

POLICY: Contractor Time Limits
IF user.employment_type == "contractor"
AND environment.date > user.contract_end_date
THEN DENY
```

**Key insight:** A single ABAC policy can replace dozens of RBAC roles. Instead of creating "Finance_Morning_Corporate", "Finance_Evening_Corporate", "Finance_Morning_VPN", etc., you write one policy with conditions.

### ABAC vs RBAC Detailed Comparison

| Aspect | RBAC | ABAC |
|--------|------|------|
| **Basis of decision** | Static role membership | Dynamic attribute evaluation |
| **Flexibility** | Low-Medium | Very High |
| **Complexity** | Medium | High |
| **Performance** | Fast (simple lookup) | Slower (expression evaluation) |
| **Context awareness** | No | Yes (time, location, device, etc.) |
| **Audit difficulty** | Easy ("Alice has Developer role") | Harder ("Alice was denied because device.managed was false") |
| **Admin overhead** | Medium (role management) | High (policy authoring and debugging) |
| **Best for** | Stable organizations with clear job functions | Dynamic, cloud, remote, or regulated environments |

**The hybrid approach (recommended):**
Most effective implementations use RBAC for coarse-grained access (job functions) and ABAC for fine-grained constraints (context, time, device, location).

**Example hybrid policy:**
```
RBAC: Alice is a Developer → Base permissions granted
ABAC: Alice can access production ONLY during business hours from corporate devices
```

---

## How It Works

### XACML Architecture

XACML (eXtensible Access Control Markup Language) is the OASIS standard for ABAC. The architecture separates concerns:

| Component | Role | Analogy |
|-----------|------|---------|
| **PEP** (Policy Enforcement Point) | Intercepts access requests and enforces decisions | Security guard at the door |
| **PDP** (Policy Decision Point) | Evaluates policies and makes access decisions | Judge reviewing case law |
| **PIP** (Policy Information Point) | Retrieves attribute values from sources | Court clerk fetching records |
| **PAP** (Policy Administration Point) | Creates, manages, and distributes policies | Legislature writing laws |

**Request flow:**
1. User attempts to access a resource
2. PEP intercepts the request and creates a decision request
3. PEP sends request to PDP
4. PDP identifies applicable policies
5. PDP asks PIP for attribute values:
   - "What is Alice's department?"
   - "What is the file's classification?"
   - "What time is it?"
   - "Is Alice's device managed?"
6. PIP queries identity stores, resource metadata, device management systems
7. PDP evaluates policies using retrieved attributes
8. PDP returns decision: PERMIT, DENY, or NOT_APPLICABLE
9. PEP enforces the decision (allow or block access)
10. PEP logs the decision for audit

### Policy Evaluation and Conflict Resolution

When multiple policies apply to a request, conflicts can occur (one says ALLOW, another says DENY). XACML defines several algorithms:

| Algorithm | Behavior | When to Use |
|-----------|----------|-------------|
| **Deny-overrides** | Any DENY → final DENY | Most secure default |
| **Permit-overrides** | Any ALLOW → final ALLOW | Permissive environments |
| **First-applicable** | First matching policy wins | Ordered policy lists |
| **Only-one-applicable** | Error if multiple policies match | Strict governance |

**Why deny-overrides is the secure default:** If you have 100 ALLOW policies and 1 DENY policy, and the DENY applies, the access should be blocked. This is defense in depth.

### ABAC in Cloud Platforms

**AWS IAM with conditions:**
```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::company-bucket/*",
  "Condition": {
    "StringEquals": {
      "aws:RequestedRegion": "us-east-1",
      "s3:x-amz-acl": "bucket-owner-full-control"
    },
    "IpAddress": {
      "aws:SourceIp": "203.0.113.0/24"
    },
    "Bool": {
      "aws:MultiFactorAuthPresent": "true"
    },
    "DateGreaterThan": {
      "aws:CurrentTime": "2024-01-01T00:00:00Z"
    }
  }
}
```

**Azure AD Conditional Access:**
- IF user.riskLevel == "high" → Require MFA
- IF device.trustType != "Azure AD joined" → Block access
- IF location.country NOT IN ["US", "CA"] → Require manager approval
- IF application.name == "Sensitive App" → Require compliant device

---

## Where You See It

| Product | ABAC Feature | Example |
|---------|-------------|---------|
| **AWS IAM** | Policy conditions | Restrict S3 access by IP, region, MFA status |
| **Azure AD** | Conditional Access | Require MFA for risky sign-ins, block non-compliant devices |
| **Google Cloud IAM** | IAM conditions | Time-bound access, resource tag conditions |
| **Okta** | Device posture | Block access from unmanaged devices |
| **XACML engines** | Full ABAC | Enterprise policy management |
| **OPA (Open Policy Agent)** | Policy as code | Kubernetes, microservices authorization |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "ABAC replaces RBAC" | Most organizations use both: RBAC for coarse-grained, ABAC for fine-grained constraints |
| "ABAC is too slow for production" | Modern PDPs evaluate ABAC policies in milliseconds; caching further improves performance |
| "ABAC is impossible to audit" | ABAC generates detailed decision logs showing every attribute evaluated; often more auditable than RBAC |
| "Any attribute can be used in ABAC" | Attributes must be reliable, tamper-proof, and available at decision time. Untrusted attributes weaken security. |
| "ABAC is only for cloud" | ABAC applies to any environment where context matters, including on-premises and hybrid |

---

## How to Practice

### Exercise 1: Write an ABAC Policy
Write an ABAC policy for this scenario:
> Contractors in the Engineering department can read project documentation from corporate laptops between 9 AM and 6 PM. They cannot access production systems. Full-time employees can access production systems from any managed device at any time.

Identify all subject, resource, action, and environment attributes.

### Exercise 2: Compare RBAC and ABAC
For a 500-person company with remote workers:
1. Count how many RBAC roles you would need
2. Count how many ABAC policies you would need
3. Document which model is simpler for administration
4. Document which model is more flexible for edge cases

### Exercise 3: Debug an ABAC Denial
Alice is denied access to a file. The ABAC policy says:
```
ALLOW IF user.department == resource.owner_department
       AND user.clearance >= resource.classification
       AND environment.time.hour >= 9
       AND environment.time.hour <= 17
```

Alice's attributes:
- department: Engineering
- clearance: 3

File attributes:
- owner_department: Engineering
- classification: 2

Access attempt: 8:30 PM

Why was Alice denied? What are three ways to resolve this?

### Exercise 4: Run the Simulations
- `abac_policy_evaluator.py` — Evaluate policies against requests
- `abac_vs_rbac_comparator.py` — Compare administrative overhead

---

## Projects

### `abac_policy_evaluator.py`
Evaluates ABAC policies against access requests:
- Defines subjects, resources, actions, environment attributes
- Parses Boolean policy expressions with AND/OR/NOT
- Resolves policy conflicts using configurable algorithms
- Returns PERMIT/DENY/NOT_APPLICABLE with explanation

### `abac_vs_rbac_comparator.py`
Compares ABAC and RBAC for identical scenarios:
- Shows how RBAC requires many roles for the same result
- Demonstrates ABAC flexibility with fewer policies
- Calculates administrative overhead metrics
- Provides visual comparison

### `xacml_policy_generator.py`
Generates XACML-compliant policy XML:
- Creates policies from simple rule definitions
- Validates policy syntax against XACML schema
- Exports for import into XACML engines

---

## Check Your Understanding

1. Name the four attribute categories in ABAC. For each, provide three specific examples relevant to a financial services company.
2. Write an ABAC policy that allows database administrators to modify production databases only during maintenance windows (Saturdays 2-6 AM), from corporate laptops, with MFA enabled.
3. Why is ABAC more flexible than RBAC? In what situations would this flexibility be a disadvantage rather than an advantage?
4. What is XACML? Describe the roles of PEP, PDP, PIP, and PAP, and trace a complete access request through the architecture.
5. How does "deny-overrides" conflict resolution work? Why is it considered the most secure default? When might you choose a different algorithm?
6. A company uses RBAC with 200 roles. After migrating to ABAC, they have 40 policies. What benefits did they gain? What challenges might they face?
7. Design a hybrid RBAC+ABAC system for a university: Students, Faculty, Staff, and Administrators need different access to course materials, financial systems, and research data. Define the RBAC roles and the ABAC constraints.
8. In ABAC, what happens if an attribute source (PIP) is unavailable? How should the system handle missing attributes?
9. Compare AWS IAM conditions, Azure AD Conditional Access, and Google Cloud IAM conditions. What similarities and differences exist?
10. An ABAC policy has a bug that allows unintended access. How would you detect, diagnose, and fix this bug? What tools and processes would you use?
