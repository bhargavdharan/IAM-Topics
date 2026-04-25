#!/usr/bin/env python3
"""
IAM Concept Matcher
===================
Interactive quiz that matches real-world scenarios to IAM concepts.
Helps non-technical learners connect analogies to technical terms.

Run: python iam_concept_matcher.py
"""

import random

class ConceptMatcher:
    def __init__(self):
        self.scenarios = [
            {
                "scenario": "A new employee gets a key card on their first day",
                "concept": "Provisioning",
                "explanation": "Creating an identity and granting initial access"
            },
            {
                "scenario": "The security guard checks your ID before letting you in",
                "concept": "Authentication",
                "explanation": "Verifying that you are who you claim to be"
            },
            {
                "scenario": "Your key card only opens the 3rd floor, not the CEO suite",
                "concept": "Authorization",
                "explanation": "Determining what resources you are allowed to access"
            },
            {
                "scenario": "Security cameras record who entered which room and when",
                "concept": "Accounting/Audit",
                "explanation": "Tracking and logging all access events for review"
            },
            {
                "scenario": "An intern's key card is deactivated when they leave",
                "concept": "Deprovisioning",
                "explanation": "Removing access when an identity is no longer needed"
            },
            {
                "scenario": "The cleaning staff can enter offices but not the vault",
                "concept": "Principle of Least Privilege",
                "explanation": "Giving only the minimum access needed for the job"
            },
            {
                "scenario": "Two managers must approve any purchase over $10,000",
                "concept": "Separation of Duties",
                "explanation": "Preventing one person from having complete control over sensitive processes"
            },
            {
                "scenario": "A server needs its own identity to access the database",
                "concept": "Machine Identity",
                "explanation": "Non-human entities like servers and applications also need identities"
            }
        ]
        
        self.concepts = list(set(s["concept"] for s in self.scenarios))
    
    def play(self):
        print("=" * 60)
        print("🎯 IAM CONCEPT MATCHER")
        print("=" * 60)
        print("\nI'll describe a real-world scenario.")
        print("You identify which IAM concept it represents.\n")
        
        score = 0
        total = len(self.scenarios)
        random.shuffle(self.scenarios)
        
        for i, item in enumerate(self.scenarios, 1):
            print(f"\n📋 Scenario {i}/{total}:")
            print(f"   '{item['scenario']}'")
            print("\n   Which concept is this?")
            
            # Show options (correct + 3 random wrong)
            options = [item["concept"]]
            wrong = [c for c in self.concepts if c != item["concept"]]
            options.extend(random.sample(wrong, min(3, len(wrong))))
            random.shuffle(options)
            
            for j, opt in enumerate(options, 1):
                print(f"      {j}. {opt}")
            
            while True:
                try:
                    choice = int(input("\n   Your answer (1-4): ").strip())
                    if 1 <= choice <= len(options):
                        break
                except ValueError:
                    pass
                print("   Please enter a valid number.")
            
            if options[choice - 1] == item["concept"]:
                print(f"   ✅ Correct! {item['concept']}")
                score += 1
            else:
                print(f"   ❌ Wrong! The correct answer is: {item['concept']}")
            
            print(f"   💡 {item['explanation']}")
        
        print("\n" + "=" * 60)
        print(f"🎉 FINAL SCORE: {score}/{total} ({score/total*100:.0f}%)")
        if score == total:
            print("🏆 Perfect! You're an IAM expert!")
        elif score >= total * 0.7:
            print("👍 Great job! You understand the core concepts.")
        else:
            print("📚 Keep learning! Review the README and try again.")
        print("=" * 60)


def main():
    game = ConceptMatcher()
    game.play()


if __name__ == "__main__":
    main()
