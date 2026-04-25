#!/usr/bin/env python3
"""
Micro-Segmentation Simulator
============================
Simulates network micro-segmentation:
- Creates isolated network zones
- Enforces zone-to-zone policies
- Simulates lateral movement attacks
- Demonstrates containment benefits

Run: python micro_segment_sim.py
"""

import random
from typing import Dict, List, Set
from dataclasses import dataclass, field


@dataclass
class NetworkZone:
    name: str
    sensitivity: int  # 1-5
    allowed_peers: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    compromised: bool = False
    
    def can_access(self, other_zone: str) -> bool:
        return other_zone in self.allowed_peers


class MicroSegmentedNetwork:
    def __init__(self):
        self.zones: Dict[str, NetworkZone] = {}
        self.traffic_log: List[Dict] = []
    
    def add_zone(self, zone: NetworkZone):
        self.zones[zone.name] = zone
    
    def attempt_traffic(self, source: str, destination: str, protocol: str) -> bool:
        """Attempt to send traffic between zones."""
        if source not in self.zones or destination not in self.zones:
            return False
        
        src = self.zones[source]
        dst = self.zones[destination]
        
        allowed = dst.can_access(source)
        
        self.traffic_log.append({
            "source": source,
            "destination": destination,
            "protocol": protocol,
            "allowed": allowed
        })
        
        if allowed:
            print(f"   ✅ {source} → {destination} ({protocol}): ALLOWED")
            # If source is compromised, destination might get compromised too
            if src.compromised and random.random() < 0.3:
                dst.compromised = True
                print(f"   🚨 LATERAL MOVEMENT: {destination} compromised!")
        else:
            print(f"   ❌ {source} → {destination} ({protocol}): DENIED by policy")
        
        return allowed
    
    def simulate_attack(self, entry_zone: str):
        """Simulate attacker moving laterally from entry point."""
        print(f"\n🚨 ATTACK SIMULATION: Breach in {entry_zone}")
        print("-" * 50)
        
        self.zones[entry_zone].compromised = True
        print(f"   🔴 {entry_zone} has been compromised!")
        
        # Attacker tries to move to all connected zones
        compromised = {entry_zone}
        queue = [entry_zone]
        
        while queue:
            current = queue.pop(0)
            
            for zone_name, zone in self.zones.items():
                if zone_name not in compromised and zone.can_access(current):
                    if random.random() < 0.5:  # 50% chance of successful lateral movement
                        zone.compromised = True
                        compromised.add(zone_name)
                        queue.append(zone_name)
                        print(f"   → Lateral movement to {zone_name}: SUCCESS")
                    else:
                        print(f"   → Lateral movement to {zone_name}: BLOCKED")
        
        return compromised
    
    def visualize(self):
        print("\n🏗️  NETWORK TOPOLOGY")
        print("=" * 60)
        
        for name, zone in self.zones.items():
            status = "🔴 COMPROMISED" if zone.compromised else "🟢 SECURE"
            print(f"\n   [{status}] {name} (sensitivity: {zone.sensitivity})")
            print(f"      Resources: {', '.join(zone.resources)}")
            print(f"      Allowed inbound from: {zone.allowed_peers or 'NONE'}")
    
    def generate_report(self):
        total = len(self.zones)
        compromised = sum(1 for z in self.zones.values() if z.compromised)
        
        print(f"\n📊 SECURITY REPORT")
        print("=" * 60)
        print(f"   Total zones: {total}")
        print(f"   Compromised: {compromised}")
        print(f"   Containment rate: {(total - compromised) / total * 100:.1f}%")
        
        if compromised == 1:
            print("   ✅ Attack contained to entry point!")
        elif compromised <= total * 0.3:
            print("   🟡 Limited lateral movement")
        else:
            print("   🔴 Widespread compromise")


def main():
    print("=" * 60)
    print("🌐 MICRO-SEGMENTATION SIMULATOR")
    print("=" * 60)
    
    network = MicroSegmentedNetwork()
    
    # Create zones with strict policies
    zones = [
        NetworkZone("DMZ", 2, ["Internet"], ["web-server", "dns"]),
        NetworkZone("Web_Tier", 3, ["DMZ", "App_Tier"], ["app-server-1", "app-server-2"]),
        NetworkZone("App_Tier", 4, ["Web_Tier", "DB_Tier"], ["api-gateway", "cache"]),
        NetworkZone("DB_Tier", 5, ["App_Tier"], ["primary-db", "replica-db"]),
        NetworkZone("Management", 5, [], ["jump-host", "monitoring"]),
    ]
    
    for zone in zones:
        network.add_zone(zone)
    
    network.visualize()
    
    # Normal traffic
    print("\n📡 NORMAL TRAFFIC FLOWS")
    print("-" * 60)
    network.attempt_traffic("DMZ", "Web_Tier", "HTTPS")
    network.attempt_traffic("Web_Tier", "App_Tier", "HTTP")
    network.attempt_traffic("App_Tier", "DB_Tier", "SQL")
    network.attempt_traffic("DMZ", "DB_Tier", "SQL")  # Should be denied
    
    # Attack scenario 1: Flat network (no segmentation)
    print("\n" + "=" * 60)
    print("🚨 SCENARIO 1: Flat Network (No Segmentation)")
    print("=" * 60)
    
    flat_network = MicroSegmentedNetwork()
    flat_zones = [
        NetworkZone("Everything", 3, ["Everything"], ["web", "app", "db", "mgmt"]),
    ]
    flat_network.add_zone(flat_zones[0])
    flat_zones[0].compromised = True
    
    print("   One zone contains everything. If breached, all is lost.")
    print("   Compromise rate: 100%")
    
    # Attack scenario 2: Segmented network
    print("\n" + "=" * 60)
    print("🚨 SCENARIO 2: Segmented Network")
    print("=" * 60)
    
    compromised = network.simulate_attack("DMZ")
    network.visualize()
    network.generate_report()
    
    # Attack scenario 3: Segmented with management breach
    print("\n" + "=" * 60)
    print("🚨 SCENARIO 3: Management Zone Breach (Isolated)")
    print("=" * 60)
    
    network2 = MicroSegmentedNetwork()
    for zone in zones:
        network2.add_zone(NetworkZone(
            zone.name, zone.sensitivity, zone.allowed_peers, zone.resources
        ))
    
    compromised2 = network2.simulate_attack("Management")
    network2.visualize()
    network2.generate_report()
    
    print("\n💡 KEY TAKEAWAYS:")
    print("   • Flat networks = attackers move freely")
    print("   • Micro-segmentation contains breaches")
    print("   • East-west traffic must be explicitly allowed")
    print("   • Sensitive zones (DB) should have minimal connections")
    print("   • Even if DMZ is breached, DB stays protected")


if __name__ == "__main__":
    main()
