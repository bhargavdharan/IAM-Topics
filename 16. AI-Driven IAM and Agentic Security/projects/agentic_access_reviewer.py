#!/usr/bin/env python3
"""
Agentic Access Reviewer Simulation
====================================
Demonstrates an autonomous AI agent that reviews user access entitlements,
auto-approves low-risk access, recommends revocations, and escalates
anomalies to human reviewers.

Concepts demonstrated:
- Agentic workflow (perceive → reason → decide → act → learn)
- Risk scoring based on usage, peer groups, and policies
- Human-in-the-loop governance
- Audit trail generation
"""

import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class Decision(Enum):
    AUTO_APPROVE = "AUTO_APPROVE"
    RECOMMEND_REVOKE = "RECOMMEND_REVOKE"
    ESCALATE = "ESCALATE"
    FLAG_SOD = "FLAG_SOD"


@dataclass
class Entitlement:
    name: str
    resource: str
    access_level: str
    last_used_days: int
    usage_count_90d: int
    is_critical: bool = False


@dataclass
class ReviewResult:
    entitlement: str
    decision: Decision
    reason: str
    risk_score: float
    auto_executed: bool = False


class AgenticAccessReviewer:
    """Autonomous AI agent for access reviews."""

    def __init__(self):
        self.decision_log: List[Dict] = []
        self.peer_group_baselines = {
            "Engineering": ["code_repo", "staging_env", "ci_cd", "wiki"],
            "Finance": ["erp", "financial_reports", "payroll_view", "expense_system"],
            "Marketing": ["crm", "social_media", "analytics", "design_tools"],
            "HR": ["hris", "recruiting", "employee_records", "benefits_portal"],
        }

    def calculate_risk_score(self, entitlement: Entitlement, department: str) -> float:
        """Calculate risk score for an entitlement (0-100)."""
        score = 0.0

        # Factor 1: Usage recency (higher = riskier if unused)
        if entitlement.last_used_days > 90:
            score += 30
        elif entitlement.last_used_days > 30:
            score += 15
        else:
            score += 0

        # Factor 2: Usage frequency (lower = riskier)
        if entitlement.usage_count_90d == 0:
            score += 25
        elif entitlement.usage_count_90d < 3:
            score += 10

        # Factor 3: Criticality
        if entitlement.is_critical:
            score += 20

        # Factor 4: Peer group deviation
        peer_resources = self.peer_group_baselines.get(department, [])
        if entitlement.resource not in peer_resources:
            score += 20  # Unusual for role

        # Factor 5: Access level sensitivity
        sensitivity = {"read": 0, "write": 10, "admin": 25, "delete": 30}
        score += sensitivity.get(entitlement.access_level, 10)

        return min(score, 100)

    def decide(self, entitlement: Entitlement, department: str,
               sod_violations: List[str]) -> ReviewResult:
        """Agent makes a decision based on risk analysis."""
        risk = self.calculate_risk_score(entitlement, department)

        # Check SoD violations first (highest priority)
        if entitlement.name in sod_violations:
            return ReviewResult(
                entitlement=entitlement.name,
                decision=Decision.FLAG_SOD,
                reason=f"SoD violation detected: {entitlement.name} conflicts with another entitlement",
                risk_score=risk
            )

        # Low risk + used recently → Auto-approve
        if risk < 30 and entitlement.last_used_days <= 30:
            return ReviewResult(
                entitlement=entitlement.name,
                decision=Decision.AUTO_APPROVE,
                reason=f"Low risk ({risk:.1f}); actively used {entitlement.last_used_days} days ago",
                risk_score=risk,
                auto_executed=True
            )

        # Medium risk + unused → Recommend revoke
        if risk >= 40 and entitlement.usage_count_90d == 0:
            return ReviewResult(
                entitlement=entitlement.name,
                decision=Decision.RECOMMEND_REVOKE,
                reason=f"Unused for 90+ days with risk score {risk:.1f}; recommend revocation",
                risk_score=risk
            )

        # High risk or unusual → Escalate to human
        return ReviewResult(
            entitlement=entitlement.name,
            decision=Decision.ESCALATE,
            reason=f"Risk score {risk:.1f}; unusual for {department} role; requires human review",
            risk_score=risk
        )

    def review_user(self, username: str, department: str,
                    entitlements: List[Entitlement]) -> List[ReviewResult]:
        """Run agentic review for a single user."""
        print(f"\n{'='*60}")
        print(f"AGENTIC REVIEW: {username} ({department})")
        print(f"{'='*60}")
        print(f"Total entitlements to review: {len(entitlements)}")
        print("-" * 60)

        # Simulate SoD policy check
        sod_violations = self._check_sod(entitlements)

        results = []
        for ent in entitlements:
            result = self.decide(ent, department, sod_violations)
            results.append(result)
            self._log_decision(username, result)

        # Summary
        self._print_summary(results)
        return results

    def _check_sod(self, entitlements: List[Entitlement]) -> List[str]:
        """Check for separation of duties violations."""
        names = {e.name for e in entitlements}
        violations = []
        # Rule: Cannot have both payment_request and payment_approve
        if "payment_request" in names and "payment_approve" in names:
            violations.extend(["payment_request", "payment_approve"])
        # Rule: Cannot have both code_deploy and code_review_approve
        if "code_deploy" in names and "code_review_approve" in names:
            violations.extend(["code_deploy", "code_review_approve"])
        return violations

    def _log_decision(self, username: str, result: ReviewResult):
        """Log decision for audit trail."""
        self.decision_log.append({
            "timestamp": datetime.now().isoformat(),
            "user": username,
            "entitlement": result.entitlement,
            "decision": result.decision.value,
            "risk_score": round(result.risk_score, 1),
            "reason": result.reason,
            "auto_executed": result.auto_executed
        })

    def _print_summary(self, results: List[ReviewResult]):
        """Print review summary statistics."""
        counts = {d: 0 for d in Decision}
        for r in results:
            counts[r.decision] += 1

        auto_count = sum(1 for r in results if r.auto_executed)
        human_review_count = len(results) - auto_count

        print("\n📊 REVIEW SUMMARY")
        print("-" * 40)
        for decision, count in counts.items():
            icon = {"AUTO_APPROVE": "✅", "RECOMMEND_REVOKE": "🗑️",
                    "ESCALATE": "⚠️", "FLAG_SOD": "🚫"}
            print(f"  {icon.get(decision.value, '•')} {decision.value}: {count}")
        print("-" * 40)
        print(f"  Auto-processed: {auto_count}/{len(results)} ({auto_count*100//len(results)}%)")
        print(f"  Requiring human review: {human_review_count}")
        print(f"  Manager time saved: ~{(len(results)-human_review_count)*2} minutes")

    def generate_audit_report(self) -> str:
        """Generate compliance audit report."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_decisions": len(self.decision_log),
            "auto_decisions": sum(1 for d in self.decision_log if d["auto_executed"]),
            "human_reviewed": sum(1 for d in self.decision_log if not d["auto_executed"]),
            "decisions": self.decision_log
        }
        return json.dumps(report, indent=2)


def create_sample_user(username: str, department: str) -> List[Entitlement]:
    """Create sample entitlements for demo."""
    if department == "Finance":
        return [
            Entitlement("erp_access", "erp", "write", 5, 45),
            Entitlement("financial_reports", "financial_reports", "read", 2, 60),
            Entitlement("payroll_view", "payroll", "read", 120, 0),  # Unused
            Entitlement("payment_request", "payment_system", "write", 10, 20),
            Entitlement("payment_approve", "payment_system", "admin", 8, 15),  # SoD violation
            Entitlement("expense_system", "expenses", "write", 3, 30),
            Entitlement("code_repo", "code_repo", "read", 0, 0),  # Unusual for Finance
        ]
    elif department == "Engineering":
        return [
            Entitlement("code_repo", "code_repo", "write", 1, 80),
            Entitlement("staging_env", "staging", "admin", 2, 50),
            Entitlement("production_deploy", "production", "admin", 60, 2),
            Entitlement("ci_cd", "cicd", "write", 1, 70),
            Entitlement("code_review_approve", "code_review", "admin", 1, 40),
            Entitlement("code_deploy", "deploy", "admin", 3, 25),  # SoD violation
            Entitlement("financial_reports", "financial_reports", "read", 0, 0),  # Unusual
        ]
    else:
        return []


def main():
    print("🤖 AGENTIC ACCESS REVIEWER SIMULATION")
    print("=" * 60)
    print("This simulation demonstrates how an AI agent autonomously")
    print("reviews user access entitlements with human-in-the-loop")
    print("governance for high-risk decisions.\n")

    agent = AgenticAccessReviewer()

    # Review Finance user
    finance_entitlements = create_sample_user("alice_smith", "Finance")
    agent.review_user("alice_smith", "Finance", finance_entitlements)

    # Review Engineering user
    eng_entitlements = create_sample_user("bob_jones", "Engineering")
    agent.review_user("bob_jones", "Engineering", eng_entitlements)

    # Generate audit report
    print("\n" + "=" * 60)
    print("📋 AUDIT TRAIL SAMPLE (last 3 decisions)")
    print("=" * 60)
    for decision in agent.decision_log[-3:]:
        print(f"\nUser: {decision['user']}")
        print(f"  Entitlement: {decision['entitlement']}")
        print(f"  Decision: {decision['decision']}")
        print(f"  Risk Score: {decision['risk_score']}")
        print(f"  Auto-executed: {decision['auto_executed']}")
        print(f"  Reason: {decision['reason']}")

    print("\n" + "=" * 60)
    print("✅ Simulation complete.")
    print("=" * 60)
    print("\nKey takeaways:")
    print("  • Low-risk, active access is auto-approved without human burden")
    print("  • Unused or high-risk access is flagged for review")
    print("  • SoD violations are automatically detected and escalated")
    print("  • Every decision is logged with reasoning for audit")
    print("  • Managers only review exceptions, not every entitlement")


if __name__ == "__main__":
    main()
