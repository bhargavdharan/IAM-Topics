#!/usr/bin/env python3
"""
AI Anomaly Detector Simulation
==============================
Demonstrates ML-based login anomaly detection using statistical methods.
Builds behavioral baselines and flags deviations.

Concepts demonstrated:
- Baseline profiling from historical data
- Feature engineering (time, location, device)
- Anomaly scoring using z-scores and thresholds
- False positive vs false negative trade-offs
"""

import random
import math
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum


class AnomalyLevel(Enum):
    NORMAL = "NORMAL"
    SUSPICIOUS = "SUSPICIOUS"
    ANOMALOUS = "ANOMALOUS"
    CRITICAL = "CRITICAL"


@dataclass
class LoginEvent:
    timestamp: datetime
    hour: int
    day_of_week: int
    location: str
    device_type: str
    device_managed: bool
    is_vpn: bool
    data_accessed_mb: float
    actions_count: int
    is_label: bool = False  # True if this is a known attack


class BehavioralBaseline:
    """Learns normal behavior patterns for a user."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.hour_mean = 0
        self.hour_std = 1
        self.typical_locations: set = set()
        self.typical_device_types: set = set()
        self.avg_actions = 0
        self.avg_data_accessed = 0
        self.mgmt_device_ratio = 1.0
        self.vpn_ratio = 0.0

    def train(self, events: List[LoginEvent]):
        """Build baseline from historical events."""
        hours = [e.hour for e in events]
        self.hour_mean = sum(hours) / len(hours)
        self.hour_std = math.sqrt(sum((h - self.hour_mean) ** 2 for h in hours) / len(hours)) or 1

        self.typical_locations = {e.location for e in events}
        self.typical_device_types = {e.device_type for e in events}

        self.avg_actions = sum(e.actions_count for e in events) / len(events)
        self.avg_data_accessed = sum(e.data_accessed_mb for e in events) / len(events)

        managed = sum(1 for e in events if e.device_managed)
        self.mgmt_device_ratio = managed / len(events)

        vpn = sum(1 for e in events if e.is_vpn)
        self.vpn_ratio = vpn / len(events)

        print(f"  Baseline trained on {len(events)} events:")
        print(f"    Typical hours: {self.hour_mean:.1f}h ± {self.hour_std:.1f}h")
        print(f"    Typical locations: {', '.join(self.typical_locations)}")
        print(f"    Typical devices: {', '.join(self.typical_device_types)}")
        print(f"    Avg actions/session: {self.avg_actions:.1f}")
        print(f"    Managed device ratio: {self.mgmt_device_ratio:.1%}")


class AnomalyDetector:
    """Detects anomalies in login events against a behavioral baseline."""

    def __init__(self, baseline: BehavioralBaseline):
        self.baseline = baseline
        self.thresholds = {
            AnomalyLevel.NORMAL: 0,
            AnomalyLevel.SUSPICIOUS: 25,
            AnomalyLevel.ANOMALOUS: 50,
            AnomalyLevel.CRITICAL: 75
        }

    def score_event(self, event: LoginEvent) -> Tuple[float, List[str]]:
        """Calculate anomaly score and reasons."""
        score = 0.0
        reasons = []

        # Feature 1: Time deviation (z-score)
        time_z = abs(event.hour - self.baseline.hour_mean) / self.baseline.hour_std
        if time_z > 2:
            score += min(time_z * 10, 25)
            reasons.append(f"Unusual login time ({event.hour}:00, z={time_z:.1f})")

        # Feature 2: Unknown location
        if event.location not in self.baseline.typical_locations:
            score += 20
            reasons.append(f"Unknown location: {event.location}")

        # Feature 3: Unknown device type
        if event.device_type not in self.baseline.typical_device_types:
            score += 15
            reasons.append(f"Unknown device: {event.device_type}")

        # Feature 4: Unmanaged device (if user normally uses managed)
        if self.baseline.mgmt_device_ratio > 0.8 and not event.device_managed:
            score += 20
            reasons.append("Unmanaged device (user typically uses managed)")

        # Feature 5: VPN usage (if user doesn't normally use VPN)
        if self.baseline.vpn_ratio < 0.2 and event.is_vpn:
            score += 10
            reasons.append("Unusual VPN usage")

        # Feature 6: High action count
        if event.actions_count > self.baseline.avg_actions * 3:
            score += 15
            reasons.append(f"High activity: {event.actions_count} actions (avg: {self.baseline.avg_actions:.0f})")

        # Feature 7: High data access
        if event.data_accessed_mb > self.baseline.avg_data_accessed * 5:
            score += 15
            reasons.append(f"Large data access: {event.data_accessed_mb:.0f}MB (avg: {self.baseline.avg_data_accessed:.0f}MB)")

        # Feature 8: Weekend login (simple heuristic)
        if event.day_of_week >= 5:
            score += 5
            reasons.append("Weekend login")

        return min(score, 100), reasons

    def classify(self, score: float) -> AnomalyLevel:
        """Classify anomaly level based on score."""
        if score >= self.thresholds[AnomalyLevel.CRITICAL]:
            return AnomalyLevel.CRITICAL
        elif score >= self.thresholds[AnomalyLevel.ANOMALOUS]:
            return AnomalyLevel.ANOMALOUS
        elif score >= self.thresholds[AnomalyLevel.SUSPICIOUS]:
            return AnomalyLevel.SUSPICIOUS
        return AnomalyLevel.NORMAL

    def evaluate(self, event: LoginEvent) -> Dict:
        """Full evaluation of a login event."""
        score, reasons = self.score_event(event)
        level = self.classify(score)

        return {
            "event": event,
            "score": score,
            "level": level,
            "reasons": reasons,
            "action": self._recommend_action(level)
        }

    def _recommend_action(self, level: AnomalyLevel) -> str:
        actions = {
            AnomalyLevel.NORMAL: "Allow access",
            AnomalyLevel.SUSPICIOUS: "Allow with step-up MFA",
            AnomalyLevel.ANOMALOUS: "Block and alert SOC",
            AnomalyLevel.CRITICAL: "Block immediately; disable account; initiate investigation"
        }
        return actions[level]


def generate_normal_events(user_id: str, count: int = 50) -> List[LoginEvent]:
    """Generate synthetic normal login events."""
    random.seed(hash(user_id) % 10000)
    events = []
    base_time = datetime(2024, 1, 1, 9, 0)

    for i in range(count):
        # Normal: 9 AM - 6 PM, weekday, office or home, managed laptop
        hour = random.randint(9, 17)
        day = random.randint(0, 4)
        location = random.choice(["office_nyc", "home"])
        device = random.choice(["managed_laptop", "managed_desktop"])

        events.append(LoginEvent(
            timestamp=base_time + timedelta(days=i % 30, hours=hour),
            hour=hour,
            day_of_week=day,
            location=location,
            device_type=device,
            device_managed=True,
            is_vpn=False,
            data_accessed_mb=random.uniform(10, 100),
            actions_count=random.randint(5, 20)
        ))
    return events


def generate_test_events() -> List[Tuple[LoginEvent, str]]:
    """Generate test events with known labels for evaluation."""
    tests = []

    # Normal event
    tests.append((LoginEvent(
        timestamp=datetime(2024, 2, 1, 10, 0),
        hour=10, day_of_week=1,
        location="office_nyc", device_type="managed_laptop",
        device_managed=True, is_vpn=False,
        data_accessed_mb=50, actions_count=12
    ), "Normal login from office"))

    # Suspicious: Late night + unknown location
    tests.append((LoginEvent(
        timestamp=datetime(2024, 2, 2, 3, 0),
        hour=3, day_of_week=3,
        location="moscow", device_type="managed_laptop",
        device_managed=True, is_vpn=True,
        data_accessed_mb=30, actions_count=8
    ), "3 AM login from Moscow via VPN"))

    # Anomalous: Unmanaged device + massive data download
    tests.append((LoginEvent(
        timestamp=datetime(2024, 2, 3, 14, 0),
        hour=14, day_of_week=4,
        location="office_nyc", device_type="unknown_android",
        device_managed=False, is_vpn=False,
        data_accessed_mb=2500, actions_count=5
    ), "Unmanaged Android downloading 2.5GB from office"))

    # Critical: Impossible travel + admin elevation
    tests.append((LoginEvent(
        timestamp=datetime(2024, 2, 4, 10, 0),
        hour=10, day_of_week=0,
        location="tokyo", device_type="unknown_browser",
        device_managed=False, is_vpn=False,
        data_accessed_mb=5000, actions_count=150
    ), "Login from Tokyo 1 hour after NYC login with massive activity"))

    return tests


def main():
    print("🔍 AI ANOMALY DETECTOR SIMULATION")
    print("=" * 60)
    print("This simulation trains a behavioral baseline from historical")
    print("login data, then evaluates new login events for anomalies.\n")

    user_id = "alice_smith"

    # Step 1: Train baseline
    print(f"📊 STEP 1: Training baseline for {user_id}")
    print("-" * 40)
    historical = generate_normal_events(user_id, 60)
    baseline = BehavioralBaseline(user_id)
    baseline.train(historical)

    # Step 2: Evaluate test events
    print(f"\n🔎 STEP 2: Evaluating login events")
    print("=" * 60)

    detector = AnomalyDetector(baseline)
    test_events = generate_test_events()

    correct = 0
    for event, description in test_events:
        result = detector.evaluate(event)

        icons = {
            AnomalyLevel.NORMAL: "✅",
            AnomalyLevel.SUSPICIOUS: "⚠️",
            AnomalyLevel.ANOMALOUS: "🚨",
            AnomalyLevel.CRITICAL: "🔴"
        }

        print(f"\n{icons[result['level']]} {description}")
        print(f"   Anomaly Score: {result['score']:.1f}/100 ({result['level'].value})")
        print(f"   Action: {result['action']}")
        if result['reasons']:
            print(f"   Reasons:")
            for reason in result['reasons']:
                print(f"      • {reason}")

        # Expected classification heuristic
        expected = AnomalyLevel.NORMAL if "Normal" in description else AnomalyLevel.SUSPICIOUS
        if "Anomalous" in description or "massive" in description.lower():
            expected = AnomalyLevel.ANOMALOUS
        if "Critical" in description or "impossible" in description.lower():
            expected = AnomalyLevel.CRITICAL

        if result['level'] == expected or (expected == AnomalyLevel.ANOMALOUS and result['level'] in [AnomalyLevel.ANOMALOUS, AnomalyLevel.CRITICAL]):
            correct += 1

    # Step 3: Threshold analysis
    print(f"\n{'='*60}")
    print("📈 STEP 3: Threshold Sensitivity Analysis")
    print("=" * 60)

    thresholds = [15, 25, 35, 50, 65, 75]
    print("\nThreshold | Normal | Suspicious | Anomalous | Critical")
    print("-" * 55)
    for t in thresholds:
        detector.thresholds[AnomalyLevel.SUSPICIOUS] = t
        detector.thresholds[AnomalyLevel.ANOMALOUS] = t + 25
        detector.thresholds[AnomalyLevel.CRITICAL] = t + 50

        counts = {level: 0 for level in AnomalyLevel}
        for event, _ in test_events:
            score, _ = detector.score_event(event)
            counts[detector.classify(score)] += 1

        print(f"   {t:3d}     |   {counts[AnomalyLevel.NORMAL]}    |     {counts[AnomalyLevel.SUSPICIOUS]}      |     {counts[AnomalyLevel.ANOMALOUS]}       |    {counts[AnomalyLevel.CRITICAL]}")

    print("\n" + "=" * 60)
    print("✅ Simulation complete.")
    print("=" * 60)
    print("\nKey takeaways:")
    print("  • Baselines learn 'normal' from historical data")
    print("  • Anomaly scoring combines multiple behavioral signals")
    print("  • Threshold tuning balances false positives vs false negatives")
    print("  • Multiple weak signals together create strong detection")
    print("  • Explainable reasons help SOC analysts investigate alerts")


if __name__ == "__main__":
    main()
