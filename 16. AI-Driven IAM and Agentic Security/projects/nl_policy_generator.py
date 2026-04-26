#!/usr/bin/env python3
"""
Natural Language Policy Generator Simulation
=============================================
Converts English policy descriptions into structured IAM policies.
Demonstrates NLP parsing, template matching, and policy validation.

Concepts demonstrated:
- Natural language understanding for IAM
- Policy template extraction
- Structured policy generation (JSON)
- Ambiguity detection and validation
"""

import json
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum


class PolicyAction(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    SHARE = "share"
    DOWNLOAD = "download"


@dataclass
class ParsedPolicy:
    subjects: List[str]
    resources: List[str]
    actions: List[str]
    conditions: Dict[str, any]
    validity_period: Optional[str] = None
    ambiguous: bool = False
    ambiguities: List[str] = None


class NLPolicyParser:
    """Parses natural language into structured IAM policies."""

    def __init__(self):
        self.department_keywords = {
            "engineering": ["engineer", "developers", "dev team", "engineering"],
            "finance": ["finance", "accounting", "accountants", "financial team"],
            "marketing": ["marketing", "marketers", "marketing team"],
            "hr": ["hr", "human resources", "people team"],
            "sales": ["sales", "sales team", "sales reps"],
        }

        self.resource_keywords = {
            "financial_reports": ["financial report", "revenue data", "budget", "finance doc"],
            "code_repo": ["code repository", "source code", "git repo", "codebase"],
            "customer_database": ["customer data", "customer database", "crm data"],
            "employee_records": ["employee record", "hr data", "personnel file"],
            "production_env": ["production", "prod environment", "live system"],
            "staging_env": ["staging", "test environment", "qa system"],
        }

        self.action_keywords = {
            "read": ["read", "view", "access", "see"],
            "write": ["write", "edit", "modify", "update"],
            "delete": ["delete", "remove", "destroy"],
            "admin": ["admin", "manage", "configure", "full control"],
            "share": ["share", "distribute", "send to"],
            "download": ["download", "export", "copy"],
        }

        self.condition_keywords = {
            "business_hours": ["business hours", "9 to 5", "working hours", "weekdays"],
            "corporate_network": ["corporate network", "office network", "company network"],
            "managed_device": ["managed device", "company device", "corporate laptop"],
            "mfa_required": ["mfa", "multi-factor", "two-factor", "second factor"],
            "contractor_limit": ["contractor", "temporary", "expires", "until"],
        }

    def parse(self, text: str) -> ParsedPolicy:
        """Main entry point: parse natural language to policy."""
        text_lower = text.lower()
        ambiguities = []

        # Extract subjects
        subjects = self._extract_subjects(text_lower)
        if not subjects:
            ambiguities.append("No subject identified (who is this policy for?)")

        # Extract resources
        resources = self._extract_resources(text_lower)
        if not resources:
            ambiguities.append("No resource identified (what does this policy protect?)")

        # Extract actions
        actions = self._extract_actions(text_lower)
        if not actions:
            ambiguities.append("No action identified (what can the subject do?)")

        # Extract conditions
        conditions = self._extract_conditions(text_lower)

        # Check for contradictions
        if "contractor" in text_lower and "full control" in text_lower:
            ambiguities.append("Contradiction: contractors typically should not have 'full control'")

        # Check for missing time restriction on sensitive access
        if any(r in ["financial_reports", "customer_database", "production_env"] for r in resources):
            if "business_hours" not in conditions and "time" not in text_lower:
                ambiguities.append("Sensitive resource access without time restriction may be too permissive")

        return ParsedPolicy(
            subjects=subjects,
            resources=resources,
            actions=actions,
            conditions=conditions,
            ambiguous=len(ambiguities) > 0,
            ambiguities=ambiguities
        )

    def _extract_subjects(self, text: str) -> List[str]:
        subjects = []
        for dept, keywords in self.department_keywords.items():
            for kw in keywords:
                if kw in text:
                    subjects.append(dept)
                    break
        return list(set(subjects))

    def _extract_resources(self, text: str) -> List[str]:
        resources = []
        for resource, keywords in self.resource_keywords.items():
            for kw in keywords:
                if kw in text:
                    resources.append(resource)
                    break
        return list(set(resources))

    def _extract_actions(self, text: str) -> List[str]:
        actions = []
        for action, keywords in self.action_keywords.items():
            for kw in keywords:
                if kw in text:
                    actions.append(action)
                    break
        # Default to read if no action found
        return actions if actions else ["read"]

    def _extract_conditions(self, text: str) -> Dict[str, any]:
        conditions = {}

        for condition, keywords in self.condition_keywords.items():
            for kw in keywords:
                if kw in text:
                    if condition == "business_hours":
                        conditions["time"] = {"start": "09:00", "end": "17:00", "days": "mon-fri"}
                    elif condition == "corporate_network":
                        conditions["network"] = {"type": "corporate"}
                    elif condition == "managed_device":
                        conditions["device"] = {"managed": True}
                    elif condition == "mfa_required":
                        conditions["authentication"] = {"mfa": True}
                    elif condition == "contractor_limit":
                        conditions["employment"] = {"type": "contractor", "access": "read_only"}
                    break

        return conditions

    def generate_json_policy(self, parsed: ParsedPolicy) -> Dict:
        """Convert parsed policy to JSON format."""
        return {
            "version": "2024-01",
            "effect": "allow",
            "subjects": [{"department": s} for s in parsed.subjects],
            "resources": [{"type": r} for r in parsed.resources],
            "actions": parsed.actions,
            "conditions": parsed.conditions,
            "metadata": {
                "generated_from_nl": True,
                "has_ambiguities": parsed.ambiguous,
                "ambiguity_warnings": parsed.ambiguities or []
            }
        }

    def validate_policy(self, parsed: ParsedPolicy) -> Tuple[bool, List[str]]:
        """Validate generated policy for completeness and safety."""
        errors = []

        if not parsed.subjects:
            errors.append("Missing subject: Policy must specify who it applies to")
        if not parsed.resources:
            errors.append("Missing resource: Policy must specify what is being protected")
        if not parsed.actions:
            errors.append("Missing action: Policy must specify what is allowed")

        # Safety check: admin on sensitive resources without conditions
        if "admin" in parsed.actions:
            sensitive = {"financial_reports", "customer_database", "production_env", "employee_records"}
            if any(r in sensitive for r in parsed.resources):
                if not parsed.conditions:
                    errors.append("SAFETY: Admin access on sensitive resource without conditions is dangerous")

        # Check for overly broad access
        if "delete" in parsed.actions and len(parsed.resources) > 3:
            errors.append("WARNING: Delete permission on many resources may violate least privilege")

        return len(errors) == 0, errors


def print_policy_comparison(nl_text: str, parser: NLPolicyParser):
    """Display the full pipeline from NL to structured policy."""
    print(f"\n{'='*60}")
    print(f"📝 INPUT (Natural Language)")
    print(f"{'='*60}")
    print(f'"{nl_text}"')

    parsed = parser.parse(nl_text)
    valid, errors = parser.validate_policy(parsed)
    json_policy = parser.generate_json_policy(parsed)

    print(f"\n🔍 PARSED ELEMENTS")
    print("-" * 40)
    print(f"  Subjects: {parsed.subjects if parsed.subjects else '⚠️ NOT DETECTED'}")
    print(f"  Resources: {parsed.resources if parsed.resources else '⚠️ NOT DETECTED'}")
    print(f"  Actions: {parsed.actions}")
    print(f"  Conditions: {json.dumps(parsed.conditions, indent=4) if parsed.conditions else 'None'}")

    if parsed.ambiguous:
        print(f"\n⚠️ AMBIGUITIES DETECTED")
        print("-" * 40)
        for amb in parsed.ambiguities:
            print(f"  • {amb}")

    if not valid:
        print(f"\n🚫 VALIDATION ERRORS")
        print("-" * 40)
        for err in errors:
            print(f"  • {err}")

    print(f"\n📋 GENERATED POLICY (JSON)")
    print("-" * 40)
    print(json.dumps(json_policy, indent=2))

    status = "✅ VALID" if valid and not parsed.ambiguous else "⚠️ NEEDS REVIEW"
    print(f"\n{status}")


def main():
    print("🧠 NATURAL LANGUAGE POLICY GENERATOR SIMULATION")
    print("=" * 60)
    print("This simulation converts English policy descriptions into")
    print("structured IAM policies, detecting ambiguities and validating")
    print("safety before deployment.\n")

    parser = NLPolicyParser()

    # Example 1: Clear policy
    print_policy_comparison(
        "Engineering team can read and write to the code repository during business hours from managed devices.",
        parser
    )

    # Example 2: Ambiguous policy
    print_policy_comparison(
        "People can access financial stuff when they need to.",
        parser
    )

    # Example 3: Contractor policy with time limit
    print_policy_comparison(
        "Contractors can view customer data but cannot download or share it. Access expires when their contract ends.",
        parser
    )

    # Example 4: Potentially dangerous policy
    print_policy_comparison(
        "Everyone has full control over everything all the time.",
        parser
    )

    print(f"\n{'='*60}")
    print("✅ Simulation complete.")
    print("=" * 60)
    print("\nKey takeaways:")
    print("  • NL parsing extracts subjects, resources, actions, conditions")
    print("  • Ambiguity detection flags underspecified policies")
    print("  • Safety validation prevents dangerous auto-generated policies")
    print("  • Human review is mandatory before deploying generated policies")
    print("  • Clear, specific language produces better structured policies")


if __name__ == "__main__":
    main()
