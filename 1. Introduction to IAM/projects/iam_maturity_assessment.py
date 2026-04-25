#!/usr/bin/env python3
"""
IAM Maturity Assessment
=======================
Evaluates an organization's IAM maturity across key dimensions
and provides actionable recommendations.

Run: python iam_maturity_assessment.py
"""

from typing import Dict, List


class MaturityDimension:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.level = 0
        self.questions = []
    
    def add_question(self, question: str, levels: Dict[int, str]):
        self.questions.append({"question": question, "levels": levels})
    
    def assess(self):
        print(f"\n📊 {self.name}")
        print(f"   {self.description}")
        print("-" * 50)
        
        for i, q in enumerate(self.questions, 1):
            print(f"\n   Q{i}: {q['question']}")
            for level, desc in sorted(q['levels'].items()):
                print(f"      [{level}] {desc}")
            
            while True:
                try:
                    answer = int(input(f"   Your maturity level (0-3): ").strip())
                    if 0 <= answer <= 3:
                        break
                    print("   Please enter 0, 1, 2, or 3.")
                except ValueError:
                    print("   Please enter a number.")
            
            self.level += answer
        
        self.level = self.level / (len(self.questions) * 3) * 100
        return self.level


def create_assessment() -> List[MaturityDimension]:
    dimensions = []
    
    # Dimension 1: Identity Governance
    d = MaturityDimension(
        "Identity Governance",
        "How well does your organization manage the identity lifecycle?"
    )
    d.add_question(
        "How are new user accounts created?",
        {
            0: "Manual process, no standardization",
            1: "Semi-automated with email requests",
            2: "Automated provisioning from HR system",
            3: "Fully automated with role-based templates and self-service"
        }
    )
    d.add_question(
        "How often are access reviews conducted?",
        {
            0: "Never or only during audits",
            1: "Annually",
            2: "Quarterly",
            3: "Continuous with real-time analytics and automated recertification"
        }
    )
    d.add_question(
        "How are terminated employee accounts handled?",
        {
            0: "Accounts disabled manually, often delayed",
            1: "IT is notified but process takes days",
            2: "Automated deprovisioning within 24 hours",
            3: "Real-time deprovisioning integrated with HR systems"
        }
    )
    dimensions.append(d)
    
    # Dimension 2: Access Management
    d = MaturityDimension(
        "Access Management",
        "How effectively is access controlled and monitored?"
    )
    d.add_question(
        "What access control model is primarily used?",
        {
            0: "Ad-hoc, no formal model",
            1: "Discretionary access control (owner decides)",
            2: "Role-based access control (RBAC)",
            3: "Attribute-based access control (ABAC) with dynamic policies"
        }
    )
    d.add_question(
        "How is least privilege enforced?",
        {
            0: "Not enforced",
            1: "Reviewed during onboarding only",
            2: "Regular reviews with some automation",
            3: "Continuous monitoring with automated remediation"
        }
    )
    d.add_question(
        "Is there separation of duties for sensitive operations?",
        {
            0: "No separation of duties",
            1: "Informal separation in some areas",
            2: "Formal SoD policies, manually enforced",
            3: "Automated SoD enforcement with preventive and detective controls"
        }
    )
    dimensions.append(d)
    
    # Dimension 3: Authentication
    d = MaturityDimension(
        "Authentication Strength",
        "How robust are your authentication mechanisms?"
    )
    d.add_question(
        "What authentication factors are required?",
        {
            0: "Password only",
            1: "Strong password policy",
            2: "Multi-factor authentication for some users",
            3: "Phishing-resistant MFA (FIDO2/WebAuthn) for all users"
        }
    )
    d.add_question(
        "How are privileged accounts protected?",
        {
            0: "No special protection",
            1: "Stronger passwords for admins",
            2: "Privileged Access Management (PAM) for some accounts",
            3: "Comprehensive PAM with vaulting, JIT access, and session recording"
        }
    )
    d.add_question(
        "Is risk-based or adaptive authentication used?",
        {
            0: "No adaptive authentication",
            1: "Basic IP-based restrictions",
            2: "Risk scoring with step-up MFA",
            3: "AI-driven continuous risk assessment with behavioral biometrics"
        }
    )
    dimensions.append(d)
    
    # Dimension 4: Monitoring & Analytics
    d = MaturityDimension(
        "Monitoring and Analytics",
        "How well are identity events monitored and analyzed?"
    )
    d.add_question(
        "Are authentication and authorization events logged?",
        {
            0: "Minimal or no logging",
            1: "Basic logs without centralized collection",
            2: "Centralized logging with manual review",
            3: "SIEM integration with real-time alerting and automated response"
        }
    )
    d.add_question(
        "How are anomalies and threats detected?",
        {
            0: "Reactive, after incidents occur",
            1: "Basic rule-based alerting",
            2: "Behavioral analytics with some automation",
            3: "AI/ML-driven UEBA with predictive threat detection"
        }
    )
    d.add_question(
        "How are audit reports generated?",
        {
            0: "Manual, ad-hoc reports",
            1: "Scheduled basic reports",
            2: "Automated compliance reports",
            3: "Real-time dashboards with drill-down analytics"
        }
    )
    dimensions.append(d)
    
    return dimensions


def get_recommendations(score: float, dimension: str) -> List[str]:
    if score < 25:
        return [
            f"🔴 CRITICAL: {dimension} is at an ad-hoc level.",
            "   → Establish formal policies immediately.",
            "   → Assign ownership and budget for IAM improvements.",
            "   → Conduct a risk assessment to prioritize gaps."
        ]
    elif score < 50:
        return [
            f"🟡 DEVELOPING: {dimension} has basic processes.",
            "   → Document and standardize existing practices.",
            "   → Introduce automation for repetitive tasks.",
            "   → Define KPIs and begin measuring effectiveness."
        ]
    elif score < 75:
        return [
            f"🟢 DEFINED: {dimension} is well-managed.",
            "   → Optimize processes with advanced automation.",
            "   → Integrate with other security systems.",
            "   → Consider predictive analytics and AI enhancements."
        ]
    else:
        return [
            f"🔵 OPTIMIZED: {dimension} is world-class.",
            "   → Focus on continuous improvement.",
            "   → Share best practices with industry peers.",
            "   → Explore emerging technologies to maintain leadership."
        ]


def main():
    print("=" * 60)
    print("🏢 IAM MATURITY ASSESSMENT")
    print("=" * 60)
    print("\nThis assessment evaluates your organization's IAM capabilities")
    print("across four critical dimensions. For each question, select the")
    print("maturity level (0-3) that best describes your current state.\n")
    
    dimensions = create_assessment()
    scores = {}
    
    for dim in dimensions:
        scores[dim.name] = dim.assess()
    
    # Results
    print("\n" + "=" * 60)
    print("📈 ASSESSMENT RESULTS")
    print("=" * 60)
    
    total_score = 0
    for name, score in scores.items():
        total_score += score
        bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        print(f"\n{name:25s} [{bar}] {score:.1f}%")
        for rec in get_recommendations(score, name):
            print(rec)
    
    overall = total_score / len(scores)
    print("\n" + "=" * 60)
    print(f"🎯 OVERALL IAM MATURITY: {overall:.1f}%")
    
    if overall < 25:
        print("   Level 1: INITIAL - Ad-hoc, reactive processes")
    elif overall < 50:
        print("   Level 2: DEVELOPING - Basic, repeatable processes")
    elif overall < 75:
        print("   Level 3: DEFINED - Standardized, measured processes")
    else:
        print("   Level 4: OPTIMIZED - Automated, continuously improving")
    
    print("=" * 60)
    
    # Save results
    import json
    with open("iam_maturity_report.json", "w") as f:
        json.dump({
            "overall_score": overall,
            "dimension_scores": scores,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }, f, indent=2)
    print("\n💾 Report saved to iam_maturity_report.json")


if __name__ == "__main__":
    # For demo purposes, run with sample data if no input
    import sys
    if not sys.stdin.isatty():
        print("Running in non-interactive mode. Sample assessment:")
        print("(In interactive mode, you'll answer questions)\n")
    main()
