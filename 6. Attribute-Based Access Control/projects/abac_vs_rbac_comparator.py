#!/usr/bin/env python3
"""
ABAC vs RBAC Comparator
=======================
Compares ABAC and RBAC for the same scenarios:
- Shows how RBAC requires many roles
- Demonstrates ABAC's flexibility
- Calculates administrative overhead

Run: python abac_vs_rbac_comparator.py
"""

from typing import Dict, List, Set


class RBACScenario:
    def __init__(self):
        self.roles = []
        self.user_assignments = {}
    
    def add_role(self, name: str):
        self.roles.append(name)
    
    def assign(self, user: str, role: str):
        if user not in self.user_assignments:
            self.user_assignments[user] = []
        self.user_assignments[user].append(role)
    
    def count(self) -> Dict:
        return {
            "roles": len(self.roles),
            "assignments": sum(len(v) for v in self.user_assignments.values()),
            "details": self.user_assignments
        }


class ABACScenario:
    def __init__(self):
        self.policies = []
    
    def add_policy(self, description: str):
        self.policies.append(description)
    
    def count(self) -> Dict:
        return {
            "policies": len(self.policies),
            "details": self.policies
        }


def compare_scenarios():
    print("=" * 60)
    print("⚖️  ABAC vs RBAC COMPARATOR")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "Multi-department project access",
            "description": "Users need access based on department + project + time",
            "rbac_setup": lambda rbac: setup_multidept_rbac(rbac),
            "abac_setup": lambda abac: setup_multidept_abac(abac)
        },
        {
            "name": "Remote work access control",
            "description": "Different access based on location and device",
            "rbac_setup": lambda rbac: setup_remote_rbac(rbac),
            "abac_setup": lambda abac: setup_remote_abac(abac)
        },
        {
            "name": "Contractor time-limited access",
            "description": "Contractors need access only during contracts",
            "rbac_setup": lambda rbac: setup_contractor_rbac(rbac),
            "abac_setup": lambda abac: setup_contractor_abac(abac)
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        print(f"   {scenario['description']}")
        print("-" * 60)
        
        rbac = RBACScenario()
        abac = ABACScenario()
        
        scenario['rbac_setup'](rbac)
        scenario['abac_setup'](abac)
        
        rbac_stats = rbac.count()
        abac_stats = abac.count()
        
        print(f"\n   RBAC Approach:")
        print(f"      Roles needed: {rbac_stats['roles']}")
        print(f"      User-role assignments: {rbac_stats['assignments']}")
        print(f"      Administrative overhead: HIGH")
        
        print(f"\n   ABAC Approach:")
        print(f"      Policies needed: {abac_stats['policies']}")
        print(f"      Administrative overhead: LOW")
        print(f"      Flexibility: HIGH")
        
        reduction = ((rbac_stats['roles'] - abac_stats['policies']) / max(rbac_stats['roles'], 1)) * 100
        print(f"\n   📊 Result: ABAC uses {reduction:.0f}% fewer policy objects")


def setup_multidept_rbac(rbac):
    """RBAC needs a role for every department-project combination."""
    departments = ["Engineering", "Finance", "HR"]
    projects = ["Alpha", "Beta", "Gamma"]
    
    for dept in departments:
        for proj in projects:
            rbac.add_role(f"{dept}_{proj}_Member")
            rbac.add_role(f"{dept}_{proj}_Lead")
    
    # Assign users
    rbac.assign("alice", "Engineering_Alpha_Member")
    rbac.assign("bob", "Finance_Beta_Lead")
    rbac.assign("charlie", "HR_Gamma_Member")


def setup_multidept_abac(abac):
    """ABAC needs just a few policies."""
    abac.add_policy("Allow if user.department == resource.project_department")
    abac.add_policy("Allow if user.role == 'Lead' AND resource.sensitivity <= 3")
    abac.add_policy("Deny if user.status != 'active'")


def setup_remote_rbac(rbac):
    """RBAC needs roles for every location-device combination."""
    locations = ["Office", "Home", "Travel"]
    devices = ["Corporate", "Personal"]
    
    for loc in locations:
        for dev in devices:
            rbac.add_role(f"{loc}_{dev}_User")
    
    rbac.assign("alice", "Office_Corporate_User")
    rbac.assign("alice", "Home_Corporate_User")
    rbac.assign("bob", "Travel_Personal_User")


def setup_remote_abac(abac):
    """ABAC handles this with context attributes."""
    abac.add_policy("Allow if location == 'office' AND device.managed == true")
    abac.add_policy("Allow if location == 'home' AND device.managed == true AND mfa == true")
    abac.add_policy("Deny if location == 'travel' AND device.managed == false")


def setup_contractor_rbac(rbac):
    """RBAC needs to create and delete roles for each contract."""
    for month in range(1, 13):
        rbac.add_role(f"Contractor_M{month}")
    
    rbac.assign("contractor1", "Contractor_M1")
    rbac.assign("contractor1", "Contractor_M2")
    rbac.assign("contractor1", "Contractor_M3")


def setup_contractor_abac(abac):
    """ABAC handles time-based access naturally."""
    abac.add_policy("Allow if user.type == 'contractor' AND now < user.contract_end")
    abac.add_policy("Deny if user.type == 'contractor' AND now > user.contract_end")


def main():
    compare_scenarios()
    
    print("\n" + "=" * 60)
    print("💡 WHEN TO USE WHICH")
    print("=" * 60)
    print("\nUse RBAC when:")
    print("   • Organization is small to medium")
    print("   • Job roles are well-defined and stable")
    print("   • Access doesn't depend on time/location/context")
    print("   • You need simple administration")
    
    print("\nUse ABAC when:")
    print("   • Organization is large or complex")
    print("   • Access depends on context (time, location, device)")
    print("   • You have many dynamic attributes")
    print("   • You need fine-grained, dynamic policies")
    
    print("\nHybrid approach (recommended for most enterprises):")
    print("   • Use RBAC for coarse-grained access (job functions)")
    print("   • Use ABAC for fine-grained constraints (time, location)")
    print("   • Example: 'Developer' role + 'only from office during business hours'")


if __name__ == "__main__":
    main()
