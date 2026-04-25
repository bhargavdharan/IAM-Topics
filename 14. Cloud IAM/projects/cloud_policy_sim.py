#!/usr/bin/env python3
"""
Cloud IAM Policy Simulator
==========================
Simulates cloud IAM policy evaluation:
- Parses AWS-style IAM policies
- Evaluates access requests
- Handles explicit deny, allow, and implicit deny
- Supports conditions

Run: python cloud_policy_sim.py
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class AccessRequest:
    user: str
    action: str
    resource: str
    conditions: Dict[str, Any]


class CloudPolicy:
    """Represents an IAM policy statement."""
    
    def __init__(self, sid: str, effect: str, actions: List[str],
                 resources: List[str], conditions: Dict = None):
        self.sid = sid
        self.effect = effect  # "Allow" or "Deny"
        self.actions = actions
        self.resources = resources
        self.conditions = conditions or {}
    
    def matches(self, request: AccessRequest) -> bool:
        """Check if policy applies to request."""
        # Check action match (supports wildcards)
        action_match = any(
            self._match_pattern(request.action, pattern)
            for pattern in self.actions
        )
        if not action_match:
            return False
        
        # Check resource match
        resource_match = any(
            self._match_pattern(request.resource, pattern)
            for pattern in self.resources
        )
        if not resource_match:
            return False
        
        # Check conditions
        return self._check_conditions(request)
    
    def _match_pattern(self, value: str, pattern: str) -> bool:
        """Simple wildcard matching."""
        if pattern == "*":
            return True
        if pattern.endswith("*"):
            return value.startswith(pattern[:-1])
        if pattern.startswith("*"):
            return value.endswith(pattern[1:])
        return value == pattern
    
    def _check_conditions(self, request: AccessRequest) -> bool:
        """Evaluate policy conditions."""
        for condition_type, condition_values in self.conditions.items():
            if condition_type == "StringEquals":
                for key, expected in condition_values.items():
                    actual = request.conditions.get(key)
                    if actual != expected:
                        return False
            elif condition_type == "IpAddress":
                # Simplified IP check
                allowed_ips = condition_values.get("SourceIp", [])
                source_ip = request.conditions.get("SourceIp")
                if source_ip not in allowed_ips:
                    return False
            elif condition_type == "Bool":
                for key, expected in condition_values.items():
                    actual = request.conditions.get(key, False)
                    if bool(actual) != bool(expected):
                        return False
        return True


class CloudIAMSimulator:
    """Simulates cloud IAM policy evaluation."""
    
    def __init__(self):
        self.policies: List[CloudPolicy] = []
    
    def add_policy(self, policy: CloudPolicy):
        self.policies.append(policy)
    
    def evaluate(self, request: AccessRequest) -> Dict:
        """Evaluate request against all policies."""
        matching_allow = []
        matching_deny = []
        
        for policy in self.policies:
            if policy.matches(request):
                if policy.effect == "Deny":
                    matching_deny.append(policy)
                else:
                    matching_allow.append(policy)
        
        # Decision logic
        if matching_deny:
            decision = "DENY"
            reason = f"Explicit deny by: {[p.sid for p in matching_deny]}"
        elif matching_allow:
            decision = "ALLOW"
            reason = f"Explicit allow by: {[p.sid for p in matching_allow]}"
        else:
            decision = "DENY"
            reason = "Implicit deny (no matching allow policy)"
        
        return {
            "decision": decision,
            "reason": reason,
            "request": {
                "user": request.user,
                "action": request.action,
                "resource": request.resource
            },
            "matching_policies": {
                "allow": [p.sid for p in matching_allow],
                "deny": [p.sid for p in matching_deny]
            }
        }


def main():
    print("=" * 60)
    print("☁️  CLOUD IAM POLICY SIMULATOR")
    print("=" * 60)
    
    simulator = CloudIAMSimulator()
    
    # Define policies
    print("\n📜 Defining IAM policies...")
    
    # Policy 1: Allow developers to read from dev bucket
    simulator.add_policy(CloudPolicy(
        sid="DevReadAccess",
        effect="Allow",
        actions=["s3:GetObject", "s3:ListBucket"],
        resources=["arn:aws:s3:::dev-bucket/*", "arn:aws:s3:::dev-bucket"],
        conditions={"StringEquals": {"Department": "Engineering"}}
    ))
    
    # Policy 2: Allow admins full access to prod
    simulator.add_policy(CloudPolicy(
        sid="AdminProdAccess",
        effect="Allow",
        actions=["s3:*"],
        resources=["arn:aws:s3:::prod-bucket/*"]
    ))
    
    # Policy 3: Deny all access from public IPs
    simulator.add_policy(CloudPolicy(
        sid="DenyPublicIP",
        effect="Deny",
        actions=["*"],
        resources=["*"],
        conditions={"IpAddress": {"SourceIp": ["0.0.0.0/0"]}}
    ))
    
    # Policy 4: Deny delete on prod
    simulator.add_policy(CloudPolicy(
        sid="DenyProdDelete",
        effect="Deny",
        actions=["s3:DeleteObject"],
        resources=["arn:aws:s3:::prod-bucket/*"]
    ))
    
    print("   ✅ 4 policies loaded")
    
    # Test scenarios
    scenarios = [
        {
            "name": "Developer reading dev bucket",
            "request": AccessRequest(
                user="alice",
                action="s3:GetObject",
                resource="arn:aws:s3:::dev-bucket/app.js",
                conditions={"Department": "Engineering", "SourceIp": "10.0.0.5"}
            )
        },
        {
            "name": "Developer trying to delete prod",
            "request": AccessRequest(
                user="alice",
                action="s3:DeleteObject",
                resource="arn:aws:s3:::prod-bucket/data.csv",
                conditions={"Department": "Engineering", "SourceIp": "10.0.0.5"}
            )
        },
        {
            "name": "Admin deleting prod (explicit deny)",
            "request": AccessRequest(
                user="eve",
                action="s3:DeleteObject",
                resource="arn:aws:s3:::prod-bucket/data.csv",
                conditions={"Role": "Admin", "SourceIp": "10.0.0.10"}
            )
        },
        {
            "name": "Unknown user accessing anything",
            "request": AccessRequest(
                user="hacker",
                action="s3:GetObject",
                resource="arn:aws:s3:::dev-bucket/secret.txt",
                conditions={"SourceIp": "10.0.0.99"}
            )
        },
        {
            "name": "Access from public IP (denied)",
            "request": AccessRequest(
                user="alice",
                action="s3:GetObject",
                resource="arn:aws:s3:::dev-bucket/app.js",
                conditions={"Department": "Engineering", "SourceIp": "0.0.0.0/0"}
            )
        }
    ]
    
    print("\n🧪 Evaluating scenarios...")
    for scenario in scenarios:
        print(f"\n📋 {scenario['name']}")
        print(f"   {scenario['request'].action} on {scenario['request'].resource}")
        
        result = simulator.evaluate(scenario['request'])
        
        icon = "✅" if result['decision'] == "ALLOW" else "❌"
        print(f"   {icon} {result['decision']}")
        print(f"   Reason: {result['reason']}")
    
    print("\n" + "=" * 60)
    print("💡 CLOUD IAM PRINCIPLES")
    print("=" * 60)
    print("• Default deny: No access without explicit allow")
    print("• Explicit deny overrides explicit allow")
    print("• Conditions make policies dynamic and context-aware")
    print("• Least privilege: Grant minimum necessary access")
    print("• Use resource-level permissions for fine-grained control")


if __name__ == "__main__":
    main()
