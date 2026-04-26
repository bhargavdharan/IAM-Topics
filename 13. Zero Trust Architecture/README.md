# 13. Zero Trust Architecture

## What Is Zero Trust?

**Zero Trust** is a security framework and mindset that assumes no user, device, or network location should be implicitly trusted — regardless of whether they are inside or outside the organizational network. Every access request must be verified, authenticated, and authorized before access is granted.

The traditional model assumed: "Inside the network = trusted. Outside the network = untrusted." Zero Trust rejects this assumption. Attackers who breach the perimeter should not automatically gain access to everything inside.

The core principle of Zero Trust is **"Never trust, always verify."**

---

## Why Learn This?

Modern IT environments have eroded the traditional network perimeter:
- Remote work connects users from home networks, coffee shops, airports
- Cloud services exist outside the corporate data center
- Mobile devices access corporate data from anywhere
- Partners and contractors need access without VPNs
- Insiders with legitimate access can be threats

Understanding Zero Trust is essential for:
- Designing modern security architectures
- Protecting cloud-native applications
- Implementing least privilege at scale
- Reducing blast radius of breaches
- Meeting evolving compliance requirements

---

## Core Concepts

### The Three Pillars of Zero Trust

**1. Verify Explicitly**
Every access request must be authenticated and authorized based on all available data:
- User identity
- Device health and compliance
- Location
- Risk signals
- Request context

No access is granted based on network location alone.

**2. Use Least Privilege Access**
Users and systems receive only the minimum access needed, and only for the time needed:
- Just-in-time access
- Just-enough-access (role-based, attribute-based)
- Time-limited permissions
- Continuous verification

**3. Assume Breach**
Design systems as if an attacker is already inside:
- Segment networks to limit lateral movement
- Encrypt all data in transit and at rest
- Monitor everything for anomalies
- Minimize blast radius

### Zero Trust Architecture Components

| Component | Function | Example |
|-----------|----------|---------|
| **Identity Provider** | Authenticates users and issues tokens | Azure AD, Okta, Ping |
| **Device Directory** | Manages and assesses device compliance | Microsoft Intune, Jamf, VMware Workspace ONE |
| **Policy Engine** | Evaluates access requests against policies | Azure AD Conditional Access, Okta Policies |
| **Policy Administrator** | Enforces policy decisions | WAF, application gateway, proxy |
| **Signal Collection** | Gathers risk signals | Endpoint detection, threat intelligence, user behavior |

### The Zero Trust Control Plane

```
                    ┌─────────────────────┐
                    │   Access Request    │
                    │ (User + Device +    │
                    │  Resource + Context)│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Policy Engine     │
                    │  Evaluates signals: │
                    │  - Identity valid?  │
                    │  - Device healthy?  │
                    │  - Location normal? │
                    │  - Risk score?      │
                    │  - MFA required?    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │    Decision         │
                    │  Allow / Deny /     │
                    │  Step-up Auth /     │
                    │  Limited Access     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Access Granted    │
                    │  with conditions:   │
                    │  - Session timeout  │
                    │  - Scope limits     │
                    │  - Monitoring active│
                    └─────────────────────┘
```

### Identity in Zero Trust

Identity is the primary security perimeter in Zero Trust:
- **Strong authentication:** MFA required for all users, all the time
- **Dynamic authorization:** Access decisions based on real-time risk
- **Privileged access protection:** PAM integrated into Zero Trust
- **Continuous authentication:** Re-evaluate trust throughout the session

### Device Trust

Zero Trust requires knowing and trusting the device:

| Device Signal | What It Tells You | Risk If Missing |
|--------------|-------------------|-----------------|
| **Compliance status** | Device meets security policy (patched, encrypted, managed) | Outdated, vulnerable device accessing data |
| **Health attestation** | No malware detected, no suspicious processes | Compromised device used to steal data |
| **Location** | Device is where user is expected to be | Stolen device or VPN bypass |
| **Certificate** | Device is corporate-issued and registered | Personal, unmanaged device |

### Micro-Segmentation

Micro-segmentation divides the network into small, isolated zones:
- Each application or workload has its own security boundary
- East-west traffic (within the network) is controlled
- Even if an attacker breaches one segment, they cannot move laterally
- Policies define exactly which services can communicate

**Example:**
```
Traditional:  [Internet] → [Firewall] → [Trusted Internal Network]
                                              (Everything accessible)

Zero Trust:   [Internet] → [Firewall] → [Web Tier] → [App Tier] → [DB Tier]
                           Each tier isolated; only allowed connections
```

---

## How It Works

### Continuous Authentication

Zero Trust does not authenticate once and forget. Trust is continuously re-evaluated:

| Trigger | Action |
|---------|--------|
| User switches device | Re-authenticate and re-assess device trust |
| Device becomes non-compliant | Block or limit access until compliance restored |
| Anomalous behavior detected | Require step-up authentication or block |
| Session timeout | Re-authenticate |
| Risk score increases | Restrict access, require MFA, or terminate session |
| Location changes unexpectedly | Flag for review, require additional verification |

### Conditional Access Policies

Conditional Access is Microsoft's implementation of Zero Trust policy evaluation:

**Policy structure:**
```
IF (user is in Finance group)
   AND (device is compliant)
   AND (location is trusted)
   AND (risk score is low)
THEN allow access to FinanceApp
     require MFA
     session expires in 4 hours
ELSE block access
     OR require password reset
     OR allow limited read-only access
```

**Common conditions:**
- User or group membership
- Device platform (iOS, Android, Windows, macOS)
- Device compliance status
- Location (IP range, country, GPS)
- Client application
- Sign-in risk (real-time risk score)
- User risk (historical risk assessment)

### Zero Trust Network Access (ZTNA)

ZTNA replaces traditional VPNs:

**Traditional VPN:**
- User connects to VPN concentrator
- User is "inside" the network
- User can access many internal resources
- No per-application authorization

**ZTNA:**
- User connects to specific application through broker
- Each application requires separate authorization
- User never joins the corporate network
- Access is granted per-application, per-session
- All traffic is encrypted and logged

**Benefits:**
- Reduced attack surface (no broad network access)
- Better visibility (all access logged)
- No need to manage VPN infrastructure
- Works from anywhere without network-level trust

---

## Where You See It

| Product | Zero Trust Capability | Use Case |
|---------|----------------------|----------|
| **Microsoft Azure AD** | Conditional Access, Identity Protection | Device compliance, risk-based policies |
| **Zscaler Private Access** | ZTNA platform | Application-specific access without VPN |
| **Cloudflare Access** | ZTNA and Zero Trust network | Per-application access policies |
| **Google BeyondCorp** | Google's Zero Trust model | Device trust, context-aware access |
| **Okta Identity Engine** | Risk-based policies, device trust | Adaptive authentication |
| **Cisco Secure Access** | SD-Access with Zero Trust | Network micro-segmentation |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Zero Trust means trusting no one" | Zero Trust means "verify explicitly" before granting trust, not "deny everything." |
| "Zero Trust replaces VPN" | Zero Trust principles can be implemented via ZTNA, which replaces VPN for many use cases. |
| "Zero Trust is only for large enterprises" | Organizations of any size can implement Zero Trust principles: MFA, least privilege, device management. |
| "Zero Trust is a product you buy" | Zero Trust is a strategy and architecture. Products enable it, but mindset and policy are essential. |
| "Zero Trust means zero access" | Users still get access — but access is based on verification, not assumed from network location. |
| "Implementing Zero Trust is all-or-nothing" | Zero Trust is a journey. Start with MFA, then add device compliance, then micro-segmentation. |

---

## How to Practice

### Exercise 1: Assess Your Organization's Zero Trust Maturity
Rate your organization on these dimensions (1-5 scale):
- Identity: MFA deployment, passwordless readiness, identity protection
- Devices: Device management coverage, compliance enforcement, health attestation
- Applications: SSO adoption, session management, application protection
- Network: Micro-segmentation, encryption, ZTNA vs VPN
- Data: Classification, encryption, DLP

Identify the highest-impact improvements.

### Exercise 2: Design a Conditional Access Policy
Design a policy for a financial analyst accessing a trading application:
- What identity requirements? (MFA, passwordless?)
- What device requirements? (Compliant, managed, specific OS?)
- What location requirements? (Office only? Trusted countries?)
- What risk considerations? (Real-time risk, user risk?)
- What session controls? (Timeout, continuous access evaluation?)

### Exercise 3: Map Attack Scenarios
Consider these attack scenarios and how Zero Trust mitigates each:
1. Phished credentials used to log in from abroad
2. Compromised device connects to corporate application
3. Insider attempts to access data outside their role
4. Attacker breaches one server and tries lateral movement
5. Stolen session cookie used from different device

### Exercise 4: Run the Simulations
- `zero_trust_engine.py` — Policy evaluation simulation
- `device_trust_scorer.py` — Device compliance assessment
- `micro_segment_sim.py` — Network micro-segmentation

---

## Projects

### `zero_trust_engine.py`
Simulates Zero Trust policy evaluation:
- Multiple policy conditions (identity, device, location, risk)
- Continuous authentication triggers
- Decision outcomes: Allow, Block, Step-up, Limited
- Audit logging of all decisions
- Signal aggregation from multiple sources

### `device_trust_scorer.py`
Assesses device compliance for Zero Trust:
- Checks device attributes (OS version, patch level, encryption)
- Evaluates against compliance policy
- Calculates trust score
- Recommends remediation actions
- Simulates health attestation

### `micro_segment_sim.py`
Models network micro-segmentation:
- Defines network segments (web, app, database)
- Specifies allowed traffic flows
- Simulates lateral movement attempts
- Evaluates blast radius of breaches
- Demonstrates segmentation policy enforcement

---

## Check Your Understanding

1. What is the fundamental difference between traditional network security and Zero Trust? Why did the traditional model become insufficient?
2. What are the three pillars of Zero Trust? Explain each with a concrete example.
3. How does micro-segmentation prevent lateral movement? Compare a flat network with a micro-segmented network after a breach.
4. What is ZTNA and how does it differ from traditional VPN? What are the security benefits?
5. How does continuous authentication work in Zero Trust? Give three examples of triggers that would cause re-evaluation.
6. Design a Conditional Access policy for a healthcare worker accessing patient records from a personal tablet at home.
7. Why is identity considered the primary security perimeter in Zero Trust? What does this mean for authentication requirements?
8. Describe how Zero Trust would handle these scenarios differently from traditional security:
   a. An employee working from a coffee shop
   b. A contractor accessing a specific application
   c. A server in the data center calling an API
9. What are the phases of a Zero Trust implementation journey? What would you implement first, second, and third?
10. An attacker steals valid credentials and tries to log in from a new device in a different country. How would a Zero Trust architecture respond at each layer?
