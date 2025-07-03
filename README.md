# Cybersecurity Governance & Compliance Management System

**Dynamic compliance management system for ISO 27001 & PCI DSS standards with real-time monitoring, incident simulation, and automated remediation workflows.**

## 🎯 Dynamic Features

### 🔄 Real-Time Monitoring 
- **Live Compliance Drift Detection** - Controls automatically degrade over time based on automation levels
- **10-Second Monitoring Cycles** - Continuous background monitoring for immediate updates
- **Dynamic Risk Scoring** - Risk scores change based on incidents, automation, and control status
- **Time-Based Assessments** - Compliance status evolves based on days since last review

### 🚨 Incident Simulation & Impact 
- **Automated Security Incidents** - Random incidents affect specific controls in real-time
- **Incident Types**: Failed audits, firewall misconfigurations, asset gaps, policy violations
- **Immediate Impact** - Incidents instantly change compliance status from compliant to non-compliant
- **Incident Resolution Tracking** - Mark incidents as resolved to restore compliance

### 🔧 Solution Management Center 
- **Interactive Remediation** - Implement solutions directly from the dashboard
- **Solution Types**: Automation, Training, Policy Updates, Technology, Process Improvements
- **Automated Impact** - Solutions improve automation levels and reduce compliance drift
- **Progress Tracking** - Monitor solution effectiveness over time

### 📊 Live Governance Dashboard
- **Real-time Compliance Metrics** - Percentages that change as incidents occur
- **Active Alerts System** - Unacknowledged alerts for overdue reviews and incidents
- **Recent Incidents Feed** - Live feed of security incidents affecting compliance
- **Trend Analysis** - Track automation coverage, drift risk, and total risk scores

### ⚡ Demo & Testing Features
- **Force Incident Button** - Create immediate incidents for demonstration
- **Manual Simulation Triggers** - Test compliance changes instantly
- **Solution Implementation** - Immediate feedback on remediation efforts

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd Governance_Compliance_Project
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the main application:**
   ```bash
   python main.py
   ```

4. **Start the web dashboard:**
   ```bash
   python dashboard.py
   ```

5. **Access the dashboard:**
   Open your browser and go to: `http://localhost:5000`

## 🎮 How to Experience the Dynamic Features

### Try the Live Demo Flow:
1. **Open Dashboard** - Visit `http://localhost:5000`
2. **Click "⚡ Force Incident"** - Creates immediate security incident
3. **Click "🔄 Refresh Data"** - See compliance percentages drop
4. **Click "🔧 Solutions & Remediation"** - Open solution center
5. **Click "📋 Show Issues Needing Solutions"** - View non-compliant controls
6. **Select solution type & Click "✅ Implement Solution"** - Fix the issues
7. **Click "🔄 Refresh Data"** - Watch compliance improve in real-time!

### Automatic Changes (Every 10 Seconds):
- Random security incidents occur
- Compliance drift happens naturally
- New alerts are generated
- Risk scores update dynamically

## 📊 System Components

### 1. Core Management System (`main.py`)
- **GovernanceManager**: Central class with dynamic monitoring capabilities
- **ControlRequirement**: Enhanced data structure with automation and drift factors
- **Real-time Monitoring Thread**: Background compliance monitoring every 10 seconds
- **Incident Simulation Engine**: Automated incident generation and impact assessment
- **Solution Implementation**: Multiple remediation pathways with measurable impact

### 2. Web Dashboard (`dashboard.py`)
- **Flask Web Application**: Interactive web interface with dynamic updates
- **Enhanced REST API**: 15+ endpoints including incident management and solutions
- **Real-time Data Feeds**: Live compliance monitoring with immediate updates
- **Solution Management API**: Incident resolution and remediation endpoints

### 3. Dashboard Interface (`templates/dashboard.html`)
- **Dynamic Dashboard**: Real-time updates with live charts and metrics
- **Solution Management Panel**: Interactive remediation center
- **Incident Tracking**: Live incident feed with resolution capabilities
- **Alert System**: Active alerts with acknowledgment features
- **Demo Controls**: Force incident and manual triggers for testing

## 🔧 Usage Examples

### Basic Usage
```python
from main import GovernanceManager, ComplianceStatus

# Initialize the governance manager
gov_manager = GovernanceManager()

# Update a control status
gov_manager.update_control_status(
    "A.5.1.1", 
    ComplianceStatus.COMPLIANT, 
    "Policy approved and implemented"
)

# Generate compliance report
summary = gov_manager.get_compliance_summary()
print(f"ISO 27001 Compliance: {summary['iso27001']['compliance_percentage']}%")
print(f"PCI DSS Compliance: {summary['pci_dss']['compliance_percentage']}%")

# Export detailed report
gov_manager.export_report("compliance_report.json")
```

### Dynamic API Usage 
```bash
# Get real-time compliance summary
curl http://localhost:5000/api/compliance-summary

# Get active alerts
curl http://localhost:5000/api/alerts

# Get live trends and risk scores
curl http://localhost:5000/api/compliance-trends

# Force incident for demo (creates immediate impact)
curl -X POST http://localhost:5000/api/force-incident

# Get recent incidents
curl http://localhost:5000/api/incidents

# Implement solution for non-compliant control
curl -X POST http://localhost:5000/api/implement-solution \
  -H "Content-Type: application/json" \
  -d '{"control_id": "PCI.2.1", "solution_type": "automation"}'

# Resolve incident
curl -X POST http://localhost:5000/api/resolve-incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "SEC-001-1234567890"}'
```

## 📋 Control Standards Included

### ISO 27001 Controls
- **A.5.1.1** - Information Security Policy
- **A.6.1.1** - Information Security Roles and Responsibilities  
- **A.8.1.1** - Asset Management Policy
- *Easily extensible for additional controls*

### PCI DSS Controls
- **PCI.1.1** - Firewall Configuration Standards
- **PCI.2.1** - Change Default Passwords
- **PCI.3.4** - Cryptographic Key Management
- *Easily extensible for additional requirements*

## 🎨 Dynamic Dashboard Features

The interactive dashboard provides:
- **Live Compliance Metrics**: Percentages that change as incidents occur
- **Active Alerts Panel**: Real-time governance alerts and notifications  
- **Live Trends Widget**: Risk scores, automation levels, and drift metrics
- **Recent Incidents Feed**: Security incidents with severity and impact details
- **Solution Management Center**: Interactive remediation with multiple solution types
- **Force Incident Demo**: Create immediate compliance impacts for testing
- **Risk Assessment Charts**: Dynamic visualizations of control risk distribution

## 📈 Compliance Reporting

### Dynamic Reports Include:
- **Real-time Compliance Percentages** that reflect current incidents and solutions
- **Active Alert Summary** with unacknowledged governance notifications
- **Recent Incident Impact Analysis** showing affected controls and timelines
- **Live Risk Scoring** based on automation levels, incidents, and drift factors
- **Solution Implementation Tracking** with measurable compliance improvements
- **Trend Analysis** of compliance drift and remediation effectiveness

### Export Formats:
- **Enhanced JSON reports** with incidents, alerts, and trend data
- **Live web dashboard** with real-time updates every 10 seconds
- **API endpoints** for integration with enterprise governance tools

## 🔐 Enhanced Security Features

- **Real-time Audit Logging**: All incidents, solutions, and changes logged with timestamps
- **Dynamic Risk Assessment**: Risk scores adapt based on incidents and automation levels
- **Incident Impact Tracking**: Monitor how security events affect compliance posture
- **Solution Effectiveness Measurement**: Track improvement metrics from remediation efforts
- **Compliance Drift Detection**: Proactive monitoring of control degradation over time
- **Alert Management**: Comprehensive notification system for governance teams

## 🛠️ Customization

### Adding New Controls
```python
# Add custom ISO 27001 control
new_control = ControlRequirement(
    control_id="A.9.1.1",
    title="Access Control Policy", 
    description="Business requirement for access control shall be established",
    standard="ISO27001",
    status=ComplianceStatus.NOT_ASSESSED,
    risk_level=RiskLevel.HIGH,
    implementation_date="",
    next_review_date="",
    responsible_team="Access Management",
    evidence_documents=[]
)
```

### Extending Standards
The system is designed to easily accommodate additional standards:
- NIST Cybersecurity Framework
- SOC 2 Controls
- GDPR Requirements
- Custom organizational standards

## 📞 Support

For governance teams implementing this system:

1. **Training**: Review the control requirements for your organization
2. **Team Assignment**: Assign responsible teams for each control area
3. **Regular Reviews**: Schedule periodic compliance assessments
4. **Documentation**: Maintain evidence documents for audit purposes

## 🔄 Dynamic Governance Workflow

### Real-time Operations:
- **Continuous Monitoring**: 10-second background checks for compliance drift and incidents
- **Immediate Alerts**: Real-time notifications for governance teams
- **Instant Impact Assessment**: See how incidents affect overall compliance posture
- **On-demand Remediation**: Implement solutions with immediate measurable results

### Recommended Governance Schedule:
- **Real-time**: Monitor active alerts and respond to critical incidents
- **Daily**: Review incident feed and implement solutions for non-compliant controls
- **Weekly**: Analyze compliance trends and automation effectiveness
- **Monthly**: Comprehensive assessment of drift patterns and solution outcomes
- **Quarterly**: Strategic review of automation levels and process improvements

## 🌟 Why This System is Unique

Unlike static compliance tracking tools, this system provides:

- **Living Compliance Data**: Status changes in real-time based on actual operational events
- **Predictive Insights**: Compliance drift detection before issues become critical
- **Measurable Remediation**: Solutions show immediate, quantifiable impact on compliance scores
- **Realistic Simulation**: Mirrors real-world enterprise environments where compliance is constantly changing
- **Actionable Intelligence**: Governance teams can see exactly what needs attention and how to fix it

Perfect for **security professionals**, **compliance officers**, and **governance teams** who need dynamic visibility into their cybersecurity compliance posture with the ability to demonstrate measurable improvement through targeted remediation efforts.
