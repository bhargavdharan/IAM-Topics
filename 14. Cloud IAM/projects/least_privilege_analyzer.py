#!/usr/bin/env python3
"""
Least Privilege Analyzer
========================
Analyzes cloud permissions for least privilege:
- Identifies unused permissions from logs
- Suggests policy refinements
- Detects overly permissive wildcards
- Generates least-privilege recommendations

Run: python least_privilege_analyzer.py
"""

from typing import Dict, List, Set
from dataclasses import dataclass, field


@dataclass
class PermissionUsage:
    action: str
    resource: str
    used_count: int = 0
    last_used: str = ""


@dataclass
class CloudPolicy:
    name: str
    statements: List[Dict] = field(default_factory=list)


class LeastPrivilegeAnalyzer:
    def __init__(self):
        self.policies: List[CloudPolicy] = []
        self.usage_logs: List[Dict] = []
        self.risky_patterns = [
            "*", "*:*", "s3:*", "ec2:*", "iam:*", "AdminAccess"
        ]
    
    def add_policy(self, policy: CloudPolicy):
        self.policies.append(policy)
    
    def add_usage_log(self, user: str, action: str, resource: str, timestamp: str):
        self.usage_logs.append({
            "user": user,
            "action": action,
            "resource": resource,
            "timestamp": timestamp
        })
    
    def analyze_wildcards(self) -> List[Dict]:
        """Find policies with overly permissive wildcards."""
        issues = []
        
        for policy in self.policies:
            for stmt in policy.statements:
                actions = stmt.get("Action", [])
                if isinstance(actions, str):
                    actions = [actions]
                
                for action in actions:
                    if action in ["*", "*:*"]:
                        issues.append({
                            "policy": policy.name,
                            "issue": "CRITICAL: Action allows ALL actions",
                            "recommendation": "Replace with specific required actions",
                            "risk": "CRITICAL"
                        })
                    elif action.endswith(":*"):
                        service = action.split(":")[0]
                        issues.append({
                            "policy": policy.name,
                            "issue": f"HIGH: Action allows ALL {service} actions",
                            "recommendation": f"List specific {service} actions needed",
                            "risk": "HIGH"
                        })
        
        return issues
    
    def analyze_unused_permissions(self) -> List[Dict]:
        """Find granted but unused permissions."""
        issues = []
        
        # Build set of all used actions per user
        used_actions: Dict[str, Set[str]] = {}
        for log in self.usage_logs:
            user = log["user"]
            if user not in used_actions:
                used_actions[user] = set()
            used_actions[user].add(log["action"])
        
        # Compare with granted permissions
        for policy in self.policies:
            for stmt in policy.statements:
                if stmt.get("Effect") != "Allow":
                    continue
                
                actions = stmt.get("Action", [])
                if isinstance(actions, str):
                    actions = [actions]
                
                for action in actions:
                    if "*" in action:
                        continue  # Skip wildcards for this analysis
                    
                    # Check if this action was ever used
                    found_usage = False
                    for user, used in used_actions.items():
                        if action in used:
                            found_usage = True
                            break
                    
                    if not found_usage:
                        issues.append({
                            "policy": policy.name,
                            "issue": f"Action '{action}' granted but never used",
                            "recommendation": "Remove if not needed",
                            "risk": "MEDIUM"
                        })
        
        return issues
    
    def generate_least_privilege_policy(self, user: str) -> Dict:
        """Generate a least-privilege policy based on actual usage."""
        user_actions: Set[str] = set()
        user_resources: Set[str] = set()
        
        for log in self.usage_logs:
            if log["user"] == user:
                user_actions.add(log["action"])
                user_resources.add(log["resource"])
        
        return {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": sorted(user_actions),
                "Resource": sorted(user_resources)
            }]
        }
    
    def full_analysis(self):
        """Run complete analysis."""
        print("=" * 60)
        print("🔍 LEAST PRIVILEGE ANALYZER")
        print("=" * 60)
        
        print("\n🚨 WILDCARD ANALYSIS")
        print("-" * 60)
        wildcard_issues = self.analyze_wildcards()
        if wildcard_issues:
            for issue in wildcard_issues:
                icon = "🔴" if issue["risk"] == "CRITICAL" else "🟠"
                print(f"   {icon} [{issue['risk']}] {issue['policy']}")
                print(f"      Issue: {issue['issue']}")
                print(f"      Fix: {issue['recommendation']}")
        else:
            print("   ✅ No wildcard issues found")
        
        print("\n📊 USAGE ANALYSIS")
        print("-" * 60)
        unused_issues = self.analyze_unused_permissions()
        if unused_issues:
            for issue in unused_issues[:5]:  # Show top 5
                print(f"   🟡 {issue['policy']}")
                print(f"      {issue['issue']}")
            if len(unused_issues) > 5:
                print(f"   ... and {len(unused_issues) - 5} more")
        else:
            print("   ✅ All granted permissions are being used")
        
        print("\n📝 LEAST PRIVILEGE RECOMMENDATIONS")
        print("-" * 60)
        users = set(log["user"] for log in self.usage_logs)
        for user in users:
            policy = self.generate_least_privilege_policy(user)
            print(f"\n   Recommended policy for {user}:")
            print(f"   Actions: {policy['Statement'][0]['Action']}")
            print(f"   Resources: {policy['Statement'][0]['Resource']}")


def main():
    analyzer = LeastPrivilegeAnalyzer()
    
    # Define some policies
    analyzer.add_policy(CloudPolicy("AdminPolicy", [{
        "Effect": "Allow",
        "Action": ["*"],
        "Resource": ["*"]
    }]))
    
    analyzer.add_policy(CloudPolicy("DeveloperPolicy", [{
        "Effect": "Allow",
        "Action": ["s3:*", "ec2:*", "lambda:*", "iam:PassRole"],
        "Resource": ["*"]
    }]))
    
    analyzer.add_policy(CloudPolicy("ReadOnlyPolicy", [{
        "Effect": "Allow",
        "Action": [
            "s3:GetObject", "s3:ListBucket",
            "ec2:DescribeInstances", "ec2:DescribeImages",
            "dynamodb:GetItem", "dynamodb:Query",
            "iam:CreateUser",  # Probably shouldn't be here
            "cloudwatch:*"
        ],
        "Resource": ["*"]
    }]))
    
    # Simulate usage logs (only a subset of granted permissions are used)
    usage_data = [
        ("alice", "s3:GetObject", "arn:aws:s3:::bucket/file.txt", "2024-01-01"),
        ("alice", "s3:ListBucket", "arn:aws:s3:::bucket", "2024-01-01"),
        ("alice", "ec2:DescribeInstances", "*", "2024-01-02"),
        ("bob", "s3:GetObject", "arn:aws:s3:::bucket/file.txt", "2024-01-01"),
        ("bob", "dynamodb:GetItem", "arn:aws:dynamodb:table/users", "2024-01-03"),
    ]
    
    for user, action, resource, ts in usage_data:
        analyzer.add_usage_log(user, action, resource, ts)
    
    analyzer.full_analysis()
    
    print("\n💡 BEST PRACTICES:")
    print("   • Start with zero permissions")
    print("   • Add only what's actually used")
    print("   • Avoid wildcards - list specific actions")
    print("   • Review CloudTrail logs quarterly")
    print("   • Use AWS IAM Access Analyzer or similar tools")


if __name__ == "__main__":
    main()
