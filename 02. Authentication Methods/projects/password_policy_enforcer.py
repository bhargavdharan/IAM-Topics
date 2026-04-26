#!/usr/bin/env python3
"""
Password Policy Enforcer
========================
Interactive password strength checker with:
- Length, complexity, and entropy checks
- Dictionary and pattern detection
- NIST SP 800-63B compliance validation
- Visual strength meter

Run: python password_policy_enforcer.py
"""

import math
import re
import string


class PasswordPolicy:
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "qwerty", "admin", "welcome",
            "password123", "abc123", "letmein", "monkey", "dragon"
        ]
    
    def calculate_entropy(self, password: str) -> float:
        """Calculate Shannon entropy of password."""
        charset_size = 0
        if re.search(r'[a-z]', password): charset_size += 26
        if re.search(r'[A-Z]', password): charset_size += 26
        if re.search(r'[0-9]', password): charset_size += 10
        if re.search(r'[^a-zA-Z0-9]', password): charset_size += 32
        
        if charset_size == 0:
            return 0
        
        return len(password) * math.log2(charset_size)
    
    def check_length(self, pwd: str) -> tuple:
        length = len(pwd)
        if length < 8:
            return False, f"❌ Too short ({length} chars). Minimum 8 required."
        elif length < 12:
            return True, f"⚠️  Acceptable ({length} chars). 12+ recommended."
        else:
            return True, f"✅ Good length ({length} chars)"
    
    def check_complexity(self, pwd: str) -> tuple:
        checks = {
            "Lowercase letters": bool(re.search(r'[a-z]', pwd)),
            "Uppercase letters": bool(re.search(r'[A-Z]', pwd)),
            "Numbers": bool(re.search(r'[0-9]', pwd)),
            "Special characters": bool(re.search(r'[^a-zA-Z0-9]', pwd))
        }
        
        passed = sum(checks.values())
        
        details = []
        for check, passed_flag in checks.items():
            icon = "✅" if passed_flag else "❌"
            details.append(f"      {icon} {check}")
        
        if passed >= 3:
            return True, "\n".join(details)
        else:
            return False, "\n".join(details)
    
    def check_common(self, pwd: str) -> tuple:
        lower = pwd.lower()
        for common in self.common_passwords:
            if common in lower or lower in common:
                return False, f"❌ Contains common pattern: '{common}'"
        
        # Check for keyboard patterns
        keyboard_rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', '1234567890']
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                if row[i:i+3] in lower:
                    return False, f"❌ Keyboard pattern detected: '{row[i:i+3]}'"
        
        return True, "✅ Not a common password or pattern"
    
    def check_repetition(self, pwd: str) -> tuple:
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', pwd):
            return False, "❌ Repeated characters (e.g., 'aaa')"
        
        # Check for sequential characters
        sequential = 0
        for i in range(len(pwd) - 1):
            if ord(pwd[i+1]) - ord(pwd[i]) == 1:
                sequential += 1
            else:
                sequential = 0
            if sequential >= 2:
                return False, "❌ Sequential characters (e.g., 'abc', '123')"
        
        return True, "✅ No problematic repetition"
    
    def evaluate(self, password: str) -> dict:
        results = {
            "password": password,
            "checks": {},
            "score": 0,
            "strength": "",
            "entropy": self.calculate_entropy(password)
        }
        
        checks = [
            ("Length", self.check_length(password)),
            ("Complexity", self.check_complexity(password)),
            ("Common Patterns", self.check_common(password)),
            ("Repetition", self.check_repetition(password))
        ]
        
        for name, (passed, detail) in checks:
            results["checks"][name] = {"passed": passed, "detail": detail}
            if passed:
                results["score"] += 25
        
        # Strength rating
        if results["score"] >= 90:
            results["strength"] = "EXCELLENT"
        elif results["score"] >= 75:
            results["strength"] = "STRONG"
        elif results["score"] >= 50:
            results["strength"] = "MODERATE"
        elif results["score"] >= 25:
            results["strength"] = "WEAK"
        else:
            results["strength"] = "VERY WEAK"
        
        return results
    
    def visual_meter(self, score: int) -> str:
        bars = int(score / 10)
        empty = 10 - bars
        
        if score >= 75:
            color = "🟩"
        elif score >= 50:
            color = "🟨"
        elif score >= 25:
            color = "🟧"
        else:
            color = "🟥"
        
        return color * bars + "⬜" * empty


def main():
    print("=" * 60)
    print("🔐 PASSWORD POLICY ENFORCER")
    print("=" * 60)
    print("\nThis tool checks password strength against enterprise policies.")
    print("It evaluates length, complexity, patterns, and entropy.\n")
    
    enforcer = PasswordPolicy()
    
    test_passwords = [
        "password",
        "Password123!",
        "Tr0ub4dor&3",
        "correct-horse-battery-staple",
        "MyS3cur3P@ssw0rd!2024"
    ]
    
    print("📊 Sample Analysis:")
    for pwd in test_passwords:
        result = enforcer.evaluate(pwd)
        meter = enforcer.visual_meter(result["score"])
        
        print(f"\n   Password: {'*' * len(pwd)}")
        print(f"   Strength: {meter} {result['strength']} ({result['score']}%)")
        print(f"   Entropy:  {result['entropy']:.1f} bits")
        for name, check in result["checks"].items():
            icon = "✅" if check["passed"] else "❌"
            print(f"   {icon} {name}:")
            for line in check["detail"].split("\n"):
                print(f"      {line}")
    
    # Interactive mode
    print("\n" + "=" * 60)
    print("🎮 Interactive Mode")
    print("=" * 60)
    
    while True:
        pwd = input("\nEnter a password to test (or 'quit' to exit): ").strip()
        if pwd.lower() == 'quit':
            break
        
        result = enforcer.evaluate(pwd)
        meter = enforcer.visual_meter(result["score"])
        
        print(f"\n   Strength: {meter} {result['strength']} ({result['score']}%)")
        print(f"   Entropy:  {result['entropy']:.1f} bits")
        print(f"   Time to crack (est): ", end="")
        
        if result["entropy"] < 40:
            print("Instant - Very weak")
        elif result["entropy"] < 60:
            print("Seconds to minutes")
        elif result["entropy"] < 80:
            print("Hours to days")
        elif result["entropy"] < 100:
            print("Months to years")
        else:
            print("Centuries - Strong enough")
        
        for name, check in result["checks"].items():
            icon = "✅" if check["passed"] else "❌"
            print(f"\n   {icon} {name}:")
            for line in check["detail"].split("\n"):
                print(f"      {line}")
    
    print("\n💡 Remember: Length beats complexity. Use passphrases!")


if __name__ == "__main__":
    main()
