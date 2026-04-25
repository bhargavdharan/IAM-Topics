# 13. Zero Trust Architecture

## 🏠 Real-World Analogy: The High-Security Laboratory

Imagine a top-secret research laboratory:

**Old approach (Perimeter-based):**
- One big fence around the facility
- Guard checks your ID at the gate
- Once inside, you can go anywhere
- If someone sneaks past the gate, they have free rein

**Zero Trust approach:**
- Every room has its own biometric scanner
- Even after entering the building, you must re-authenticate for each room
- The system checks: Who are you? What device? What time? What's your clearance?
- Cameras watch every movement
- If you act suspiciously, access is immediately revoked
- No one is trusted by default — not even the director

**Zero Trust: "Never trust, always verify."**

---

## 📋 Overview

Zero Trust is a security paradigm that eliminates the concept of a trusted network. Instead of assuming everything inside the corporate network is safe, Zero Trust verifies every user, device, and transaction — every single time.

**Why Zero Trust emerged:**
- Perimeters dissolved (cloud, remote work, mobile devices)
- Insider threats are as dangerous as external attacks
- "Trusted" networks were being breached regularly
- Once inside, attackers moved laterally with ease

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain Zero Trust with real-world analogies
- Describe the three core principles of Zero Trust
- Understand the concepts of micro-segmentation and least privilege access
- Explain continuous verification and conditional access
- Implement a basic Zero Trust policy engine

---

## 📚 Key Concepts

### The Three Pillars of Zero Trust

| Pillar | Principle | Real-World Analogy |
|--------|-----------|-------------------|
| **Verify Explicitly** | Always authenticate and authorize based on all available data | Biometric scan + ID check + security question at every door |
| **Use Least Privilege Access** | Grant only the minimum access needed, just-in-time | Temporary elevator pass for one floor, one hour |
| **Assume Breach** | Design as if attackers are already inside | Vault within a vault within a vault |

### Zero Trust Tenets (NIST SP 800-207)

1. **All data sources and computing services are considered resources.**
   - Your laptop, a cloud database, and a printer are all resources requiring protection.

2. **All communication is secured regardless of network location.**
   - Whether you're in the office or at a coffee shop, the same security applies.

3. **Access to individual enterprise resources is granted on a per-session basis.**
   - Access to email doesn't mean access to the financial database.

4. **Access to resources is determined by dynamic policy.**
   - Policy considers user identity, device health, behavior, and threat intelligence.

5. **The enterprise monitors and measures the integrity and security posture of all owned and associated assets.**
   - Every device is continuously scanned for vulnerabilities.

6. **All resource authentication and authorization are dynamic and strictly enforced before access is allowed.**
   - No "trust this device for 30 days" shortcuts.

7. **The enterprise collects as much information as possible about the current state of assets, network infrastructure, and communications.**
   - Comprehensive logging for analysis and improvement.

### Zero Trust Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Zero Trust Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│   │   Identity  │    │   Device    │    │ Application │   │
│   │  (Who)      │    │  (What)     │    │  (How)      │   │
│   │             │    │             │    │             │   │
│   │ - User      │    │ - Managed?  │    │ - Allowed   │   │
│   │ - Group     │    │ - Compliant?│    │   actions   │   │
│   │ - Risk      │    │ - Location  │    │ - Data      │   │
│   │   score     │    │ - Health    │    │   access    │   │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘   │
│          │                  │                  │            │
│          └──────────────────┼──────────────────┘            │
│                             ▼                               │
│                  ┌─────────────────────┐                    │
│                  │   Policy Engine     │                    │
│                  │   (Decision Point)  │                    │
│                  └──────────┬──────────┘                    │
│                             │                               │
│                             ▼                               │
│                  ┌─────────────────────┐                    │
│                  │   Access Decision   │                    │
│                  │   ALLOW / DENY      │                    │
│                  └─────────────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Continuous Verification

Traditional security: Verify once at login, then trust.
Zero Trust: Verify continuously.

| Signal | Low Trust Score | High Trust Score |
|--------|----------------|-----------------|
| **Device** | Personal tablet, no antivirus | Corporate laptop, fully patched |
| **Location** | Logging in from unusual country | Logging in from home office |
| **Behavior** | Downloading entire database | Normal work patterns |
| **Time** | 3 AM on a weekend | 10 AM on a weekday |
| **MFA** | No MFA used | Hardware key + biometric |

**Result:** Low trust score → Step-up authentication or deny access. High trust score → Smooth access.

### Micro-Segmentation

Instead of one big network, create many small isolated zones:

```
Traditional Network:                    Zero Trust Network:
┌──────────────────┐                    ┌──┐┌──┐┌──┐┌──┐┌──┐
│                  │                    │  ││  ││  ││  ││  │
│  Everything      │                    │Web││App││DB ││HR ││Fin│
│  together        │                    │  ││  ││  ││  ││  │
│                  │                    └──┘└──┘└──┘└──┘└──┘
└──────────────────┘                    Each zone isolated by policy
```

If an attacker breaches the web server, they cannot reach the database without passing additional checks.

---

## 🔧 Under the Hood

### The Policy Decision Point (PDP)

The PDP is the "brain" of Zero Trust. For every access request, it evaluates:

```python
def evaluate_access_request(request):
    trust_score = 0
    
    # Identity verification
    if request.user.authenticated_with_mfa:
        trust_score += 30
    if request.user.risk_level == "low":
        trust_score += 20
    
    # Device verification
    if request.device.managed and request.device.compliant:
        trust_score += 25
    if request.device.healthy (no malware, patched):
        trust_score += 15
    
    # Context verification
    if request.location == "corporate_office":
        trust_score += 5
    if request.time.within_business_hours:
        trust_score += 5
    
    # Decision
    if trust_score >= 80:
        return ALLOW
    elif trust_score >= 50:
        return STEP_UP_AUTH  # Require additional verification
    else:
        return DENY
```

### Device Trust Scoring

How do we know a device is trustworthy?

| Check | How It's Verified | Failure Consequence |
|-------|-------------------|---------------------|
| **Managed** | Device enrolled in MDM (Intune, Jamf) | Block access |
| **Compliant** | Meets policy (encryption, password, OS version) | Quarantine network |
| **Healthy** | EDR scan shows no malware | Remediate before access |
| **Certificate** | Device presents valid client certificate | Prompt for MFA |

### Software-Defined Perimeter (SDP)

SDP replaces traditional VPNs:

**Traditional VPN:**
- Connect to corporate network → access everything
- Broad attack surface
- Poor performance (backhaul all traffic)

**SDP (Zero Trust Network Access):**
- Each application is invisible until authenticated
- No network access granted — only application access
- Traffic routed optimally (not through corporate HQ)
- Continuous monitoring of every session

---

## 🛠️ Projects in This Module

### `zero_trust_engine.py`
Implements a Zero Trust policy engine:
- Evaluates trust scores based on identity, device, and context
- Makes dynamic access decisions
- Implements continuous verification
- Logs all decisions for analysis

### `device_trust_scorer.py`
Scores device trustworthiness:
- Checks management enrollment
- Verifies compliance status
- Scans for security health
- Generates device risk scores

### `micro_segment_sim.py`
Simulates network micro-segmentation:
- Creates isolated network zones
- Enforces zone-to-zone policies
- Simulates lateral movement attacks
- Demonstrates containment benefits

### `continuous_auth_monitor.py`
Monitors sessions for risk changes:
- Detects anomalous behavior mid-session
- Triggers re-authentication when risk increases
- Blocks suspicious actions in real-time
- Generates threat intelligence reports

---

## 📝 Quiz Questions

1. **What is the core principle of Zero Trust? How does it differ from traditional perimeter-based security?**
2. **Name the three pillars of Zero Trust and explain each with an analogy.**
3. **What is micro-segmentation and how does it limit the impact of a breach?**
4. **How does continuous verification work? Give an example of when access might be revoked mid-session.**
5. **What is a Software-Defined Perimeter (SDP) and how is it better than a traditional VPN?**

---

## 🔗 Further Reading

- [NIST SP 800-207 - Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [Google BeyondCorp Whitepaper](https://cloud.google.com/beyondcorp)
- [Microsoft Zero Trust Architecture Guide](https://docs.microsoft.com/en-us/security/zero-trust/)

---

## 🏷️ Tags
`#ZeroTrust` `#NeverTrustAlwaysVerify` `#MicroSegmentation` `#ContinuousVerification` `#SDP` `#ZTNA`
