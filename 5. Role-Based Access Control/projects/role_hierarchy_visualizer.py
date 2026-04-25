#!/usr/bin/env python3
"""
Role Hierarchy Visualizer
=========================
Visualizes role hierarchies with ASCII art:
- Shows inheritance chains
- Calculates effective permissions
- Detects circular inheritance
- Identifies over-privileged roles

Run: python role_hierarchy_visualizer.py
"""

from typing import Dict, List, Set
from dataclasses import dataclass, field


@dataclass
class Role:
    name: str
    permissions: Set[str] = field(default_factory=set)
    children: List["Role"] = field(default_factory=list)
    parents: List["Role"] = field(default_factory=list)
    
    def get_effective_permissions(self, visited: Set[str] = None) -> Set[str]:
        if visited is None:
            visited = set()
        if self.name in visited:
            return set()
        visited.add(self.name)
        
        perms = self.permissions.copy()
        for parent in self.parents:
            perms.update(parent.get_effective_permissions(visited))
        return perms
    
    def get_level(self) -> int:
        """Get hierarchy level (0 = top)."""
        if not self.parents:
            return 0
        return max(p.get_level() for p in self.parents) + 1


class RoleHierarchy:
    def __init__(self):
        self.roles: Dict[str, Role] = {}
    
    def add_role(self, name: str, permissions: Set[str] = None):
        if name not in self.roles:
            self.roles[name] = Role(name=name, permissions=permissions or set())
    
    def add_inheritance(self, child: str, parent: str):
        if child not in self.roles or parent not in self.roles:
            raise ValueError("Role not found")
        
        # Check for circular inheritance
        if self._would_create_cycle(child, parent):
            raise ValueError(f"Circular inheritance: {child} cannot inherit from {parent}")
        
        self.roles[child].parents.append(self.roles[parent])
        self.roles[parent].children.append(self.roles[child])
    
    def _would_create_cycle(self, child: str, parent: str) -> bool:
        """Check if adding child->parent would create a cycle."""
        visited = {child}
        stack = [parent]
        
        while stack:
            current = stack.pop()
            if current == child:
                return True
            if current in visited:
                continue
            visited.add(current)
            if current in self.roles:
                for p in self.roles[current].parents:
                    stack.append(p.name)
        
        return False
    
    def visualize(self):
        """Display ASCII art hierarchy."""
        print("\n📊 ROLE HIERARCHY")
        print("=" * 60)
        
        # Find root roles
        roots = [r for r in self.roles.values() if not r.parents]
        
        for root in roots:
            self._print_tree(root, "")
        
        print("\n📋 EFFECTIVE PERMISSIONS")
        print("-" * 60)
        for name, role in sorted(self.roles.items()):
            perms = role.get_effective_permissions()
            own = role.permissions
            inherited = perms - own
            print(f"   {name}:")
            print(f"      Own:        {own or '(none)'}")
            print(f"      Inherited:  {inherited or '(none)'}")
            print(f"      Total:      {perms or '(none)'}")
    
    def _print_tree(self, role: Role, prefix: str, is_last: bool = True):
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{role.name}")
        
        children = role.children
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            extension = "    " if is_last else "│   "
            self._print_tree(child, prefix + extension, is_last_child)
    
    def find_overprivileged(self) -> List[Dict]:
        """Find roles with excessive permissions."""
        issues = []
        
        for name, role in self.roles.items():
            perms = role.get_effective_permissions()
            
            # Heuristic: roles with >10 permissions might be overprivileged
            if len(perms) > 10:
                issues.append({
                    "role": name,
                    "permission_count": len(perms),
                    "issue": "Has more than 10 effective permissions"
                })
            
            # Check if role inherits from too many parents
            if len(role.parents) > 3:
                issues.append({
                    "role": name,
                    "parent_count": len(role.parents),
                    "issue": "Inherits from too many parents (complexity)"
                })
        
        return issues
    
    def compare_roles(self, role1: str, role2: str) -> Dict:
        """Compare two roles for similarity."""
        r1 = self.roles.get(role1)
        r2 = self.roles.get(role2)
        
        if not r1 or not r2:
            return {"error": "Role not found"}
        
        p1 = r1.get_effective_permissions()
        p2 = r2.get_effective_permissions()
        
        return {
            "role1": role1,
            "role2": role2,
            "role1_only": p1 - p2,
            "role2_only": p2 - p1,
            "common": p1 & p2,
            "similarity": len(p1 & p2) / len(p1 | p2) if p1 | p2 else 1.0
        }


def main():
    print("=" * 60)
    print("🏗️  ROLE HIERARCHY VISUALIZER")
    print("=" * 60)
    
    hierarchy = RoleHierarchy()
    
    # Create roles
    roles_config = {
        "CEO": {"approve_budget", "hire_executives", "strategic_decisions"},
        "CTO": {"approve_tech", "manage_engineering"},
        "CFO": {"approve_budget", "financial_oversight"},
        "VP_Engineering": {"manage_teams", "tech_strategy"},
        "Senior_Dev": {"write_code", "code_review", "mentor"},
        "Dev": {"write_code", "run_tests"},
        "Junior_Dev": {"write_code"},
        "Finance_Manager": {"review_expenses", "budget_planning"},
        "Accountant": {"process_invoices", "reconcile"},
    }
    
    for name, perms in roles_config.items():
        hierarchy.add_role(name, perms)
    
    # Set up hierarchy
    hierarchy.add_inheritance("CTO", "CEO")
    hierarchy.add_inheritance("CFO", "CEO")
    hierarchy.add_inheritance("VP_Engineering", "CTO")
    hierarchy.add_inheritance("Senior_Dev", "VP_Engineering")
    hierarchy.add_inheritance("Dev", "Senior_Dev")
    hierarchy.add_inheritance("Junior_Dev", "Dev")
    hierarchy.add_inheritance("Finance_Manager", "CFO")
    hierarchy.add_inheritance("Accountant", "Finance_Manager")
    
    # Visualize
    hierarchy.visualize()
    
    # Check for issues
    print("\n🚨 OVER-PRIVILEGE ANALYSIS")
    print("-" * 60)
    issues = hierarchy.find_overprivileged()
    if issues:
        for issue in issues:
            print(f"   ⚠️  {issue['role']}: {issue['issue']}")
    else:
        print("   ✅ No obvious over-privilege issues")
    
    # Compare roles
    print("\n🔄 ROLE COMPARISON")
    print("-" * 60)
    comp = hierarchy.compare_roles("Senior_Dev", "Dev")
    print(f"   Comparing {comp['role1']} vs {comp['role2']}:")
    print(f"   Similarity: {comp['similarity']*100:.1f}%")
    print(f"   Only in {comp['role1']}: {comp['role1_only']}")
    print(f"   Only in {comp['role2']}: {comp['role2_only']}")
    
    # Try circular inheritance
    print("\n🧪 CIRCULAR INHERITANCE TEST")
    print("-" * 60)
    try:
        # This would create a cycle: Dev -> Junior_Dev -> Dev
        hierarchy.add_inheritance("Junior_Dev", "Dev")
        # This should fail
        hierarchy.add_inheritance("Dev", "Junior_Dev")
    except ValueError as e:
        print(f"   ✅ Correctly blocked: {e}")


if __name__ == "__main__":
    main()
