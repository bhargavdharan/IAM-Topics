#!/usr/bin/env python3
"""
Access Review Campaign Simulator
================================
Simulates an access review campaign:
- Generates users, roles, and permissions
- Creates review assignments
- Processes certification decisions
- Applies revocations and generates reports

Run: python access_review_sim.py
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class UserAccess:
    user_name: str
    manager: str
    role: str
    resource: str
    last_used: datetime
    certified: bool = True
    reviewer_comment: str = ""


class AccessReviewCampaign:
    """Simulates an access review campaign."""
    
    def __init__(self, name: str):
        self.name = name
        self.access_items: List[UserAccess] = []
        self.violations: List[Dict] = []
        self.start_date = datetime.now()
        self.end_date = self.start_date + timedelta(days=14)
    
    def generate_sample_data(self):
        """Generate sample access data."""
        users = [
            ("Alice", "Manager_A", "Developer"),
            ("Bob", "Manager_A", "Developer"),
            ("Charlie", "Manager_B", "Finance_Analyst"),
            ("Diana", "Manager_B", "Finance_Manager"),
            ("Eve", "Manager_C", "Admin"),
            ("Frank", "Manager_A", "Developer"),
        ]
        
        resources_by_role = {
            "Developer": ["Code_Repo", "Dev_Tools", "Staging_Environment", "Jira"],
            "Finance_Analyst": ["ERP_System", "Financial_Reports", "Excel_Online"],
            "Finance_Manager": ["ERP_System", "Financial_Reports", "Budget_Tool", "Approval_Workflow"],
            "Admin": ["Production_Servers", "User_Admin_Panel", "All_Databases", "Network_Config"]
        }
        
        for user, manager, role in users:
            resources = resources_by_role.get(role, [])
            for resource in resources:
                # Some access is old and unused
                days_ago = random.randint(1, 180)
                last_used = datetime.now() - timedelta(days=days_ago)
                
                self.access_items.append(UserAccess(
                    user_name=user,
                    manager=manager,
                    role=role,
                    resource=resource,
                    last_used=last_used
                ))
        
        # Add some suspicious access (privilege creep)
        self.access_items.append(UserAccess(
            user_name="Alice",
            manager="Manager_A",
            role="Developer",
            resource="Production_Servers",  # Developer shouldn't have this
            last_used=datetime.now() - timedelta(days=120)
        ))
        
        self.access_items.append(UserAccess(
            user_name="Eve",
            manager="Manager_C",
            role="Admin",
            resource="Financial_Reports",  # Admin has everything anyway
            last_used=datetime.now() - timedelta(days=5)
        ))
    
    def simulate_reviews(self):
        """Simulate managers reviewing access."""
        print("\n📋 Managers reviewing access...")
        
        for item in self.access_items:
            # Simulate decision logic
            days_since_use = (datetime.now() - item.last_used).days
            
            # If not used for 90+ days, likely revoke
            if days_since_use > 90:
                item.certified = False
                item.reviewer_comment = f"Not used for {days_since_use} days"
            # If suspicious access (developer + prod)
            elif item.user_name == "Alice" and item.resource == "Production_Servers":
                item.certified = False
                item.reviewer_comment = "Developer should not have production access"
            else:
                item.certified = True
                item.reviewer_comment = "Still needed for job function"
    
    def apply_decisions(self):
        """Apply review decisions."""
        print("\n🔄 Applying review decisions...")
        
        revoked = [item for item in self.access_items if not item.certified]
        kept = [item for item in self.access_items if item.certified]
        
        print(f"   ✅ Certified (kept): {len(kept)} access grants")
        print(f"   ❌ Revoked: {len(revoked)} access grants")
        
        if revoked:
            print("\n   Revoked access details:")
            for item in revoked:
                print(f"      • {item.user_name} → {item.resource}")
                print(f"        Reason: {item.reviewer_comment}")
        
        return revoked, kept
    
    def check_sod_violations(self):
        """Check for Segregation of Duties violations."""
        print("\n⚖️  Checking SoD violations...")
        
        # Rule: No one should have both Finance and Admin access
        user_resources = {}
        for item in self.access_items:
            if item.certified:
                if item.user_name not in user_resources:
                    user_resources[item.user_name] = set()
                user_resources[item.user_name].add(item.resource)
        
        finance_resources = {"ERP_System", "Financial_Reports", "Budget_Tool"}
        admin_resources = {"User_Admin_Panel", "Network_Config"}
        
        for user, resources in user_resources.items():
            has_finance = bool(resources & finance_resources)
            has_admin = bool(resources & admin_resources)
            
            if has_finance and has_admin:
                self.violations.append({
                    "user": user,
                    "type": "SoD",
                    "details": "Has both Finance and Admin access"
                })
                print(f"   🚨 VIOLATION: {user} has conflicting Finance + Admin access")
    
    def generate_report(self):
        """Generate compliance report."""
        print("\n" + "=" * 60)
        print("📊 ACCESS REVIEW CAMPAIGN REPORT")
        print("=" * 60)
        print(f"Campaign: {self.name}")
        print(f"Period: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        print(f"Total Access Items Reviewed: {len(self.access_items)}")
        
        certified = sum(1 for item in self.access_items if item.certified)
        revoked = len(self.access_items) - certified
        
        print(f"Certified: {certified}")
        print(f"Revoked: {revoked}")
        print(f"SoD Violations Found: {len(self.violations)}")
        
        print("\n📈 Statistics by Manager:")
        managers = set(item.manager for item in self.access_items)
        for manager in managers:
            items = [item for item in self.access_items if item.manager == manager]
            cert_count = sum(1 for item in items if item.certified)
            print(f"   {manager}: {cert_count}/{len(items)} certified")
        
        print("\n⚠️  Action Items:")
        if self.violations:
            for v in self.violations:
                print(f"   • Investigate {v['user']}: {v['details']}")
        else:
            print("   • No immediate action required")
        
        print("=" * 60)


def main():
    print("=" * 60)
    print("📋 ACCESS REVIEW CAMPAIGN SIMULATOR")
    print("=" * 60)
    
    campaign = AccessReviewCampaign("Q1-2024 Access Review")
    
    print("\n🏢 Generating sample access data...")
    campaign.generate_sample_data()
    print(f"   Generated {len(campaign.access_items)} access items")
    
    campaign.simulate_reviews()
    campaign.apply_decisions()
    campaign.check_sod_violations()
    campaign.generate_report()
    
    print("\n💡 KEY CONCEPTS:")
    print("   • Access reviews prevent privilege creep")
    print("   • Managers certify that access is still needed")
    print("   • Unused access should be revoked")
    print("   • SoD violations must be investigated")
    print("   • Audit trail proves compliance to regulators")


if __name__ == "__main__":
    main()
