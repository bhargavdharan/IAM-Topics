#!/usr/bin/env python3
"""
Authorization Engine
====================
Pluggable authorization engine supporting:
- DAC (Discretionary Access Control)
- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)

Run: python authorization_engine.py
"""

from typing import Dict, List, Set, Callable, Any
from dataclasses import dataclass, field


@dataclass
class AccessRequest:
    user: str
    resource: str
    action: str
    context: Dict[str, Any] = field(default_factory=dict)


class DACEngine:
    """Discretionary Access Control - owners decide."""
    
    def __init__(self):
        self.ownership: Dict[str, str] = {}  # resource -> owner
        self.acl: Dict[str, Dict[str, Set[str]]] = {}  # resource -> {user -> permissions}
    
    def set_owner(self, resource: str, owner: str):
        self.ownership[resource] = owner
        if resource not in self.acl:
            self.acl[resource] = {}
    
    def grant(self, owner: str, resource: str, user: str, permissions: Set[str]):
        if self.ownership.get(resource) != owner:
            print(f"   ❌ {owner} is not the owner of {resource}")
            return False
        
        if resource not in self.acl:
            self.acl[resource] = {}
        
        if user not in self.acl[resource]:
            self.acl[resource][user] = set()
        
        self.acl[resource][user].update(permissions)
        print(f"   ✅ {owner} granted {permissions} on {resource} to {user}")
        return True
    
    def check(self, request: AccessRequest) -> bool:
        perms = self.acl.get(request.resource, {}).get(request.user, set())
        return request.action in perms


class RBACEngine:
    """Role-Based Access Control."""
    
    def __init__(self):
        self.roles: Dict[str, Set[str]] = {}  # role -> {permissions}
        self.user_roles: Dict[str, Set[str]] = {}  # user -> {roles}
    
    def create_role(self, role: str, permissions: Set[str]):
        self.roles[role] = permissions
    
    def assign_role(self, user: str, role: str):
        if user not in self.user_roles:
            self.user_roles[user] = set()
        self.user_roles[user].add(role)
    
    def check(self, request: AccessRequest) -> bool:
        user_roles = self.user_roles.get(request.user, set())
        for role in user_roles:
            if request.action in self.roles.get(role, set()):
                return True
        return False


class ABACEngine:
    """Attribute-Based Access Control."""
    
    def __init__(self):
        self.policies: List[Dict] = []
    
    def add_policy(self, name: str, effect: str, condition: Callable):
        self.policies.append({"name": name, "effect": effect, "condition": condition})
    
    def check(self, request: AccessRequest) -> bool:
        allow_found = False
        
        for policy in self.policies:
            if policy["condition"](request):
                if policy["effect"] == "DENY":
                    return False
                elif policy["effect"] == "ALLOW":
                    allow_found = True
        
        return allow_found


class HybridEngine:
    """Combines multiple authorization models."""
    
    def __init__(self):
        self.dac = DACEngine()
        self.rbac = RBACEngine()
        self.abac = ABACEngine()
        self.mode = "rbac"
    
    def set_mode(self, mode: str):
        self.mode = mode
        print(f"\n🔄 Switched to {mode.upper()} mode")
    
    def check(self, request: AccessRequest) -> bool:
        if self.mode == "dac":
            return self.dac.check(request)
        elif self.mode == "rbac":
            return self.rbac.check(request)
        elif self.mode == "abac":
            return self.abac.check(request)
        return False
    
    def demo_scenario(self, scenario_name: str, requests: List[AccessRequest]):
        print(f"\n📋 Scenario: {scenario_name}")
        print("-" * 50)
        for req in requests:
            result = self.check(req)
            icon = "✅" if result else "❌"
            print(f"   {icon} {req.user} → {req.action} on {req.resource}")


def main():
    print("=" * 60)
    print("⚙️  AUTHORIZATION ENGINE")
    print("=" * 60)
    
    engine = HybridEngine()
    
    # Setup DAC
    print("\n🏗️  Setting up DAC (Discretionary Access Control)")
    engine.dac.set_owner("file_report.pdf", "alice")
    engine.dac.grant("alice", "file_report.pdf", "bob", {"read"})
    engine.dac.grant("alice", "file_report.pdf", "charlie", {"read", "write"})
    # Eve tries to grant access (not owner)
    engine.dac.grant("eve", "file_report.pdf", "diana", {"read"})
    
    # Setup RBAC
    print("\n🏗️  Setting up RBAC (Role-Based Access Control)")
    engine.rbac.create_role("Developer", {"read_code", "write_code", "run_tests"})
    engine.rbac.create_role("Manager", {"read_reports", "approve_expenses"})
    engine.rbac.create_role("Admin", {"read_code", "write_code", "manage_users", "delete_records"})
    
    engine.rbac.assign_role("alice", "Developer")
    engine.rbac.assign_role("bob", "Manager")
    engine.rbac.assign_role("charlie", "Admin")
    
    # Setup ABAC
    print("\n🏗️  Setting up ABAC (Attribute-Based Access Control)")
    engine.abac.add_policy(
        "Business_Hours",
        "ALLOW",
        lambda r: r.context.get("time", 0) >= 9 and r.context.get("time", 0) <= 17
    )
    engine.abac.add_policy(
        "No_Delete_After_Hours",
        "DENY",
        lambda r: r.action == "delete" and r.context.get("time", 0) > 17
    )
    engine.abac.add_policy(
        "Corporate_Network",
        "ALLOW",
        lambda r: r.context.get("network") == "corporate"
    )
    
    # Demo scenarios
    print("\n" + "=" * 60)
    print("🧪 TESTING SCENARIOS")
    print("=" * 60)
    
    # DAC Demo
    engine.set_mode("dac")
    engine.demo_scenario("DAC: File sharing", [
        AccessRequest("bob", "file_report.pdf", "read"),
        AccessRequest("charlie", "file_report.pdf", "write"),
        AccessRequest("bob", "file_report.pdf", "delete"),
    ])
    
    # RBAC Demo
    engine.set_mode("rbac")
    engine.demo_scenario("RBAC: Role permissions", [
        AccessRequest("alice", "code_repo", "write_code"),
        AccessRequest("alice", "expenses", "approve_expenses"),
        AccessRequest("bob", "expenses", "approve_expenses"),
        AccessRequest("charlie", "users", "manage_users"),
    ])
    
    # ABAC Demo
    engine.set_mode("abac")
    engine.demo_scenario("ABAC: Context-aware access (10 AM, corporate)", [
        AccessRequest("alice", "docs", "read", {"time": 10, "network": "corporate"}),
        AccessRequest("bob", "docs", "delete", {"time": 10, "network": "corporate"}),
    ])
    
    engine.demo_scenario("ABAC: Context-aware access (8 PM, home)", [
        AccessRequest("alice", "docs", "read", {"time": 20, "network": "home"}),
        AccessRequest("bob", "docs", "delete", {"time": 20, "network": "home"}),
    ])
    
    print("\n" + "=" * 60)
    print("💡 COMPARISON")
    print("=" * 60)
    print("DAC: Flexible, but owners can make mistakes")
    print("RBAC: Scalable, aligns with org structure")
    print("ABAC: Most flexible, considers context (time, location, etc.)")
    print("Hybrid: Use RBAC for coarse-grained, ABAC for fine-grained")


if __name__ == "__main__":
    main()
