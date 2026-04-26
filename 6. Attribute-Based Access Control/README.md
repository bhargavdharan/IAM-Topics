# 6. Attribute-Based Access Control (ABAC)

## What Is ABAC?

**Attribute-Based Access Control (ABAC)** is an authorization model where access decisions are based on attributes of the user, the resource, the action, and the environment. Rather than asking "What role do you have?" (RBAC), ABAC asks "What are your attributes, the resource's attributes, and the current context?"

This enables fine-grained, dynamic access control that adapts to real-time conditions.

---

## Why Learn This?

Modern work is dynamic: remote employees, contractors, project-based teams, and cloud resources that spin up and down instantly. RBAC struggles with this complexity because roles are static. ABAC addresses this by making access decisions based on current context.

Understanding ABAC enables you to:
- Design context-aware security policies
- Implement fine-grained cloud IAM policies
- Build systems that adapt to risk signals
- Understand modern policy engines

---

## Core Concepts

### The Four Attribute Categories

ABAC evaluates four types of attributes for every access request:

| Category | Description | Examples |
|----------|-------------|----------|
| **Subject** | Who is requesting access | Department, job title, clearance level, certifications |
| **Resource** | What is being accessed | Classification, owner, data type, location |
| **Action** | What operation is being attempted | Read, write, delete, approve |
| **Environment** | The context of the request | Time, location, device type, network, threat level |

### ABAC Policy Examples

```
POLICY 1:
IF user.department == "Finance"
AND resource.type == "financial_report"
AND action == "read"
AND environment.time.hour BETWEEN 9 AND 17
AND environment.network == "corporate"
THEN ALLOW

POLICY 2:
IF user.type == "contractor"
AND resource.classification == "confidential"
THEN DENY

POLICY 3:
IF device.managed == false
AND resource.sensitivity >= 4
THEN DENY
```

### ABAC vs RBAC

| Factor | RBAC | ABAC |
|--------|------|------|
| Basis of decision | Static role assignments | Dynamic attributes |
| Complexity | Lower | Higher |
| Flexibility | Less (roles change slowly) | More (context-aware) |
| Performance | Faster (simple lookup) | Slower (evaluate expressions) |
| Context awareness | No | Yes (time, location, device) |
| Example rule | "Developers can read code" | "Developers can read code IF on corporate laptop AND during business hours" |

**When to use RBAC:** Small to medium organizations with stable job functions.
**When to use ABAC:** Large enterprises, remote work, cloud environments, or any situation where context matters.
**Best practice:** Use RBAC for coarse-grained access and ABAC for fine-grained constraints.

---

## How It Works

### XACML Architecture

XACML (eXtensible Access Control Markup Language) is the standard for ABAC. The architecture separates concerns into four components:

| Component | Role | Analogy |
|-----------|------|---------|
| **PEP** (Policy Enforcement Point) | Intercepts access requests | Security guard at the door |
| **PDP** (Policy Decision Point) | Evaluates policies and decides | Judge making a ruling |
| **PIP** (Policy Information Point) | Provides attribute values | Court clerk fetching records |
| **PAP** (Policy Administration Point) | Creates and manages policies | Legislature writing laws |

**How a request flows:**
1. A user tries to open a file
2. The PEP intercepts the request
3. The PDP looks up policies and asks the PIP for attributes
4. The PIP fetches: user's department, file's classification, current time, device status
5. The PDP evaluates all policies and returns PERMIT, DENY, or NOT_APPLICABLE
6. The PEP enforces the decision

### Policy Evaluation Logic

ABAC policies use Boolean logic:
- **AND:** All conditions must be true
- **OR:** At least one condition must be true
- **NOT:** Condition must be false

**Conflict resolution:** What if one policy says ALLOW and another says DENY?
- **Deny-overrides:** If any policy says DENY, the result is DENY (most secure default)
- **Permit-overrides:** If any policy says ALLOW, the result is ALLOW
- **First-applicable:** First matching policy wins
- **Only-one-applicable:** Error if multiple policies match

### ABAC in the Real World

**AWS IAM Policies:**
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

**Azure AD Conditional Access:**
- IF user.riskLevel == "high" → Require MFA
- IF device.compliance == "noncompliant" → Block access
- IF location.country NOT IN ["US", "CA"] → Require approval

---

## Where You See It

| System | ABAC Feature | Example |
|--------|-------------|---------|
| **AWS IAM** | Policy conditions | Restrict S3 access by IP and region |
| **Azure AD** | Conditional Access | Require MFA for risky sign-ins |
| **Google Cloud IAM** | Conditions | Time-bound access to resources |
| **Okta** | Device posture | Block access from unmanaged devices |
| **XACML implementations** | Full ABAC engine | Enterprise policy management |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "ABAC replaces RBAC" | Most organizations use both: RBAC for coarse-grained, ABAC for fine-grained |
| "ABAC is too slow" | Modern policy engines evaluate ABAC in milliseconds |
| "ABAC is hard to audit" | ABAC generates detailed decision logs, often more auditable than RBAC |
| "Any attribute can be used" | Attributes must be reliable, tamper-proof, and available at decision time |

---

## How to Practice

1. **Write an ABAC policy for a real scenario**
   - Scenario: Contractors should only access project files during business hours from company devices
   - Identify subject, resource, action, and environment attributes
   - Write the policy using Boolean logic

2. **Compare RBAC and ABAC for the same scenario**
   - Count how many roles RBAC would need
   - Count how many policies ABAC would need
   - Document the trade-offs

3. **Run the simulations**
   - `abac_policy_evaluator.py` evaluates ABAC policies against requests
   - `abac_vs_rbac_comparator.py` shows administrative overhead differences

---

## Projects

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

## Check Your Understanding

1. Name the four attribute categories in ABAC and give two examples of each.
2. Write an ABAC policy that allows access ONLY during business hours from company devices.
3. Why is ABAC more flexible than RBAC? What is the trade-off?
4. What is XACML? Describe the roles of PEP, PDP, PIP, and PAP.
5. How does "deny-overrides" conflict resolution work? Why is it the most secure default?
