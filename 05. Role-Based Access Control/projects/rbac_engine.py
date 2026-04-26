#!/usr/bin/env python3
"""
RBAC Engine
===========
Full-featured Role-Based Access Control implementation:
- User-role assignment and revocation
- Role-permission grants
- Role hierarchy with inheritance
- Session management with role activation
- Static and Dynamic SoD enforcement

Run: python rbac_engine.py
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field


@dataclass
class Role:
    name: str
    permissions: Set[str] = field(default_factory=set)
    parents: List["Role"] = field(default_factory=list)
    
    def get_all_permissions(self, visited: Set[str] = None) -> Set[str]:
        """Recursively get all permissions including inherited ones."""
        if visited is None:
            visited = set()
        if self.name in visited:
            return set()  # Prevent circular inheritance
        visited.add(self.name)
        
        all_perms = self.permissions.copy()
        for parent in self.parents:
            all_perms.update(parent.get_all_permissions(visited))
        return all_perms
    
    def __repr__(self):
        return f"Role({self.name})"


@dataclass
class User:
    username: str
    assigned_roles: List[Role] = field(default_factory=list)
    active_roles: List[Role] = field(default_factory=list)
    
    def activate_role(self, role: Role):
        if role in self.assigned_roles and role not in self.active_roles:
            self.active_roles.append(role)
    
    def deactivate_role(self, role: Role):
        if role in self.active_roles:
            self.active_roles.remove(role)
    
    def get_active_permissions(self) -> Set[str]:
        perms = set()
        for role in self.active_roles:
            perms.update(role.get_all_permissions())
        return perms
    
    def __repr__(self):
        return f"User({self.username})"


class RBACSystem:
    """Complete RBAC system with hierarchy, sessions, and constraints."""
    
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.sod_constraints: List[Set[str]] = []  # List of mutually exclusive role sets
        self.audit_log: List[str] = []
    
    def log(self, message: str):
        self.audit_log.append(message)
        print(f"   [LOG] {message}")
    
    def create_role(self, name: str, permissions: List[str] = None) -> Role:
        role = Role(name=name, permissions=set(permissions or []))
        self.roles[name] = role
        self.log(f"Created role: {name} with permissions: {permissions or []}")
        return role
    
    def set_role_hierarchy(self, child_name: str, parent_name: str):
        """Make child role inherit from parent role."""
        if child_name not in self.roles or parent_name not in self.roles:
            raise ValueError("Role not found")
        
        child = self.roles[child_name]
        parent = self.roles[parent_name]
        
        # Check for circular inheritance
        if child_name in [r.name for r in parent.get_all_permissions()]:
            raise ValueError("Circular inheritance detected!")
        
        child.parents.append(parent)
        self.log(f"Set hierarchy: {child_name} inherits from {parent_name}")
    
    def add_user(self, username: str) -> User:
        user = User(username=username)
        self.users[username] = user
        self.log(f"Added user: {username}")
        return user
    
    def assign_role(self, username: str, role_name: str):
        """Assign a role to a user (Static assignment)."""
        if username not in self.users or role_name not in self.roles:
            raise ValueError("User or role not found")
        
        # Check Static SoD
        user = self.users[username]
        new_role = self.roles[role_name]
        
        for constraint in self.sod_constraints:
            if role_name in constraint:
                # Check if user already has any conflicting role
                assigned_names = {r.name for r in user.assigned_roles}
                conflicts = constraint & assigned_names
                if conflicts:
                    conflict = conflicts.pop()
                    raise PermissionError(
                        f"Static SoD violation: Cannot assign '{role_name}' "
                        f"because user already has '{conflict}'"
                    )
        
        user.assigned_roles.append(new_role)
        # Also activate by default
        user.activate_role(new_role)
        self.log(f"Assigned role '{role_name}' to user '{username}'")
    
    def revoke_role(self, username: str, role_name: str):
        if username not in self.users:
            return
        user = self.users[username]
        role = self.roles.get(role_name)
        if role:
            if role in user.assigned_roles:
                user.assigned_roles.remove(role)
            if role in user.active_roles:
                user.active_roles.remove(role)
            self.log(f"Revoked role '{role_name}' from user '{username}'")
    
    def add_sod_constraint(self, role_names: List[str]):
        """Add Static Separation of Duties constraint."""
        self.sod_constraints.append(set(role_names))
        self.log(f"Added SoD constraint: {role_names}")
    
    def check_access(self, username: str, permission: str) -> bool:
        """Check if user has permission through active roles."""
        if username not in self.users:
            return False
        
        user = self.users[username]
        perms = user.get_active_permissions()
        allowed = permission in perms
        
        self.log(f"Access check: {username} → {permission}: {'ALLOWED' if allowed else 'DENIED'}")
        return allowed
    
    def check_dynamic_sod(self, username: str, new_role_name: str) -> bool:
        """Check Dynamic SoD: prevent activating conflicting roles in same session."""
        if username not in self.users:
            return False
        
        user = self.users[username]
        active_names = {r.name for r in user.active_roles}
        
        for constraint in self.sod_constraints:
            if new_role_name in constraint:
                conflicts = constraint & active_names
                if conflicts:
                    self.log(f"Dynamic SoD violation: Cannot activate '{new_role_name}' "
                            f"while '{conflicts.pop()}' is active")
                    return False
        return True
    
    def display_role_hierarchy(self):
        print("\n📊 ROLE HIERARCHY")
        for name, role in self.roles.items():
            perms = role.permissions
            parents = [p.name for p in role.parents]
            all_perms = role.get_all_permissions()
            print(f"   {name}")
            print(f"      Direct permissions: {perms}")
            print(f"      Parents: {parents}")
            print(f"      All permissions (with inheritance): {all_perms}")
            print()


def main():
    print("=" * 60)
    print("🔐 RBAC ENGINE DEMONSTRATION")
    print("=" * 60)
    
    rbac = RBACSystem()
    
    # Create role hierarchy
    print("\n🏗️  Creating role hierarchy...")
    rbac.create_role("Employee", ["read_email", "view_calendar"])
    rbac.create_role("Developer", ["read_code", "write_code", "run_tests"])
    rbac.create_role("Senior Developer", ["approve_prs", "deploy_staging"])
    rbac.create_role("Manager", ["approve_expenses", "view_team_metrics"])
    rbac.create_role("Admin", ["manage_users", "manage_systems"])
    rbac.create_role("Auditor", ["view_audit_logs", "read_all_reports"])
    
    # Set up inheritance
    rbac.set_role_hierarchy("Developer", "Employee")
    rbac.set_role_hierarchy("Senior Developer", "Developer")
    rbac.set_role_hierarchy("Manager", "Employee")
    
    rbac.display_role_hierarchy()
    
    # Add users
    print("\n👥 Adding users...")
    rbac.add_user("alice")
    rbac.add_user("bob")
    rbac.add_user("charlie")
    rbac.add_user("diana")
    
    # Assign roles
    print("\n📝 Assigning roles...")
    rbac.assign_role("alice", "Senior Developer")
    rbac.assign_role("bob", "Manager")
    rbac.assign_role("charlie", "Developer")
    rbac.assign_role("diana", "Auditor")
    
    # SoD Constraint: Developer and Auditor should not be same person
    print("\n⚖️  Adding Separation of Duties constraints...")
    rbac.add_sod_constraint(["Developer", "Auditor"])
    
    # Try to violate Static SoD
    print("\n🧪 Testing Static SoD violation...")
    try:
        rbac.assign_role("alice", "Auditor")  # Alice is already Developer
    except PermissionError as e:
        print(f"   🚨 BLOCKED: {e}")
    
    # Access checks
    print("\n🔑 Access checks...")
    rbac.check_access("alice", "write_code")
    rbac.check_access("alice", "approve_prs")
    rbac.check_access("alice", "manage_users")
    rbac.check_access("bob", "view_team_metrics")
    rbac.check_access("charlie", "read_email")  # Inherited from Employee
    
    # Dynamic SoD: Session management
    print("\n🎭 Session management (Dynamic SoD)...")
    user = rbac.users["diana"]
    
    # Deactivate Auditor, try to activate Developer (would violate SoD)
    print(f"   Diana's active roles: {[r.name for r in user.active_roles]}")
    
    # Bob tries to activate both Manager and Developer in same session
    print("\n🧪 Testing Dynamic SoD in session...")
    # First, let's give Bob Developer role too
    rbac.assign_role("bob", "Developer")
    
    # Now he has both Manager and Developer assigned
    print(f"   Bob's assigned roles: {[r.name for r in rbac.users['bob'].assigned_roles]}")
    
    # Deactivate both and try to activate conflicting ones
    user_bob = rbac.users["bob"]
    for role in list(user_bob.active_roles):
        user_bob.deactivate_role(role)
    
    # Add SoD for Manager and Admin
    rbac.add_sod_constraint(["Manager", "Admin"])
    
    # Activate Manager
    user_bob.activate_role(rbac.roles["Manager"])
    print(f"   Bob activated Manager")
    
    # Try to activate Admin in same session
    can_activate = rbac.check_dynamic_sod("bob", "Admin")
    if can_activate:
        user_bob.activate_role(rbac.roles["Admin"])
    
    print(f"   Bob's active roles: {[r.name for r in user_bob.active_roles]}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 RBAC SYSTEM SUMMARY")
    print("=" * 60)
    for username, user in rbac.users.items():
        print(f"\n👤 {username}:")
        print(f"   Assigned: {[r.name for r in user.assigned_roles]}")
        print(f"   Active:   {[r.name for r in user.active_roles]}")
        print(f"   Permissions: {user.get_active_permissions()}")
    
    print("\n💡 KEY CONCEPTS DEMONSTRATED:")
    print("   • Role hierarchy with permission inheritance")
    print("   • Static SoD (role assignment time)")
    print("   • Dynamic SoD (session activation time)")
    print("   • Session-based role activation")
    print("=" * 60)


if __name__ == "__main__":
    main()
