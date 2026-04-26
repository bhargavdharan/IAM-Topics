#!/usr/bin/env python3
"""
Identity Lifecycle Simulator
============================
Simulates the complete IAM lifecycle for an organization:
- Onboarding new employees with role-based provisioning
- Simulating role changes and access modifications
- Handling offboarding with access revocation
- Generating audit reports for compliance

Run: python identity_lifecycle_sim.py
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class User:
    """Represents a user in the IAM system."""
    
    def __init__(self, user_id: str, name: str, department: str, role: str):
        self.user_id = user_id
        self.name = name
        self.department = department
        self.role = role
        self.status = "active"  # active, suspended, terminated
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.permissions: List[str] = []
        self.audit_log: List[Dict] = []
        
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "department": self.department,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "permissions": self.permissions
        }
    
    def log_event(self, action: str, details: str):
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        })


class IAMSystem:
    """Simulates an Identity and Access Management system."""
    
    ROLE_PERMISSIONS = {
        "Intern": ["read_shared_docs", "use_email"],
        "Developer": ["read_shared_docs", "use_email", "access_code_repo", "use_dev_tools"],
        "Senior Developer": ["read_shared_docs", "use_email", "access_code_repo", "use_dev_tools", 
                             "approve_code_changes", "access_staging"],
        "Manager": ["read_shared_docs", "use_email", "access_hr_data", "approve_expenses", 
                    "manage_team_access"],
        "Admin": ["read_shared_docs", "use_email", "access_code_repo", "use_dev_tools",
                  "approve_code_changes", "access_staging", "access_production", 
                  "manage_all_users", "view_audit_logs"]
    }
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.audit_log: List[Dict] = []
        
    def log_system_event(self, action: str, user_id: str, details: str):
        event = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user_id": user_id,
            "details": details
        }
        self.audit_log.append(event)
        print(f"  [AUDIT] {action}: {details}")
    
    def provision_user(self, name: str, department: str, role: str) -> User:
        """Stage 1: Provision - Create a new user with appropriate access."""
        user_id = f"USR-{len(self.users)+1000:04d}"
        user = User(user_id, name, department, role)
        
        # Assign permissions based on role
        user.permissions = self.ROLE_PERMISSIONS.get(role, ["read_shared_docs"]).copy()
        
        self.users[user_id] = user
        user.log_event("PROVISION", f"User provisioned with role {role}")
        self.log_system_event("PROVISION", user_id, f"{name} joined as {role} in {department}")
        
        print(f"\n🟢 PROVISIONED: {name} ({user_id})")
        print(f"   Role: {role} | Department: {department}")
        print(f"   Permissions: {', '.join(user.permissions)}")
        return user
    
    def change_role(self, user_id: str, new_role: str):
        """Simulate role change (promotion, transfer, etc.)."""
        if user_id not in self.users:
            print(f"❌ User {user_id} not found")
            return
            
        user = self.users[user_id]
        old_role = user.role
        old_perms = set(user.permissions)
        
        user.role = new_role
        user.permissions = self.ROLE_PERMISSIONS.get(new_role, []).copy()
        user.modified_at = datetime.now()
        
        new_perms = set(user.permissions)
        added = new_perms - old_perms
        removed = old_perms - new_perms
        
        user.log_event("ROLE_CHANGE", f"Changed from {old_role} to {new_role}")
        self.log_system_event("ROLE_CHANGE", user_id, 
                              f"Role changed: {old_role} → {new_role}")
        
        print(f"\n🔄 ROLE CHANGE: {user.name} ({user_id})")
        print(f"   {old_role} → {new_role}")
        if added:
            print(f"   ➕ Added permissions: {', '.join(added)}")
        if removed:
            print(f"   ➖ Removed permissions: {', '.join(removed)}")
    
    def suspend_user(self, user_id: str, reason: str):
        """Temporarily disable access."""
        if user_id not in self.users:
            return
            
        user = self.users[user_id]
        user.status = "suspended"
        user.log_event("SUSPEND", reason)
        self.log_system_event("SUSPEND", user_id, reason)
        
        print(f"\n🟡 SUSPENDED: {user.name} ({user_id})")
        print(f"   Reason: {reason}")
        print(f"   All access temporarily revoked")
    
    def deprovision_user(self, user_id: str, reason: str):
        """Stage 5: Deprovision - Remove all access permanently."""
        if user_id not in self.users:
            return
            
        user = self.users[user_id]
        user.status = "terminated"
        revoked_perms = user.permissions.copy()
        user.permissions = []
        user.modified_at = datetime.now()
        
        user.log_event("DEPROVISION", reason)
        self.log_system_event("DEPROVISION", user_id, reason)
        
        print(f"\n🔴 DEPROVISIONED: {user.name} ({user_id})")
        print(f"   Reason: {reason}")
        print(f"   Revoked permissions: {', '.join(revoked_perms)}")
        print(f"   ⚠️  Account disabled. All access removed.")
    
    def check_access(self, user_id: str, permission: str) -> bool:
        """Simulate authorization check."""
        if user_id not in self.users:
            return False
            
        user = self.users[user_id]
        allowed = user.status == "active" and permission in user.permissions
        
        self.log_system_event("ACCESS_CHECK", user_id, 
                              f"{permission} → {'ALLOWED' if allowed else 'DENIED'}")
        return allowed
    
    def generate_audit_report(self):
        """Generate compliance audit report."""
        print("\n" + "="*60)
        print("📊 IAM AUDIT REPORT")
        print("="*60)
        print(f"Generated: {datetime.now().isoformat()}")
        print(f"Total Users: {len(self.users)}")
        print(f"Active: {sum(1 for u in self.users.values() if u.status == 'active')}")
        print(f"Suspended: {sum(1 for u in self.users.values() if u.status == 'suspended')}")
        print(f"Terminated: {sum(1 for u in self.users.values() if u.status == 'terminated')}")
        
        print("\n--- User Access Summary ---")
        for user in self.users.values():
            status_icon = "🟢" if user.status == "active" else "🟡" if user.status == "suspended" else "🔴"
            print(f"{status_icon} {user.name} ({user.user_id}) - {user.role}")
            print(f"   Permissions: {', '.join(user.permissions) if user.permissions else 'NONE'}")
        
        print("\n--- System Audit Log ---")
        for event in self.audit_log:
            print(f"[{event['timestamp']}] {event['action']}: {event['details']}")
        
        print("="*60)


def main():
    print("🏢 Identity Lifecycle Simulator")
    print("Simulating IAM lifecycle: Provision → Authenticate → Authorize → Monitor → Deprovision\n")
    
    iam = IAMSystem()
    
    # Scenario: Company hires 3 employees
    print("─" * 50)
    print("📅 DAY 1: New hires join the company")
    print("─" * 50)
    
    alice = iam.provision_user("Alice Johnson", "Engineering", "Developer")
    bob = iam.provision_user("Bob Smith", "Finance", "Manager")
    charlie = iam.provision_user("Charlie Davis", "Engineering", "Intern")
    
    # Simulate access checks
    print("\n📋 Access checks:")
    iam.check_access(alice.user_id, "access_code_repo")
    iam.check_access(charlie.user_id, "access_code_repo")
    iam.check_access(bob.user_id, "access_hr_data")
    
    # Scenario: Role change
    print("\n" + "─" * 50)
    print("📅 DAY 90: Alice gets promoted")
    print("─" * 50)
    iam.change_role(alice.user_id, "Senior Developer")
    
    # Scenario: Suspicious activity
    print("\n" + "─" * 50)
    print("📅 DAY 120: Security incident")
    print("─" * 50)
    iam.suspend_user(charlie.user_id, "Suspicious login attempts from foreign IP")
    iam.check_access(charlie.user_id, "read_shared_docs")
    
    # Scenario: Offboarding
    print("\n" + "─" * 50)
    print("📅 DAY 365: Bob leaves the company")
    print("─" * 50)
    iam.deprovision_user(bob.user_id, "Employee resignation")
    
    # Final audit
    iam.generate_audit_report()
    
    # Save to JSON for further analysis
    with open("iam_lifecycle_report.json", "w") as f:
        json.dump({
            "users": [u.to_dict() for u in iam.users.values()],
            "audit_log": iam.audit_log
        }, f, indent=2)
    print("\n💾 Report saved to iam_lifecycle_report.json")


if __name__ == "__main__":
    main()
