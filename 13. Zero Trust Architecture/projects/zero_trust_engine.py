#!/usr/bin/env python3
"""
Zero Trust Policy Engine
========================
Implements a Zero Trust policy engine that evaluates
trust scores and makes dynamic access decisions.

Run: python zero_trust_engine.py
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class Decision(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    STEP_UP = "STEP_UP_AUTH"
    QUARANTINE = "QUARANTINE"


@dataclass
class Device:
    device_id: str
    managed: bool
    compliant: bool
    healthy: bool  # No malware, patched
    has_certificate: bool


@dataclass
class Environment:
    location: str  # office, home, public, unknown
    network: str   # corporate, vpn, public_wifi
    threat_level: str  # low, medium, high
    time_hour: int


@dataclass
class Identity:
    username: str
    auth_method: str  # password, mfa, hardware_key
    risk_score: int   # 0-100 from identity provider
    failed_attempts_1h: int


class ZeroTrustEngine:
    """Evaluates Zero Trust access requests."""
    
    def __init__(self):
        self.policies = []
    
    def calculate_trust_score(self, identity: Identity, device: Device, 
                             env: Environment, resource_sensitivity: int) -> Dict:
        """Calculate overall trust score (0-100)."""
        score = 0
        factors = []
        
        # Identity factors (max 40 points)
        if identity.auth_method == "hardware_key":
            score += 20
            factors.append("Hardware key auth (+20)")
        elif identity.auth_method == "mfa":
            score += 15
            factors.append("MFA auth (+15)")
        elif identity.auth_method == "password":
            score += 5
            factors.append("Password only (+5)")
        
        if identity.risk_score < 20:
            score += 20
            factors.append("Low identity risk (+20)")
        elif identity.risk_score < 50:
            score += 10
            factors.append("Medium identity risk (+10)")
        else:
            factors.append("High identity risk (+0)")
        
        # Device factors (max 30 points)
        if device.managed:
            score += 10
            factors.append("Managed device (+10)")
        if device.compliant:
            score += 10
            factors.append("Compliant device (+10)")
        if device.healthy:
            score += 10
            factors.append("Healthy device (+10)")
        
        # Environment factors (max 20 points)
        if env.location == "office":
            score += 10
            factors.append("Office location (+10)")
        elif env.location == "home":
            score += 5
            factors.append("Home location (+5)")
        
        if env.network == "corporate":
            score += 10
            factors.append("Corporate network (+10)")
        elif env.network == "vpn":
            score += 5
            factors.append("VPN (+5)")
        
        # Time factor (max 10 points)
        if 9 <= env.time_hour <= 17:
            score += 10
            factors.append("Business hours (+10)")
        else:
            score += 2
            factors.append("After hours (+2)")
        
        # Resource sensitivity penalty
        sensitivity_penalty = (resource_sensitivity - 1) * 5
        score -= sensitivity_penalty
        if sensitivity_penalty > 0:
            factors.append(f"Resource sensitivity penalty (-{sensitivity_penalty})")
        
        # Failed attempts penalty
        if identity.failed_attempts_1h > 3:
            score -= 20
            factors.append("Recent failures (-20)")
        
        # Threat level
        if env.threat_level == "high":
            score -= 15
            factors.append("High threat environment (-15)")
        elif env.threat_level == "medium":
            score -= 5
            factors.append("Medium threat environment (-5)")
        
        final_score = max(0, min(100, score))
        
        return {
            "score": final_score,
            "factors": factors,
            "level": self._get_level(final_score)
        }
    
    def _get_level(self, score: int) -> str:
        if score >= 80:
            return "HIGH_TRUST"
        elif score >= 60:
            return "MEDIUM_TRUST"
        elif score >= 40:
            return "LOW_TRUST"
        else:
            return "UNTRUSTED"
    
    def make_decision(self, trust_result: Dict, resource_sensitivity: int) -> Decision:
        """Make access decision based on trust score."""
        score = trust_result["score"]
        
        if score < 30:
            return Decision.DENY
        elif score < 50:
            return Decision.QUARANTINE
        elif score < 70:
            return Decision.STEP_UP
        else:
            if resource_sensitivity >= 4 and score < 85:
                return Decision.STEP_UP
            return Decision.ALLOW
    
    def evaluate(self, identity: Identity, device: Device, 
                env: Environment, resource: str, resource_sensitivity: int) -> Dict:
        """Full evaluation pipeline."""
        trust = self.calculate_trust_score(identity, device, env, resource_sensitivity)
        decision = self.make_decision(trust, resource_sensitivity)
        
        return {
            "resource": resource,
            "trust_score": trust["score"],
            "trust_level": trust["level"],
            "decision": decision.value,
            "factors": trust["factors"]
        }


def main():
    print("=" * 60)
    print("🛡️  ZERO TRUST POLICY ENGINE")
    print("=" * 60)
    
    engine = ZeroTrustEngine()
    
    scenarios = [
        {
            "name": "Employee in office with managed laptop",
            "identity": Identity("alice", "hardware_key", 10, 0),
            "device": Device("laptop_alice", True, True, True, True),
            "env": Environment("office", "corporate", "low", 10),
            "resource": "Financial Database",
            "sensitivity": 5
        },
        {
            "name": "Employee from home with personal device",
            "identity": Identity("bob", "mfa", 30, 0),
            "device": Device("tablet_bob", False, False, True, False),
            "env": Environment("home", "public_wifi", "low", 20),
            "resource": "Email",
            "sensitivity": 2
        },
        {
            "name": "Contractor from coffee shop",
            "identity": Identity("charlie", "password", 60, 2),
            "device": Device("laptop_charlie", False, True, True, False),
            "env": Environment("public", "public_wifi", "medium", 14),
            "resource": "Code Repository",
            "sensitivity": 3
        },
        {
            "name": "Suspicious login with many failures",
            "identity": Identity("diana", "mfa", 80, 5),
            "device": Device("unknown", False, False, False, False),
            "env": Environment("unknown", "public_wifi", "high", 3),
            "resource": "Admin Panel",
            "sensitivity": 5
        },
        {
            "name": "Admin during high threat alert",
            "identity": Identity("eve", "hardware_key", 15, 0),
            "device": Device("laptop_eve", True, True, True, True),
            "env": Environment("office", "corporate", "high", 11),
            "resource": "Production Servers",
            "sensitivity": 5
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        print("-" * 50)
        print(f"   User: {scenario['identity'].username}")
        print(f"   Auth: {scenario['identity'].auth_method}")
        print(f"   Device: managed={scenario['device'].managed}, "
              f"compliant={scenario['device'].compliant}")
        print(f"   Location: {scenario['env'].location}, "
              f"network={scenario['env'].network}")
        print(f"   Resource: {scenario['resource']} (sensitivity: {scenario['sensitivity']})")
        
        result = engine.evaluate(
            scenario['identity'],
            scenario['device'],
            scenario['env'],
            scenario['resource'],
            scenario['sensitivity']
        )
        
        print(f"\n📊 Trust Score: {result['trust_score']}/100 ({result['trust_level']})")
        print("   Factors:")
        for factor in result['factors']:
            print(f"      • {factor}")
        
        decision_icon = "✅" if result['decision'] == "ALLOW" else "❌" if result['decision'] == "DENY" else "⚠️"
        print(f"\n🔒 Decision: {decision_icon} {result['decision']}")
    
    print("\n" + "=" * 60)
    print("💡 ZERO TRUST PRINCIPLES")
    print("=" * 60)
    print("• No implicit trust based on network location")
    print("• Every access request is fully evaluated")
    print("• Device health matters as much as user identity")
    print("• Threat intelligence dynamically affects decisions")
    print("• Sensitive resources require higher trust scores")


if __name__ == "__main__":
    main()
