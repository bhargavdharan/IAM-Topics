#!/usr/bin/env python3
"""
Access Matrix Visualizer
========================
Creates and visualizes access control matrices.
Demonstrates ACL vs Capability List views and checks for
privilege escalation paths and SoD constraints.

Run: python access_matrix_visualizer.py
"""

from typing import Dict, List, Set, Tuple


class AccessControlMatrix:
    """Represents an access control matrix with users, resources, and permissions."""
    
    PERMISSIONS = {
        "r": "Read",
        "w": "Write", 
        "x": "Execute",
        "d": "Delete",
        "a": "Admin"
    }
    
    def __init__(self):
        self.users: List[str] = []
        self.resources: List[str] = []
        self.matrix: Dict[str, Dict[str, Set[str]]] = {}
    
    def add_user(self, user: str):
        if user not in self.users:
            self.users.append(user)
            self.matrix[user] = {}
    
    def add_resource(self, resource: str):
        if resource not in self.resources:
            self.resources.append(resource)
    
    def grant(self, user: str, resource: str, permissions: str):
        """Grant permissions (e.g., 'rw' for read+write)."""
        self.add_user(user)
        self.add_resource(resource)
        self.matrix[user][resource] = set(permissions)
    
    def revoke(self, user: str, resource: str):
        if user in self.matrix and resource in self.matrix[user]:
            del self.matrix[user][resource]
    
    def check(self, user: str, resource: str, permission: str) -> bool:
        if user not in self.matrix:
            return False
        if resource not in self.matrix[user]:
            return False
        return permission in self.matrix[user][resource]
    
    def display_matrix(self):
        """Display the full access control matrix."""
        print("\n📊 ACCESS CONTROL MATRIX")
        print("-" * (15 + len(self.resources) * 12))
        
        # Header
        header = f"{'User':<15}"
        for res in self.resources:
            header += f"{res:<12}"
        print(header)
        print("-" * (15 + len(self.resources) * 12))
        
        # Rows
        for user in self.users:
            row = f"{user:<15}"
            for res in self.resources:
                perms = "".join(sorted(self.matrix[user].get(res, set())))
                row += f"{perms or '-':<12}"
            print(row)
        
        print("\nLegend: r=Read, w=Write, x=Execute, d=Delete, a=Admin")
    
    def get_acl_view(self) -> Dict[str, List[Tuple[str, str]]]:
        """Return Access Control List view (permissions per resource)."""
        acl = {}
        for res in self.resources:
            acl[res] = []
            for user in self.users:
                perms = "".join(sorted(self.matrix[user].get(res, set())))
                if perms:
                    acl[res].append((user, perms))
        return acl
    
    def get_capability_view(self) -> Dict[str, List[Tuple[str, str]]]:
        """Return Capability List view (permissions per user)."""
        caps = {}
        for user in self.users:
            caps[user] = []
            for res in self.resources:
                perms = "".join(sorted(self.matrix[user].get(res, set())))
                if perms:
                    caps[user].append((res, perms))
        return caps
    
    def check_sod(self, conflicting_pairs: List[Tuple[str, str]]) -> List[Dict]:
        """Check for Separation of Duties violations."""
        violations = []
        
        for user in self.users:
            user_perms = set()
            for res in self.resources:
                user_perms.update(self.matrix[user].get(res, set()))
            
            for perm1, perm2 in conflicting_pairs:
                if perm1 in user_perms and perm2 in user_perms:
                    violations.append({
                        "user": user,
                        "conflict": (perm1, perm2),
                        "message": f"{user} has both '{perm1}' and '{perm2}'"
                    })
        
        return violations
    
    def find_privilege_escalation(self) -> List[Dict]:
        """Find potential privilege escalation paths."""
        issues = []
        
        # Check for users with admin on user-management resources
        # who also have access to sensitive resources
        for user in self.users:
            has_admin = False
            sensitive_access = []
            
            for res in self.resources:
                perms = self.matrix[user].get(res, set())
                if "a" in perms:
                    has_admin = True
                if any(p in perms for p in ["w", "d", "a"]):
                    if "user" in res.lower() or "admin" in res.lower():
                        pass  # Admin resources
                    else:
                        sensitive_access.append(res)
            
            if has_admin and sensitive_access:
                issues.append({
                    "user": user,
                    "risk": "Admin access + sensitive resource access",
                    "resources": sensitive_access
                })
        
        return issues


def main():
    print("=" * 60)
    print("🔐 ACCESS MATRIX VISUALIZER")
    print("=" * 60)
    
    acm = AccessControlMatrix()
    
    # Setup a company scenario
    print("\n🏢 Setting up corporate access control...")
    
    users = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    resources = [
        "Public_Website",
        "HR_Database", 
        "Finance_Reports",
        "Code_Repository",
        "User_Admin_Panel",
        "Production_Servers"
    ]
    
    for u in users:
        acm.add_user(u)
    for r in resources:
        acm.add_resource(r)
    
    # Grant permissions based on roles
    acm.grant("Alice", "Public_Website", "rwa")
    acm.grant("Alice", "Code_Repository", "rwx")
    
    acm.grant("Bob", "HR_Database", "rw")
    acm.grant("Bob", "Finance_Reports", "r")
    
    acm.grant("Charlie", "Public_Website", "r")
    acm.grant("Charlie", "Code_Repository", "r")
    
    acm.grant("Diana", "Finance_Reports", "rwa")
    acm.grant("Diana", "HR_Database", "r")
    
    acm.grant("Eve", "User_Admin_Panel", "rwa")
    acm.grant("Eve", "Production_Servers", "rwxd")
    
    # Display matrix
    acm.display_matrix()
    
    # ACL View
    print("\n📋 ACCESS CONTROL LIST (ACL) VIEW")
    print("   (Stored with the resource)")
    acl = acm.get_acl_view()
    for res, entries in acl.items():
        print(f"   {res}: {entries}")
    
    # Capability View
    print("\n🔑 CAPABILITY LIST VIEW")
    print("   (Stored with the user)")
    caps = acm.get_capability_view()
    for user, entries in caps.items():
        print(f"   {user}: {entries}")
    
    # SoD Check
    print("\n⚖️  SEPARATION OF DUTIES CHECK")
    print("   Rule: No one should have both Write and Admin on financial resources")
    sod_pairs = [("w", "a")]
    violations = acm.check_sod(sod_pairs)
    if violations:
        for v in violations:
            print(f"   🚨 VIOLATION: {v['message']}")
    else:
        print("   ✅ No SoD violations found")
    
    # Privilege escalation check
    print("\n🚨 PRIVILEGE ESCALATION CHECK")
    issues = acm.find_privilege_escalation()
    if issues:
        for issue in issues:
            print(f"   ⚠️  {issue['user']}: {issue['risk']}")
            print(f"      Resources: {', '.join(issue['resources'])}")
    else:
        print("   ✅ No obvious escalation paths")
    
    # Access check demo
    print("\n🧪 ACCESS CHECKS")
    checks = [
        ("Alice", "Code_Repository", "w"),
        ("Bob", "Production_Servers", "w"),
        ("Charlie", "Finance_Reports", "r"),
    ]
    for user, res, perm in checks:
        allowed = acm.check(user, res, perm)
        status = "✅ ALLOWED" if allowed else "❌ DENIED"
        print(f"   {user} → {res} ({perm}): {status}")


if __name__ == "__main__":
    main()
