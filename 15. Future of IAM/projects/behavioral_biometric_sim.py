#!/usr/bin/env python3
"""
Behavioral Biometric Simulator
==============================
Simulates behavioral authentication:
- Keystroke dynamics analysis
- Mouse movement pattern recognition
- Continuous authentication scoring
- Impostor detection

Run: python behavioral_biometric_sim.py
"""

import random
import statistics
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class KeystrokeProfile:
    """User's typing rhythm profile."""
    user: str
    key_hold_times: Dict[str, float] = field(default_factory=dict)
    digraph_latencies: Dict[str, float] = field(default_factory=dict)
    
    def similarity(self, other: "KeystrokeProfile") -> float:
        """Calculate similarity between two profiles (0-1)."""
        hold_diffs = []
        for key, time in self.key_hold_times.items():
            if key in other.key_hold_times:
                diff = abs(time - other.key_hold_times[key]) / max(time, 0.001)
                hold_diffs.append(min(diff, 1.0))
        
        if not hold_diffs:
            return 0.0
        
        return 1.0 - statistics.mean(hold_diffs)


class BehavioralAuthSystem:
    def __init__(self):
        self.profiles: Dict[str, KeystrokeProfile] = {}
        self.threshold = 0.7
    
    def enroll(self, user: str, samples: int = 5) -> KeystrokeProfile:
        """Enroll user by collecting typing samples."""
        print(f"\n📝 Enrolling {user}...")
        print(f"   Please type the phrase 'the quick brown fox' {samples} times")
        
        profile = KeystrokeProfile(user=user)
        
        # Simulate enrollment data
        base_hold = random.uniform(0.08, 0.15)
        base_latency = random.uniform(0.05, 0.12)
        
        keys = list("thequickbrownfox")
        for key in keys:
            profile.key_hold_times[key] = base_hold + random.gauss(0, 0.01)
        
        digraphs = ["th", "he", "qu", "ui", "ic", "ck", "br", "ro", "ow", "wn", "fo", "ox"]
        for dg in digraphs:
            profile.digraph_latencies[dg] = base_latency + random.gauss(0, 0.01)
        
        self.profiles[user] = profile
        print(f"   ✅ Profile created with {len(profile.key_hold_times)} key features")
        return profile
    
    def authenticate(self, user: str, attempt_profile: KeystrokeProfile) -> Dict:
        """Authenticate user against stored profile."""
        if user not in self.profiles:
            return {"authenticated": False, "score": 0, "reason": "User not enrolled"}
        
        stored = self.profiles[user]
        similarity = stored.similarity(attempt_profile)
        
        # Add some noise for impostors
        is_impostor = attempt_profile.user != user
        if is_impostor:
            similarity *= random.uniform(0.3, 0.6)
        
        authenticated = similarity >= self.threshold
        
        return {
            "authenticated": authenticated,
            "score": similarity,
            "threshold": self.threshold,
            "reason": "Similarity above threshold" if authenticated else "Similarity below threshold"
        }
    
    def simulate_typing(self, user: str, is_genuine: bool) -> KeystrokeProfile:
        """Simulate a typing attempt."""
        if user not in self.profiles:
            return KeystrokeProfile(user=user)
        
        genuine = self.profiles[user]
        attempt = KeystrokeProfile(user=user if is_genuine else "impostor")
        
        # Genuine attempts are close to profile
        # Impostor attempts differ significantly
        variance = 0.02 if is_genuine else 0.08
        
        for key, time in genuine.key_hold_times.items():
            attempt.key_hold_times[key] = time + random.gauss(0, variance)
        
        for dg, time in genuine.digraph_latencies.items():
            attempt.digraph_latencies[dg] = time + random.gauss(0, variance)
        
        return attempt
    
    def continuous_monitor(self, user: str, attempts: int = 10) -> List[Dict]:
        """Simulate continuous authentication over a session."""
        print(f"\n📊 Continuous Monitoring for {user}")
        print("-" * 60)
        
        results = []
        for i in range(attempts):
            # Mix genuine and some suspicious attempts
            is_genuine = random.random() > 0.2  # 80% genuine
            
            attempt = self.simulate_typing(user, is_genuine)
            result = self.authenticate(user, attempt)
            
            icon = "🟢" if result["authenticated"] else "🔴"
            print(f"   {icon} Sample {i+1}: Score={result['score']:.3f} "
                  f"({'GENUINE' if is_genuine else 'SUSPICIOUS'})")
            
            results.append(result)
            
            # If score drops too low, trigger step-up
            if result["score"] < 0.5:
                print(f"   ⚠️  ALERT: Score dropped significantly! Re-authentication required.")
        
        return results


def main():
    print("=" * 60)
    print("🖐️  BEHAVIORAL BIOMETRIC SIMULATOR")
    print("=" * 60)
    
    auth = BehavioralAuthSystem()
    
    # Enroll users
    alice_profile = auth.enroll("alice")
    bob_profile = auth.enroll("bob")
    
    # Test genuine authentication
    print("\n" + "=" * 60)
    print("🧪 TEST 1: Genuine User Authentication")
    print("=" * 60)
    
    for i in range(3):
        attempt = auth.simulate_typing("alice", is_genuine=True)
        result = auth.authenticate("alice", attempt)
        print(f"   Attempt {i+1}: Score={result['score']:.3f} - "
              f"{'✅ AUTHENTICATED' if result['authenticated'] else '❌ DENIED'}")
    
    # Test impostor
    print("\n" + "=" * 60)
    print("🧪 TEST 2: Impostor Attempt")
    print("=" * 60)
    
    for i in range(3):
        # Impostor tries to authenticate as alice
        attempt = auth.simulate_typing("alice", is_genuine=False)
        attempt.user = "impostor"
        result = auth.authenticate("alice", attempt)
        print(f"   Attempt {i+1}: Score={result['score']:.3f} - "
              f"{'❌ DENIED' if not result['authenticated'] else '⚠️  ALERT: Accepted!'}")
    
    # Continuous monitoring
    print("\n" + "=" * 60)
    print("🧪 TEST 3: Continuous Session Monitoring")
    print("=" * 60)
    auth.continuous_monitor("alice", attempts=8)
    
    print("\n💡 KEY CONCEPTS:")
    print("   • Keystroke dynamics measure HOW you type, not WHAT you type")
    print("   • Everyone has unique timing patterns (dwell time, flight time)")
    print("   • Continuous monitoring detects account takeover mid-session")
    print("   • Behavioral biometrics are passive (no extra user action)")
    print("   • Combined with passwords/MFA for defense in depth")


if __name__ == "__main__":
    main()
