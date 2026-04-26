#!/usr/bin/env python3
"""
AI Security Auditor Simulation
==============================
Audits AI-driven access decisions for bias, hallucinations,
and policy violations. Demonstrates AI oversight of AI.

Concepts demonstrated:
- Decision logging and explainability scoring
- Bias detection in access decisions
- Hallucination detection in policy generation
- Compliance audit report generation
"""

import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class BiasType(Enum):
    NONE = "NONE"
    TEMPORAL = "TEMPORAL"  # Time-based bias (e.g., always deny after hours)
    DEMOGRAPHIC = "DEMOGRAPHIC"  # Department/role-based bias
    GEOGRAPHIC = "GEOGRAPHIC"  # Location-based bias


class IssueSeverity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class AIDecision:
    decision_id: str
    timestamp: datetime
    user_id: str
    department: str
    location: str
    request_type: str
    ai_decision: str  # "approve" or "deny"
    risk_score: float
    reasoning: str
    human_overridden: bool = False
    human_decision: Optional[str] = None


@dataclass
class AuditFinding:
    finding_id: str
    issue_type: str
    severity: IssueSeverity
    description: str
    affected_decisions: List[str]
    recommendation: str


class AISecurityAuditor:
    """Audits AI-driven access decisions for fairness and accuracy."""

    def __init__(self):
        self.decisions: List[AIDecision] = []
        self.findings: List[AuditFinding] = []

    def log_decision(self, decision: AIDecision):
        """Record an AI decision for later audit."""
        self.decisions.append(decision)

    def audit_bias(self) -> List[AuditFinding]:
        """Detect bias in AI decisions across demographic groups."""
        findings = []

        # Check department bias
        dept_stats = {}
        for d in self.decisions:
            if d.department not in dept_stats:
                dept_stats[d.department] = {"total": 0, "denied": 0}
            dept_stats[d.department]["total"] += 1
            if d.ai_decision == "deny":
                dept_stats[d.department]["denied"] += 1

        deny_rates = {dept: stats["denied"] / stats["total"]
                      for dept, stats in dept_stats.items() if stats["total"] > 0}

        if deny_rates:
            avg_deny = sum(deny_rates.values()) / len(deny_rates)
            for dept, rate in deny_rates.items():
                if rate > avg_deny * 1.5 and dept_stats[dept]["total"] >= 5:
                    findings.append(AuditFinding(
                        finding_id=f"BIAS-DEPT-{dept.upper()}",
                        issue_type="Demographic Bias",
                        severity=IssueSeverity.HIGH,
                        description=f"{dept} has {rate:.1%} denial rate vs {avg_deny:.1%} average",
                        affected_decisions=[d.decision_id for d in self.decisions
                                           if d.department == dept and d.ai_decision == "deny"],
                        recommendation=f"Review training data for {dept} representation; verify policy does not unfairly target this department"
                    ))

        # Check temporal bias (after-hours denials)
        hour_stats = {"business": {"total": 0, "denied": 0},
                      "after_hours": {"total": 0, "denied": 0}}
        for d in self.decisions:
            hour = d.timestamp.hour
            period = "business" if 9 <= hour <= 17 else "after_hours"
            hour_stats[period]["total"] += 1
            if d.ai_decision == "deny":
                hour_stats[period]["denied"] += 1

        for period, stats in hour_stats.items():
            if stats["total"] > 0:
                rate = stats["denied"] / stats["total"]
                if period == "after_hours" and rate > 0.7:
                    findings.append(AuditFinding(
                        finding_id=f"BIAS-TIME-{period.upper()}",
                        issue_type="Temporal Bias",
                        severity=IssueSeverity.MEDIUM,
                        description=f"After-hours requests have {rate:.1%} denial rate — may indicate time-based bias",
                        affected_decisions=[d.decision_id for d in self.decisions
                                           if d.timestamp.hour not in range(9, 18) and d.ai_decision == "deny"],
                        recommendation="Verify after-hours access is legitimately restricted by policy, not model bias"
                    ))

        return findings

    def audit_hallucinations(self) -> List[AuditFinding]:
        """Detect AI decisions with unsupported or fabricated reasoning."""
        findings = []

        hallucination_patterns = [
            "based on regulation",
            "company policy states",
            "according to",
            "as per",
        ]

        for d in self.decisions:
            # Check for claims of policy/regulation without specificity
            reasoning_lower = d.reasoning.lower()
            if any(pattern in reasoning_lower for pattern in hallucination_patterns):
                if "section" not in reasoning_lower and "article" not in reasoning_lower:
                    findings.append(AuditFinding(
                        finding_id=f"HALLUCINATE-{d.decision_id}",
                        issue_type="Potential Hallucination",
                        severity=IssueSeverity.MEDIUM,
                        description=f"Decision {d.decision_id} references policy/regulation without specific citation",
                        affected_decisions=[d.decision_id],
                        recommendation="Require AI to cite specific policy sections; validate claims against actual policy documents"
                    ))

            # Check for impossible reasoning (risk score mismatch)
            if d.risk_score < 20 and d.ai_decision == "deny":
                findings.append(AuditFinding(
                    finding_id=f"HALLUCINATE-RISK-{d.decision_id}",
                    issue_type="Reasoning Inconsistency",
                    severity=IssueSeverity.HIGH,
                    description=f"Decision denied with low risk score ({d.risk_score:.1f}) — reasoning may be fabricated",
                    affected_decisions=[d.decision_id],
                    recommendation="Flag decisions where risk score and decision outcome are inconsistent"
                ))

        return findings

    def audit_human_override_rate(self) -> List[AuditFinding]:
        """Check if humans frequently override AI decisions."""
        findings = []

        overridden = [d for d in self.decisions if d.human_overridden]
        if len(overridden) > len(self.decisions) * 0.3:
            # High override rate indicates AI is not trustworthy
            override_rate = len(overridden) / len(self.decisions)

            # Analyze override patterns
            ai_approved_overridden = sum(1 for d in overridden
                                         if d.ai_decision == "approve" and d.human_decision == "deny")
            ai_denied_overridden = sum(1 for d in overridden
                                       if d.ai_decision == "deny" and d.human_decision == "approve")

            findings.append(AuditFinding(
                finding_id="OVERRIDE-HIGH",
                issue_type="High Override Rate",
                severity=IssueSeverity.HIGH,
                description=f"Humans override {override_rate:.1%} of AI decisions — model accuracy is insufficient",
                affected_decisions=[d.decision_id for d in overridden],
                recommendation=f"Retrain model; {ai_approved_overridden} false approvals and {ai_denied_overridden} false denials detected"
            ))

        return findings

    def audit_completeness(self) -> List[AuditFinding]:
        """Check that all decisions have required explainability."""
        findings = []

        unexplained = [d for d in self.decisions
                       if len(d.reasoning) < 20 or "because" not in d.reasoning.lower()]

        if unexplained:
            findings.append(AuditFinding(
                finding_id="EXPLAINABILITY-LOW",
                issue_type="Poor Explainability",
                severity=IssueSeverity.MEDIUM,
                description=f"{len(unexplained)} decisions lack meaningful reasoning",
                affected_decisions=[d.decision_id for d in unexplained],
                recommendation="Require AI to provide structured reasoning with specific factors for every decision"
            ))

        return findings

    def run_full_audit(self) -> Dict:
        """Execute complete audit and return report."""
        self.findings = []
        self.findings.extend(self.audit_bias())
        self.findings.extend(self.audit_hallucinations())
        self.findings.extend(self.audit_human_override_rate())
        self.findings.extend(self.audit_completeness())

        severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        for f in self.findings:
            severity_counts[f.severity.value] += 1

        return {
            "audit_timestamp": datetime.now().isoformat(),
            "total_decisions_audited": len(self.decisions),
            "total_findings": len(self.findings),
            "severity_breakdown": severity_counts,
            "findings": [
                {
                    "id": f.finding_id,
                    "type": f.issue_type,
                    "severity": f.severity.value,
                    "description": f.description,
                    "affected_count": len(f.affected_decisions),
                    "recommendation": f.recommendation
                }
                for f in self.findings
            ],
            "recommendations": self._generate_recommendations(severity_counts)
        }

    def _generate_recommendations(self, severity_counts: Dict) -> List[str]:
        recs = []
        if severity_counts["CRITICAL"] > 0 or severity_counts["HIGH"] > 0:
            recs.append("IMMEDIATE: Pause autonomous approvals until high-severity findings are resolved")
        if severity_counts["MEDIUM"] > 0:
            recs.append("SHORT-TERM: Implement explainability requirements and policy citation validation")
        if severity_counts["LOW"] > 0:
            recs.append("ONGOING: Monitor decision quality metrics and retrain models quarterly")
        recs.append("GOVERNANCE: Establish AI decision audit as mandatory monthly process")
        return recs


def generate_sample_decisions(count: int = 30) -> List[AIDecision]:
    """Generate synthetic AI decisions for audit demonstration."""
    random.seed(42)
    decisions = []
    departments = ["Engineering", "Finance", "Marketing", "HR", "Sales"]
    locations = ["office_nyc", "office_london", "home", "remote_unknown"]
    request_types = ["folder_access", "app_access", "privilege_elevation", "data_export"]

    base_time = datetime(2024, 3, 1, 9, 0)

    for i in range(count):
        dept = random.choice(departments)
        # Introduce bias: Finance gets higher denial rate
        if dept == "Finance":
            deny_prob = 0.5
        else:
            deny_prob = 0.2

        # Introduce temporal bias: after-hours more likely denied
        hour = random.choice(list(range(8, 18)) + [22, 23, 1, 2, 3])
        if hour < 9 or hour > 17:
            deny_prob += 0.3

        ai_dec = "deny" if random.random() < deny_prob else "approve"
        risk = random.uniform(10, 90) if ai_dec == "deny" else random.uniform(5, 40)

        # Some decisions have poor reasoning (hallucination simulation)
        if i % 7 == 0:
            reasoning = "Denied based on company policy regulation compliance requirements"
        elif i % 5 == 0:
            reasoning = "Approved"  # Too short
        else:
            reasoning = f"{ai_dec.title()}d due to risk score {risk:.0f} and location analysis"

        # Human overrides
        human_override = random.random() < 0.25
        human_dec = None
        if human_override:
            human_dec = "approve" if ai_dec == "deny" else "deny"

        decisions.append(AIDecision(
            decision_id=f"DEC-{i+1:04d}",
            timestamp=base_time + timedelta(hours=i * 2),
            user_id=f"user_{i+1}",
            department=dept,
            location=random.choice(locations),
            request_type=random.choice(request_types),
            ai_decision=ai_dec,
            risk_score=risk,
            reasoning=reasoning,
            human_overridden=human_override,
            human_decision=human_dec
        ))

    return decisions


def main():
    print("🔍 AI SECURITY AUDITOR SIMULATION")
    print("=" * 60)
    print("This simulation audits AI-driven access decisions for:")
    print("  • Bias across departments, time, and location")
    print("  • Hallucinations in reasoning")
    print("  • High human override rates (indicates untrustworthy AI)")
    print("  • Explainability gaps\n")

    # Generate sample decisions with injected issues
    print("📊 Generating 30 synthetic AI decisions...")
    decisions = generate_sample_decisions(30)

    # Log them
    auditor = AISecurityAuditor()
    for d in decisions:
        auditor.log_decision(d)

    # Show sample decisions
    print(f"\n{'='*60}")
    print("📋 SAMPLE DECISIONS (showing 3)")
    print("=" * 60)
    for d in decisions[:3]:
        override = f" [HUMAN OVERRIDES: AI={d.ai_decision}→Human={d.human_decision}]" if d.human_overridden else ""
        print(f"\n{d.decision_id} | {d.user_id} ({d.department})")
        print(f"  Time: {d.timestamp.strftime('%Y-%m-%d %H:%M')} | Location: {d.location}")
        print(f"  AI Decision: {d.ai_decision.upper()} | Risk: {d.risk_score:.1f}{override}")
        print(f"  Reasoning: {d.reasoning}")

    # Run audit
    print(f"\n{'='*60}")
    print("🔎 RUNNING FULL AUDIT")
    print("=" * 60)

    report = auditor.run_full_audit()

    print(f"\n📈 AUDIT SUMMARY")
    print("-" * 40)
    print(f"  Total decisions audited: {report['total_decisions_audited']}")
    print(f"  Total findings: {report['total_findings']}")
    print(f"\n  Severity Breakdown:")
    for sev, count in report['severity_breakdown'].items():
        icon = {"CRITICAL": "🔴", "HIGH": "🚨", "MEDIUM": "⚠️", "LOW": "ℹ️"}
        print(f"    {icon.get(sev, '•')} {sev}: {count}")

    print(f"\n📋 DETAILED FINDINGS")
    print("-" * 40)
    for finding in report['findings']:
        icon = {"CRITICAL": "🔴", "HIGH": "🚨", "MEDIUM": "⚠️", "LOW": "ℹ️"}
        print(f"\n  {icon.get(finding['severity'], '•')} [{finding['severity']}] {finding['type']}")
        print(f"     ID: {finding['id']}")
        print(f"     Description: {finding['description']}")
        print(f"     Affected decisions: {finding['affected_count']}")
        print(f"     Recommendation: {finding['recommendation']}")

    print(f"\n📋 TOP-LEVEL RECOMMENDATIONS")
    print("-" * 40)
    for rec in report['recommendations']:
        print(f"  • {rec}")

    print(f"\n{'='*60}")
    print("✅ Simulation complete.")
    print("=" * 60)
    print("\nKey takeaways:")
    print("  • AI decisions must be auditable, not just automated")
    print("  • Bias detection prevents discriminatory access patterns")
    print("  • Hallucination detection ensures reasoning is grounded")
    print("  • High override rates signal model accuracy problems")
    print("  • AI auditing AI is essential for trustworthy automation")
    print("  • Explainability is not optional — it is required for compliance")


if __name__ == "__main__":
    main()
