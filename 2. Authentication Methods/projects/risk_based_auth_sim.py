#!/usr/bin/env python3
"""
Risk-Based Authentication Simulator
====================================
Simulates adaptive authentication that evaluates login risk
from multiple signals and dynamically adjusts requirements.

Run: python risk_based_auth_sim.py
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class LoginAttempt:
    username: str
    device_id: str
    location: str
    ip_address: str
    time: datetime
    is_new_device: bool
    is_new_location: bool
    failed_attempts_last_hour: int


class RiskEngine:
    """Evaluates risk score for login attempts."""
    
    # Known good values
    KNOWN_DEVICES = ["device_alice_laptop", "device_alice_phone"]
    KNOWN_LOCATIONS = ["New York, USA", "Home Office"]
    KNOWN_IPS = ["192.168.1.100", "203.0.113.50"]
    
    def __init__(self):
        self.user_history: Dict[str, List[Dict]] = {}
    
    def calculate_risk(self, attempt: LoginAttempt) -> Dict:
        """Calculate risk score from 0 (low) to 100 (critical)."""
        risk_factors = []
        score = 0
        
        # Factor 1: Device trust
        if attempt.is_new_device:
            score += 25
            risk_factors.append("New device detected (+25)")
        else:
            risk_factors.append("Known device (+0)")
        
        # Factor 2: Location anomaly
        if attempt.is_new_location:
            score += 20
            risk_factors.append("New location (+20)")
        else:
            risk_factors.append("Known location (+0)")
        
        # Factor 3: Time anomaly
        hour = attempt.time.hour
        if hour < 6 or hour > 23:
            score += 15
            risk_factors.append("Unusual hours (+15)")
        else:
            risk_factors.append("Normal hours (+0)")
        
        # Factor 4: Failed attempts
        if attempt.failed_attempts_last_hour > 3:
            score += 30
            risk_factors.append(f"Many failed attempts ({attempt.failed_attempts_last_hour}) (+30)")
        elif attempt.failed_attempts_last_hour > 0:
            score += 10
            risk_factors.append(f"Some failed attempts ({attempt.failed_attempts_last_hour}) (+10)")
        else:
            risk_factors.append("No recent failures (+0)")
        
        # Factor 5: IP reputation (simulated)
        if attempt.ip_address.startswith("10.") or attempt.ip_address.startswith("192.168."):
            risk_factors.append("Private IP (+0)")
        else:
            # Simulate some IPs as suspicious
            ip_last_octet = int(attempt.ip_address.split(".")[-1])
            if ip_last_octet > 200:
                score += 10
                risk_factors.append("Suspicious IP range (+10)")
            else:
                risk_factors.append("Public IP (+0)")
        
        score = min(score, 100)
        
        return {
            "score": score,
            "factors": risk_factors,
            "level": self._get_risk_level(score)
        }
    
    def _get_risk_level(self, score: int) -> str:
        if score < 20:
            return "LOW"
        elif score < 50:
            return "MEDIUM"
        elif score < 75:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def determine_action(self, risk: Dict) -> str:
        """Determine authentication action based on risk."""
        score = risk["score"]
        if score < 20:
            return "ALLOW - No additional verification needed"
        elif score < 35:
            return "ALLOW - Send email notification"
        elif score < 50:
            return "STEP_UP - Require SMS/Email OTP"
        elif score < 75:
            return "STEP_UP - Require hardware token + OTP"
        else:
            return "BLOCK - Login denied. Contact security team."


def simulate_scenarios():
    """Run various login scenarios through the risk engine."""
    engine = RiskEngine()
    
    scenarios = [
        LoginAttempt(
            username="alice",
            device_id="device_alice_laptop",
            location="New York, USA",
            ip_address="192.168.1.100",
            time=datetime(2024, 1, 15, 10, 30),
            is_new_device=False,
            is_new_location=False,
            failed_attempts_last_hour=0
        ),
        LoginAttempt(
            username="alice",
            device_id="device_alice_phone",
            location="New York, USA",
            ip_address="203.0.113.50",
            time=datetime(2024, 1, 15, 14, 0),
            is_new_device=False,
            is_new_location=False,
            failed_attempts_last_hour=0
        ),
        LoginAttempt(
            username="alice",
            device_id="device_unknown_tablet",
            location="New York, USA",
            ip_address="192.168.1.105",
            time=datetime(2024, 1, 15, 11, 0),
            is_new_device=True,
            is_new_location=False,
            failed_attempts_last_hour=0
        ),
        LoginAttempt(
            username="alice",
            device_id="device_unknown",
            location="Moscow, Russia",
            ip_address="198.51.100.250",
            time=datetime(2024, 1, 15, 3, 0),
            is_new_device=True,
            is_new_location=True,
            failed_attempts_last_hour=5
        ),
        LoginAttempt(
            username="alice",
            device_id="device_alice_laptop",
            location="Home Office",
            ip_address="192.168.1.100",
            time=datetime(2024, 1, 15, 2, 0),
            is_new_device=False,
            is_new_location=False,
            failed_attempts_last_hour=0
        )
    ]
    
    for i, attempt in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"📝 SCENARIO {i}: {attempt.username} logging in")
        print(f"{'='*60}")
        print(f"   Device:       {attempt.device_id}")
        print(f"   Location:     {attempt.location}")
        print(f"   IP Address:   {attempt.ip_address}")
        print(f"   Time:         {attempt.time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   New Device:   {attempt.is_new_device}")
        print(f"   New Location: {attempt.is_new_location}")
        print(f"   Failed (1h):  {attempt.failed_attempts_last_hour}")
        
        risk = engine.calculate_risk(attempt)
        action = engine.determine_action(risk)
        
        print(f"\n📊 RISK ANALYSIS:")
        for factor in risk["factors"]:
            print(f"   • {factor}")
        
        print(f"\n🎯 TOTAL RISK SCORE: {risk['score']}/100 ({risk['level']})")
        print(f"🔒 ACTION: {action}")


def main():
    print("=" * 60)
    print("🛡️  RISK-BASED AUTHENTICATION SIMULATOR")
    print("=" * 60)
    print("\nThis simulator demonstrates how modern systems evaluate")
    print("login risk from multiple signals and adapt security")
    print("requirements dynamically.\n")
    
    simulate_scenarios()
    
    print("\n" + "=" * 60)
    print("📋 KEY TAKEAWAYS")
    print("=" * 60)
    print("• Low risk (known device, normal time) → Smooth login")
    print("• Medium risk (new device) → Additional notification")
    print("• High risk (new location + device) → Step-up MFA")
    print("• Critical risk (impossible travel + failures) → Block")
    print("• Risk is CONTINUOUSLY evaluated, not just at login")
    print("=" * 60)


if __name__ == "__main__":
    main()
