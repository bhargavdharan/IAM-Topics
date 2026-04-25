#!/usr/bin/env python3
"""
LDAP Simulator
==============
Simulates LDAP directory operations:
- Directory tree with users, groups, and OUs
- Bind authentication
- Search with filters
- Add, modify, delete operations

Run: python ldap_simulator.py
"""

import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class LDAPEntry:
    dn: str  # Distinguished Name
    attributes: Dict[str, List[str]] = field(default_factory=dict)
    
    def get(self, attr: str) -> List[str]:
        return self.attributes.get(attr, [])
    
    def add(self, attr: str, value: str):
        if attr not in self.attributes:
            self.attributes[attr] = []
        self.attributes[attr].append(value)
    
    def modify(self, attr: str, values: List[str]):
        self.attributes[attr] = values


class LDAPServer:
    """Simulates an LDAP directory server."""
    
    def __init__(self, base_dn: str = "dc=example,dc=com"):
        self.base_dn = base_dn
        self.entries: Dict[str, LDAPEntry] = {}
        self._init_directory()
    
    def _init_directory(self):
        """Initialize a sample directory structure."""
        # Root
        self.add_entry("dc=example,dc=com", {
            "objectClass": ["domain"],
            "dc": ["example"]
        })
        
        # Organizational Units
        for ou in ["Users", "Groups", "Computers"]:
            self.add_entry(f"ou={ou},dc=example,dc=com", {
                "objectClass": ["organizationalUnit"],
                "ou": [ou]
            })
        
        # Users
        users = [
            ("uid=alice", "Alice Smith", "Engineering", "Developer", "alice@example.com"),
            ("uid=bob", "Bob Jones", "Finance", "Manager", "bob@example.com"),
            ("uid=charlie", "Charlie Brown", "Engineering", "Intern", "charlie@example.com"),
        ]
        
        for uid, name, dept, title, email in users:
            self.add_entry(f"{uid},ou=Users,dc=example,dc=com", {
                "objectClass": ["inetOrgPerson", "organizationalPerson", "person"],
                "uid": [uid.split("=")[1]],
                "cn": [name],
                "sn": [name.split()[-1]],
                "ou": [dept],
                "title": [title],
                "mail": [email],
                "userPassword": [self._hash_password("password123")]
            })
        
        # Groups
        self.add_entry("cn=Engineering,ou=Groups,dc=example,dc=com", {
            "objectClass": ["groupOfNames"],
            "cn": ["Engineering"],
            "member": ["uid=alice,ou=Users,dc=example,dc=com",
                      "uid=charlie,ou=Users,dc=example,dc=com"]
        })
        
        self.add_entry("cn=Finance,ou=Groups,dc=example,dc=com", {
            "objectClass": ["groupOfNames"],
            "cn": ["Finance"],
            "member": ["uid=bob,ou=Users,dc=example,dc=com"]
        })
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def add_entry(self, dn: str, attributes: Dict[str, List[str]]):
        self.entries[dn] = LDAPEntry(dn=dn, attributes=attributes)
    
    def bind(self, dn: str, password: str) -> bool:
        """Authenticate a user (simplified bind)."""
        if dn not in self.entries:
            print(f"   ❌ Bind failed: {dn} not found")
            return False
        
        entry = self.entries[dn]
        stored_hash = entry.get("userPassword")[0] if entry.get("userPassword") else ""
        provided_hash = self._hash_password(password)
        
        if stored_hash == provided_hash:
            print(f"   ✅ Bind successful: {dn}")
            return True
        else:
            print(f"   ❌ Bind failed: invalid credentials for {dn}")
            return False
    
    def search(self, base_dn: str, filter_str: str = "(objectClass=*)", 
               scope: str = "subtree") -> List[LDAPEntry]:
        """Search directory with filter."""
        results = []
        
        for dn, entry in self.entries.items():
            # Check base DN
            if not dn.endswith(base_dn) and dn != base_dn:
                continue
            
            # Simple filter parsing (very basic)
            if filter_str == "(objectClass=*)":
                results.append(entry)
            elif "uid=" in filter_str:
                uid = filter_str.split("uid=")[1].split(")")[0]
                if f"uid={uid}" in dn:
                    results.append(entry)
            elif "ou=" in filter_str:
                ou = filter_str.split("ou=")[1].split(")")[0]
                if f"ou={ou}" in dn:
                    results.append(entry)
            elif "cn=" in filter_str:
                cn = filter_str.split("cn=")[1].split(")")[0]
                if entry.get("cn") and cn in entry.get("cn"):
                    results.append(entry)
        
        return results
    
    def modify(self, dn: str, attr: str, values: List[str]):
        if dn in self.entries:
            self.entries[dn].modify(attr, values)
            print(f"   ✅ Modified {dn}: {attr} = {values}")
        else:
            print(f"   ❌ Entry not found: {dn}")
    
    def delete(self, dn: str):
        if dn in self.entries:
            del self.entries[dn]
            print(f"   ✅ Deleted: {dn}")
        else:
            print(f"   ❌ Entry not found: {dn}")
    
    def display_tree(self, base: str = "", indent: int = 0):
        """Display directory tree."""
        if not base:
            base = self.base_dn
        
        for dn in sorted(self.entries.keys()):
            if dn.endswith(base) and dn != base:
                relative = dn.replace("," + base, "")
                print("  " * indent + f"📁 {relative}")


def main():
    print("=" * 60)
    print("📖 LDAP SIMULATOR")
    print("=" * 60)
    
    server = LDAPServer()
    
    # Display directory structure
    print("\n🏗️  Directory Structure:")
    print(f"   Base DN: {server.base_dn}")
    print("   ou=Users")
    for entry in server.search("ou=Users,dc=example,dc=com"):
        if "uid=" in entry.dn:
            uid = entry.get("uid")[0]
            cn = entry.get("cn")[0]
            title = entry.get("title")[0]
            print(f"      👤 {uid} - {cn} ({title})")
    
    print("   ou=Groups")
    for entry in server.search("ou=Groups,dc=example,dc=com"):
        if "cn=" in entry.dn:
            cn = entry.get("cn")[0]
            members = entry.get("member")
            print(f"      👥 {cn} ({len(members)} members)")
    
    # Bind operations
    print("\n🔐 Authentication Tests:")
    server.bind("uid=alice,ou=Users,dc=example,dc=com", "password123")
    server.bind("uid=bob,ou=Users,dc=example,dc=com", "wrongpassword")
    server.bind("uid=unknown,ou=Users,dc=example,dc=com", "password123")
    
    # Search operations
    print("\n🔍 Search Tests:")
    
    print("\n   Search: All Engineering users")
    results = server.search("ou=Users,dc=example,dc=com", "(ou=Engineering)")
    for r in results:
        print(f"      Found: {r.get('cn')[0]} - {r.get('mail')[0]}")
    
    print("\n   Search: User 'alice'")
    results = server.search("ou=Users,dc=example,dc=com", "(uid=alice)")
    for r in results:
        print(f"      Found: {r.dn}")
        for attr, values in r.attributes.items():
            print(f"         {attr}: {values}")
    
    # Modify operation
    print("\n✏️  Modify Test:")
    server.modify("uid=alice,ou=Users,dc=example,dc=com", "title", ["Senior Developer"])
    
    # Verify modification
    results = server.search("ou=Users,dc=example,dc=com", "(uid=alice)")
    print(f"   Alice's new title: {results[0].get('title')}")
    
    # Group membership
    print("\n👥 Group Membership Test:")
    eng_group = server.search("ou=Groups,dc=example,dc=com", "(cn=Engineering)")[0]
    print(f"   Engineering group members:")
    for member in eng_group.get("member"):
        print(f"      {member}")
    
    print("\n💡 KEY CONCEPTS:")
    print("   • DN (Distinguished Name): Unique identifier in the tree")
    print("   • OU (Organizational Unit): Container for grouping")
    print("   • Bind: Authentication operation")
    print("   • Search: Query with filters")
    print("   • LDAP is optimized for reads, not writes")


if __name__ == "__main__":
    main()
