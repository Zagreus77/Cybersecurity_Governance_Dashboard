"""
Cybersecurity Governance Project
ISO 27001 & PCI DSS Compliance Management System

This system helps governance teams manage and monitor compliance
with ISO 27001 and PCI DSS standards.
"""

import json
import datetime
import random
import time
import threading
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum

class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    IN_PROGRESS = "in_progress"
    NOT_ASSESSED = "not_assessed"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ControlRequirement:
    control_id: str
    title: str
    description: str
    standard: str  # ISO27001 or PCI_DSS
    status: ComplianceStatus
    risk_level: RiskLevel
    implementation_date: str
    next_review_date: str
    responsible_team: str
    evidence_documents: List[str]
    notes: str = ""
    last_assessment_date: Optional[datetime.datetime] = None
    compliance_drift_factor: float = 0.0  # How quickly this control degrades
    incident_count: int = 0
    automation_level: float = 0.0  # 0.0 = manual, 1.0 = fully automated
    dependency_controls: List[str] = field(default_factory=list)

@dataclass
class ComplianceIncident:
    incident_id: str
    title: str
    description: str
    affected_controls: List[str]
    severity: RiskLevel
    occurrence_time: datetime.datetime
    resolution_time: Optional[datetime.datetime] = None
    impact_duration_hours: int = 24

class GovernanceManager:
    def __init__(self):
        self.iso27001_controls = self._load_iso27001_controls()
        self.pci_dss_controls = self._load_pci_dss_controls()
        self.audit_log = []
        self.incidents = []
        self.alerts = []
        self.monitoring_active = True
        self._setup_logging()
        self._start_monitoring_thread()
    
    def _setup_logging(self):
        """Setup logging for governance activities"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('governance.log'),
                logging.StreamHandler()
            ]
        )
        
    def _load_iso27001_controls(self) -> List[ControlRequirement]:
        """Load ISO 27001 control requirements"""
        controls = [
            ControlRequirement(
                control_id="A.5.1.1",
                title="Information Security Policy",
                description="Information security policy shall be defined and approved by management",
                standard="ISO27001",
                status=ComplianceStatus.COMPLIANT,
                risk_level=RiskLevel.HIGH,
                implementation_date="2024-01-15",
                next_review_date="2025-01-15",
                responsible_team="Security Team",
                evidence_documents=["policy_doc_v2.1.pdf"],
                compliance_drift_factor=0.1,
                automation_level=0.3,
                last_assessment_date=datetime.datetime.now() - datetime.timedelta(days=30)
            ),
            ControlRequirement(
                control_id="A.6.1.1",
                title="Information Security Roles and Responsibilities",
                description="Information security roles and responsibilities shall be defined and allocated",
                standard="ISO27001",
                status=ComplianceStatus.IN_PROGRESS,
                risk_level=RiskLevel.HIGH,
                implementation_date="2024-02-01",
                next_review_date="2025-02-01",
                responsible_team="HR & Security",
                evidence_documents=["roles_matrix_draft.xlsx"],
                compliance_drift_factor=0.15,
                automation_level=0.2,
                last_assessment_date=datetime.datetime.now() - datetime.timedelta(days=15)
            ),
            ControlRequirement(
                control_id="A.8.1.1",
                title="Asset Management Policy",
                description="Assets associated with information and information processing facilities shall be identified",
                standard="ISO27001",
                status=ComplianceStatus.COMPLIANT,
                risk_level=RiskLevel.MEDIUM,
                implementation_date="2024-01-10",
                next_review_date="2024-07-10",
                responsible_team="IT Operations",
                evidence_documents=["asset_inventory.csv", "asset_policy_v1.2.pdf"],
                compliance_drift_factor=0.2,
                automation_level=0.8,
                last_assessment_date=datetime.datetime.now() - datetime.timedelta(days=5)
            )
        ]
        return controls
    
    def _load_pci_dss_controls(self) -> List[ControlRequirement]:
        """Load PCI DSS control requirements"""
        controls = [
            ControlRequirement(
                control_id="PCI.1.1",
                title="Firewall Configuration Standards",
                description="Establish and implement firewall and router configuration standards",
                standard="PCI_DSS",
                status=ComplianceStatus.COMPLIANT,
                risk_level=RiskLevel.CRITICAL,
                implementation_date="2024-01-05",
                next_review_date="2024-04-05",
                responsible_team="Network Security",
                evidence_documents=["firewall_config_v3.2.txt", "penetration_test_report.pdf"],
                compliance_drift_factor=0.3,
                automation_level=0.7,
                last_assessment_date=datetime.datetime.now() - datetime.timedelta(days=20)
            ),
            ControlRequirement(
                control_id="PCI.2.1",
                title="Change Default Passwords",
                description="Change vendor-supplied defaults for system passwords and security parameters",
                standard="PCI_DSS",
                status=ComplianceStatus.NON_COMPLIANT,
                risk_level=RiskLevel.HIGH,
                implementation_date="2024-02-15",
                next_review_date="2024-05-15",
                responsible_team="System Administration",
                evidence_documents=[],
                compliance_drift_factor=0.05,
                automation_level=0.9,
                last_assessment_date=datetime.datetime.now() - datetime.timedelta(days=3),
                incident_count=2
            ),
            ControlRequirement(
                control_id="PCI.3.4",
                title="Cryptographic Key Management",
                description="Protect cryptographic keys against disclosure and misuse",
                standard="PCI_DSS",
                status=ComplianceStatus.IN_PROGRESS,
                risk_level=RiskLevel.CRITICAL,
                implementation_date="2024-03-01",
                next_review_date="2024-06-01",
                responsible_team="Cryptography Team",
                evidence_documents=["key_mgmt_plan.pdf"],
                compliance_drift_factor=0.25,
                automation_level=0.4,
                last_assessment_date=datetime.datetime.now() - datetime.timedelta(days=10)
            )
        ]
        return controls
    
    def update_control_status(self, control_id: str, status: ComplianceStatus, notes: str = ""):
        """Update the compliance status of a control"""
        all_controls = self.iso27001_controls + self.pci_dss_controls
        
        for control in all_controls:
            if control.control_id == control_id:
                old_status = control.status
                control.status = status
                control.notes = notes
                
                # Log the change
                self.audit_log.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "action": "status_update",
                    "control_id": control_id,
                    "old_status": old_status.value,
                    "new_status": status.value,
                    "notes": notes
                })
                
                print(f"Updated {control_id}: {old_status.value} -> {status.value}")
                return True
        
        print(f"Control {control_id} not found")
        return False
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Generate compliance summary report"""
        all_controls = self.iso27001_controls + self.pci_dss_controls
        
        iso_summary = self._get_standard_summary(self.iso27001_controls, "ISO27001")
        pci_summary = self._get_standard_summary(self.pci_dss_controls, "PCI_DSS")
        
        return {
            "report_date": datetime.datetime.now().isoformat(),
            "total_controls": len(all_controls),
            "iso27001": iso_summary,
            "pci_dss": pci_summary,
            "high_risk_non_compliant": self._get_high_risk_issues()
        }
    
    def _get_standard_summary(self, controls: List[ControlRequirement], standard: str) -> Dict[str, Any]:
        """Get summary for a specific standard"""
        total = len(controls)
        compliant = len([c for c in controls if c.status == ComplianceStatus.COMPLIANT])
        non_compliant = len([c for c in controls if c.status == ComplianceStatus.NON_COMPLIANT])
        in_progress = len([c for c in controls if c.status == ComplianceStatus.IN_PROGRESS])
        not_assessed = len([c for c in controls if c.status == ComplianceStatus.NOT_ASSESSED])
        
        compliance_percentage = (compliant / total * 100) if total > 0 else 0
        
        return {
            "standard": standard,
            "total_controls": total,
            "compliant": compliant,
            "non_compliant": non_compliant,
            "in_progress": in_progress,
            "not_assessed": not_assessed,
            "compliance_percentage": round(compliance_percentage, 2)
        }
    
    def _get_high_risk_issues(self) -> List[Dict[str, str]]:
        """Get high-risk non-compliant controls"""
        all_controls = self.iso27001_controls + self.pci_dss_controls
        
        high_risk_issues = []
        for control in all_controls:
            if (control.status == ComplianceStatus.NON_COMPLIANT and 
                control.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]):
                high_risk_issues.append({
                    "control_id": control.control_id,
                    "title": control.title,
                    "risk_level": control.risk_level.value,
                    "responsible_team": control.responsible_team
                })
        
        return high_risk_issues
    
    def _start_monitoring_thread(self):
        """Start background monitoring thread for compliance drift"""
        def monitor():
            while self.monitoring_active:
                try:
                    self._check_compliance_drift()
                    self._simulate_incidents()
                    self._check_overdue_reviews()
                    time.sleep(10)  # Check every 10 seconds for demo
                except Exception as e:
                    logging.error(f"Monitoring error: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        logging.info("Compliance monitoring thread started")
    
    def _check_compliance_drift(self):
        """Simulate compliance drift over time"""
        all_controls = self.iso27001_controls + self.pci_dss_controls
        
        for control in all_controls:
            if control.status == ComplianceStatus.COMPLIANT and control.last_assessment_date:
                days_since_assessment = (datetime.datetime.now() - control.last_assessment_date).days
                
                # Calculate drift probability based on time and drift factor
                drift_probability = control.compliance_drift_factor * (days_since_assessment / 30) * (1 - control.automation_level)
                
                if random.random() < drift_probability * 0.3:  # Higher chance for demo
                    old_status = control.status
                    control.status = ComplianceStatus.IN_PROGRESS
                    self._create_alert(
                        f"Compliance drift detected for {control.control_id}",
                        f"Control {control.control_id} has drifted from compliant status due to time decay",
                        control.risk_level
                    )
                    logging.warning(f"Compliance drift: {control.control_id} {old_status.value} -> {control.status.value}")
    
    def _simulate_incidents(self):
        """Simulate security incidents that affect compliance"""
        if random.random() < 0.15:  # 15% chance per check for demo
            incident_types = [
                ("SEC-001", "Failed Password Audit", ["PCI.2.1"], RiskLevel.HIGH),
                ("SEC-002", "Firewall Misconfiguration", ["PCI.1.1"], RiskLevel.CRITICAL),
                ("SEC-003", "Asset Discovery Gap", ["A.8.1.1"], RiskLevel.MEDIUM),
                ("SEC-004", "Policy Violation", ["A.5.1.1"], RiskLevel.HIGH)
            ]
            
            incident_id, title, affected_controls, severity = random.choice(incident_types)
            incident = ComplianceIncident(
                incident_id=f"{incident_id}-{int(time.time())}",
                title=title,
                description=f"Automated incident simulation: {title}",
                affected_controls=affected_controls,
                severity=severity,
                occurrence_time=datetime.datetime.now()
            )
            
            self.incidents.append(incident)
            self._apply_incident_impact(incident)
            logging.warning(f"Incident simulated: {incident.title}")
    
    def _apply_incident_impact(self, incident: ComplianceIncident):
        """Apply incident impact to affected controls"""
        all_controls = self.iso27001_controls + self.pci_dss_controls
        
        for control in all_controls:
            if control.control_id in incident.affected_controls:
                control.incident_count += 1
                if control.status == ComplianceStatus.COMPLIANT:
                    control.status = ComplianceStatus.NON_COMPLIANT
                    self._create_alert(
                        f"Incident impact: {control.control_id}",
                        f"Control affected by incident: {incident.title}",
                        incident.severity
                    )
    
    def _check_overdue_reviews(self):
        """Check for overdue compliance reviews"""
        all_controls = self.iso27001_controls + self.pci_dss_controls
        
        for control in all_controls:
            if control.next_review_date:
                try:
                    review_date = datetime.datetime.strptime(control.next_review_date, "%Y-%m-%d")
                    if datetime.datetime.now() > review_date:
                        self._create_alert(
                            f"Overdue review: {control.control_id}",
                            f"Control {control.control_id} is past its review date",
                            RiskLevel.MEDIUM
                        )
                except ValueError:
                    pass
    
    def _create_alert(self, title: str, message: str, severity: RiskLevel):
        """Create governance alert"""
        alert = {
            "id": f"ALT-{int(time.time())}-{len(self.alerts)}",
            "title": title,
            "message": message,
            "severity": severity.value,
            "timestamp": datetime.datetime.now().isoformat(),
            "acknowledged": False
        }
        self.alerts.append(alert)
        logging.info(f"Alert created: {title}")
    
    def get_active_alerts(self) -> List[Dict]:
        """Get unacknowledged alerts"""
        return [alert for alert in self.alerts if not alert["acknowledged"]]
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["acknowledged"] = True
                return True
        return False
    
    def force_incident(self, incident_type: str = None) -> ComplianceIncident:
        """Force create an incident for demo purposes"""
        incident_types = [
            ("SEC-001", "Failed Password Audit", ["PCI.2.1"], RiskLevel.HIGH),
            ("SEC-002", "Firewall Misconfiguration", ["PCI.1.1"], RiskLevel.CRITICAL),
            ("SEC-003", "Asset Discovery Gap", ["A.8.1.1"], RiskLevel.MEDIUM),
            ("SEC-004", "Policy Violation", ["A.5.1.1"], RiskLevel.HIGH),
            ("SEC-005", "Unauthorized Access Detected", ["A.6.1.1"], RiskLevel.CRITICAL),
            ("SEC-006", "Encryption Key Exposure", ["PCI.3.4"], RiskLevel.CRITICAL)
        ]
        
        incident_id, title, affected_controls, severity = random.choice(incident_types)
        incident = ComplianceIncident(
            incident_id=f"{incident_id}-{int(time.time())}",
            title=title,
            description=f"Manually triggered incident: {title}",
            affected_controls=affected_controls,
            severity=severity,
            occurrence_time=datetime.datetime.now()
        )
        
        self.incidents.append(incident)
        self._apply_incident_impact(incident)
        logging.warning(f"FORCED incident: {incident.title}")
        return incident
    
    def resolve_incident(self, incident_id: str) -> bool:
        """Resolve an incident and restore affected controls"""
        for incident in self.incidents:
            if incident.incident_id == incident_id and not incident.resolution_time:
                incident.resolution_time = datetime.datetime.now()
                
                # Restore affected controls to compliant status
                all_controls = self.iso27001_controls + self.pci_dss_controls
                for control in all_controls:
                    if control.control_id in incident.affected_controls:
                        if control.status == ComplianceStatus.NON_COMPLIANT:
                            control.status = ComplianceStatus.COMPLIANT
                            control.last_assessment_date = datetime.datetime.now()
                            self._create_alert(
                                f"Control restored: {control.control_id}",
                                f"Control {control.control_id} restored to compliance after incident resolution",
                                RiskLevel.LOW
                            )
                
                logging.info(f"RESOLVED incident: {incident.title}")
                return True
        return False
    
    def implement_solution(self, control_id: str, solution_type: str) -> bool:
        """Implement a solution for a non-compliant control"""
        all_controls = self.iso27001_controls + self.pci_dss_controls
        
        solutions = {
            "automation": "Automated monitoring and enforcement implemented",
            "training": "Staff training and awareness program completed",
            "policy_update": "Updated policies and procedures implemented",
            "technology": "New security technology deployed",
            "process": "Improved security processes implemented"
        }
        
        for control in all_controls:
            if control.control_id == control_id:
                if control.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.IN_PROGRESS]:
                    control.status = ComplianceStatus.COMPLIANT
                    control.last_assessment_date = datetime.datetime.now()
                    
                    # Improve control based on solution type
                    if solution_type == "automation":
                        control.automation_level = min(1.0, control.automation_level + 0.3)
                        control.compliance_drift_factor *= 0.7  # Reduce drift
                    elif solution_type == "training":
                        control.compliance_drift_factor *= 0.8
                    elif solution_type == "technology":
                        control.automation_level = min(1.0, control.automation_level + 0.4)
                        control.compliance_drift_factor *= 0.6
                    
                    solution_desc = solutions.get(solution_type, "Generic solution implemented")
                    control.notes = f"Solution: {solution_desc}"
                    
                    self.audit_log.append({
                        "timestamp": datetime.datetime.now().isoformat(),
                        "action": "solution_implemented",
                        "control_id": control_id,
                        "solution_type": solution_type,
                        "description": solution_desc
                    })
                    
                    self._create_alert(
                        f"Solution implemented: {control.control_id}",
                        f"Control {control.control_id} restored via {solution_type}: {solution_desc}",
                        RiskLevel.LOW
                    )
                    
                    logging.info(f"SOLUTION implemented for {control_id}: {solution_type}")
                    return True
        return False
    
    def export_report(self, filename: str = None):
        """Export compliance report to JSON"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"compliance_report_{timestamp}.json"
        
        summary = self.get_compliance_summary()
        summary["active_alerts"] = self.get_active_alerts()
        summary["recent_incidents"] = [
            {
                "incident_id": inc.incident_id,
                "title": inc.title,
                "severity": inc.severity.value,
                "occurrence_time": inc.occurrence_time.isoformat(),
                "affected_controls": inc.affected_controls
            }
            for inc in self.incidents[-10:]  # Last 10 incidents
        ]
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Report exported to {filename}")

def main():
    """Main function to demonstrate the governance system"""
    print("Cybersecurity Governance & Compliance Management System")
    print("=" * 60)
    
    # Initialize the governance manager
    gov_manager = GovernanceManager()
    
    # Display initial summary
    print("\nInitial Compliance Status:")
    summary = gov_manager.get_compliance_summary()
    
    print(f"\nISO 27001 Status:")
    iso_data = summary['iso27001']
    print(f"  Total Controls: {iso_data['total_controls']}")
    print(f"  Compliance: {iso_data['compliance_percentage']}%")
    
    print(f"\nPCI DSS Status:")
    pci_data = summary['pci_dss']
    print(f"  Total Controls: {pci_data['total_controls']}")
    print(f"  Compliance: {pci_data['compliance_percentage']}%")
    
    # Example updates
    print("\nUpdating some control statuses...")
    gov_manager.update_control_status("A.5.1.1", ComplianceStatus.COMPLIANT, "Policy approved and implemented")
    gov_manager.update_control_status("PCI.1.1", ComplianceStatus.IN_PROGRESS, "Firewall rules being reviewed")
    
    # Export report
    print("\nGenerating compliance report...")
    gov_manager.export_report()
    
    print("\nGovernance system initialized successfully!")

if __name__ == "__main__":
    main()
