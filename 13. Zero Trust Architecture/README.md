# 13. Zero Trust Architecture

## What Is Zero Trust?

**Zero Trust** is a security model that eliminates the concept of a trusted network. Instead of assuming that everything inside the corporate network is safe, Zero Trust verifies every user, device, and transaction — every single time.

The core principle is simple: **Never trust, always verify.**

---

## Why Learn This?

The traditional security model — a strong perimeter with free movement inside — no longer works. Cloud services, remote work, and mobile devices have dissolved the perimeter. Attackers who breach the perimeter can move freely inside.

Zero Trust addresses this by:
- Eliminating implicit trust based on network location
- Enforcing least privilege at every step
- Assuming breaches and designing for containment

---

## Core Concepts

### The Three Principles of Zero Trust

| Principle | Meaning | Application |
|-----------|---------|-------------|
| **Verify Explicitly** | Always authenticate and authorize based on all available data | Check identity, device health, and behavior on every request |
| **Use Least Privilege Access** | Grant only the minimum access needed, and only for the required time | Just-in-time access, time-limited tokens |
| **Assume Breach** | Design as if attackers are already inside | Micro-segmentation, continuous monitoring |

### Zero Trust Tenets (NIST SP 800-207)

1. All data sources and computing services are resources
2. All communication is secured regardless of network location
3. Access to individual resources is granted on a per-session basis
4. Access is determined by dynamic policy
5. The enterprise monitors and measures the integrity and security posture of all assets
6. All resource authentication and authorization are dynamic and strictly enforced
7. The enterprise collects as much information as possible for analysis

### Continuous Verification

Traditional security: Verify once at login, then trust.
Zero Trust: Verify continuously.

| Signal | Low Trust | High Trust |
|--------|-----------|------------|
| **Device** | Personal tablet, no antivirus | Corporate laptop, fully patched |
| **Location** | Unknown country | Known office or home |
| **Behavior** | Downloading entire database | Normal work patterns |
| **Time** | 3 AM on weekend | 10 AM on weekday |
| **MFA** | None | Hardware key + biometric |

**Result:** Low trust score → Step-up authentication or deny. High trust score → Smooth access.

### Micro-Segmentation

Instead of one big network, create many small isolated zones. If an attacker breaches the web server, they cannot reach the database without passing additional checks.

---

## How It Works

### The Policy Decision Point (PDP)

The PDP is the brain of Zero Trust. For every access request, it evaluates:
- Identity strength (MFA method, risk score)
- Device health (managed, compliant, patched)
- Context (location, time, network)
- Resource sensitivity

**Example scoring:**
```
Hardware key auth: +20 points
Managed device: +15 points
Corporate network: +10 points
Business hours: +10 points
High-risk user: -20 points
Unmanaged device: -15 points

Score >= 80: ALLOW
Score 50-79: STEP_UP_AUTH
Score < 50: DENY
```

### Software-Defined Perimeter (SDP)

SDP replaces traditional VPNs:
- Each application is invisible until authenticated
- No broad network access granted
- Traffic routed optimally, not through corporate HQ
- Every session continuously monitored

---

## Where You See It

| Product | Zero Trust Feature |
|---------|-------------------|
| **Microsoft Azure AD** | Conditional Access policies |
| **Google BeyondCorp** | Context-aware access |
| **Zscaler** | Zero Trust Network Access |
| **Okta Identity Engine** | Risk-based authentication |
| **VMware NSX** | Micro-segmentation |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Zero Trust means zero access" | Zero Trust means verify before trusting, not block everything |
| "Zero Trust is a product" | Zero Trust is an architecture and mindset, not a single tool |
| "We need to replace everything" | Zero Trust is typically implemented incrementally |
| "Zero Trust is only for cloud" | Zero Trust applies to on-premises, cloud, and hybrid environments |

---

## How to Practice

1. **Evaluate your current trust model**
   - Do you trust devices based on network location?
   - Do you verify identity on every resource access?
   - What happens if an attacker gets inside your network?

2. **Design a Zero Trust policy for one application**
   - Define the required trust score
   - List the signals you would evaluate
   - Determine what happens when trust is low

3. **Run the simulations**
   - `zero_trust_engine.py` evaluates trust scores
   - `micro_segment_sim.py` demonstrates network segmentation

---

## Projects

### `zero_trust_engine.py`
Implements a Zero Trust policy engine:
- Evaluates trust scores based on identity, device, and context
- Makes dynamic access decisions
- Implements continuous verification

### `device_trust_scorer.py`
Scores device trustworthiness:
- Checks management enrollment
- Verifies compliance status
- Generates device risk scores

### `micro_segment_sim.py`
Simulates network micro-segmentation:
- Creates isolated network zones
- Enforces zone-to-zone policies
- Simulates lateral movement attacks

### `continuous_auth_monitor.py`
Monitors sessions for risk changes:
- Detects anomalous behavior mid-session
- Triggers re-authentication when risk increases

---

## Check Your Understanding

1. What is the core principle of Zero Trust? How does it differ from perimeter-based security?
2. Name the three pillars of Zero Trust and explain each.
3. What is micro-segmentation and how does it limit breach impact?
4. How does continuous verification work? Give an example of when access might be revoked mid-session.
5. What is a Software-Defined Perimeter and how is it better than a traditional VPN?
