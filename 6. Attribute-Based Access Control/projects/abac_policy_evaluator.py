#!/usr/bin/env python3
"""
ABAC Policy Evaluator
=====================
Evaluates Attribute-Based Access Control policies.
Demonstrates how dynamic attributes determine access decisions.

Run: python abac_policy_evaluator.py
"""

from typing import Dict, List, Any, Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Subject:
    """User attributes."""
    name: str
    department: str
    role: str
    clearance: int  # 1-5
    employment_type: str  # employee, contractor, vendor
    

@dataclass
class Resource:
    """Resource attributes."""
    name: str
    owner_department: str
    classification: int  # 1-5
    type: str  # document, database, application
    

@dataclass
class Action:
    """Action attributes."""
    name: str  # read, write, delete, approve
    

@dataclass
class Environment:
    """Environment attributes."""
    time: datetime
    location: str
    device_managed: bool
    network: str  # corporate, vpn, public
    threat_level: str  # low, medium, high


class ABACPolicy:
    """Represents a single ABAC policy rule."""
    
    def __init__(self, name: str, effect: str, condition: Callable,
                 description: str = ""):
        self.name = name
        self.effect = effect  # "PERMIT" or "DENY"
        self.condition = condition
        self.description = description
    
    def evaluate(self, subject: Subject, resource: Resource,
                 action: Action, env: Environment) -> bool:
        try:
            return self.condition(subject, resource, action, env)
        except Exception:
            return False


class ABACEngine:
    """Policy Decision Point for ABAC."""
    
    def __init__(self, conflict_resolution: str = "deny_overrides"):
        self.policies: List[ABACPolicy] = []
        self.conflict_resolution = conflict_resolution
    
    def add_policy(self, policy: ABACPolicy):
        self.policies.append(policy)
    
    def evaluate(self, subject: Subject, resource: Resource,
                 action: Action, env: Environment) -> Dict[str, Any]:
        """Evaluate all policies and return decision."""
        
        permit_policies = []
        deny_policies = []
        
        for policy in self.policies:
            if policy.evaluate(subject, resource, action, env):
                if policy.effect == "PERMIT":
                    permit_policies.append(policy)
                else:
                    deny_policies.append(policy)
        
        # Conflict resolution
        if self.conflict_resolution == "deny_overrides":
            if deny_policies:
                decision = "DENY"
                reason = f"Denied by policies: {[p.name for p in deny_policies]}"
            elif permit_policies:
                decision = "PERMIT"
                reason = f"Permitted by policies: {[p.name for p in permit_policies]}"
            else:
                decision = "DENY"
                reason = "No applicable policies (default deny)"
        
        return {
            "decision": decision,
            "reason": reason,
            "subject": subject.name,
            "resource": resource.name,
            "action": action.name,
            "permit_policies": [p.name for p in permit_policies],
            "deny_policies": [p.name for p in deny_policies]
        }


def main():
    print("=" * 60)
    print("🎯 ABAC POLICY EVALUATOR")
    print("=" * 60)
    
    engine = ABACEngine(conflict_resolution="deny_overrides")
    
    # Define policies
    print("\n📜 Defining ABAC policies...")
    
    # Policy 1: Employees can read their department's documents
    engine.add_policy(ABACPolicy(
        name="Department_Read",
        effect="PERMIT",
        description="Employees can read resources in their department",
        condition=lambda s, r, a, e: (
            s.employment_type == "employee" and
            s.department == r.owner_department and
            a.name == "read" and
            r.type == "document"
        )
    ))
    
    # Policy 2: Clearance-based access
    engine.add_policy(ABACPolicy(
        name="Clearance_Access",
        effect="PERMIT",
        description="Users can access resources at or below their clearance",
        condition=lambda s, r, a, e: s.clearance >= r.classification
    ))
    
    # Policy 3: Business hours only for contractors
    engine.add_policy(ABACPolicy(
        name="Contractor_Business_Hours",
        effect="PERMIT",
        description="Contractors can only access during business hours",
        condition=lambda s, r, a, e: (
            s.employment_type == "contractor" and
            9 <= e.time.hour <= 17 and
            e.network == "corporate"
        )
    ))
    
    # Policy 4: Deny classified access from unmanaged devices
    engine.add_policy(ABACPolicy(
        name="No_Classified_On_Unmanaged",
        effect="DENY",
        description="Prevent access to classified resources from unmanaged devices",
        condition=lambda s, r, a, e: (
            r.classification >= 4 and
            not e.device_managed
        )
    ))
    
    # Policy 5: Deny during high threat
    engine.add_policy(ABACPolicy(
        name="High_Threat_Lockdown",
        effect="DENY",
        description="Restrict non-essential access during high threat",
        condition=lambda s, r, a, e: (
            e.threat_level == "high" and
            s.clearance < 4 and
            a.name in ["write", "delete"]
        )
    ))
    
    print("   ✅ 5 policies loaded")
    
    # Test scenarios
    scenarios = [
        {
            "name": "Employee reading department document",
            "subject": Subject("Alice", "Engineering", "Developer", 3, "employee"),
            "resource": Resource("API_Docs", "Engineering", 2, "document"),
            "action": Action("read"),
            "env": Environment(
                datetime(2024, 1, 15, 14, 0), "office", True, "corporate", "low"
            )
        },
        {
            "name": "Contractor accessing after hours",
            "subject": Subject("Bob", "Finance", "Analyst", 2, "contractor"),
            "resource": Resource("Q4_Report", "Finance", 2, "document"),
            "action": Action("read"),
            "env": Environment(
                datetime(2024, 1, 15, 20, 0), "home", True, "vpn", "low"
            )
        },
        {
            "name": "Classified doc on personal device",
            "subject": Subject("Charlie", "Engineering", "Senior Dev", 4, "employee"),
            "resource": Resource("Secret_Project", "Engineering", 5, "document"),
            "action": Action("read"),
            "env": Environment(
                datetime(2024, 1, 15, 10, 0), "cafe", False, "public", "low"
            )
        },
        {
            "name": "High threat lockdown",
            "subject": Subject("Diana", "Engineering", "Developer", 2, "employee"),
            "resource": Resource("Code_Repo", "Engineering", 2, "application"),
            "action": Action("write"),
            "env": Environment(
                datetime(2024, 1, 15, 10, 0), "office", True, "corporate", "high"
            )
        }
    ]
    
    print("\n🧪 Evaluating scenarios...")
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        print(f"   Subject: {scenario['subject'].name} ({scenario['subject'].department}, "
              f"clearance: {scenario['subject'].clearance}, {scenario['subject'].employment_type})")
        print(f"   Resource: {scenario['resource'].name} (classification: {scenario['resource'].classification})")
        print(f"   Action: {scenario['action'].name}")
        print(f"   Environment: {scenario['env'].time.strftime('%H:%M')}, "
              f"{scenario['env'].location}, managed={scenario['env'].device_managed}, "
              f"{scenario['env'].network}, threat={scenario['env'].threat_level}")
        
        result = engine.evaluate(
            scenario['subject'],
            scenario['resource'],
            scenario['action'],
            scenario['env']
        )
        
        icon = "✅" if result['decision'] == "PERMIT" else "❌"
        print(f"   {icon} DECISION: {result['decision']}")
        print(f"   Reason: {result['reason']}")


if __name__ == "__main__":
    main()
