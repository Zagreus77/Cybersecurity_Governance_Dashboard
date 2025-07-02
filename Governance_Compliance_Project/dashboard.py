"""
Governance Dashboard for ISO 27001 & PCI DSS Compliance
Web-based dashboard for monitoring compliance status
"""

from flask import Flask, render_template, jsonify, request
import json
import datetime
from main import GovernanceManager, ComplianceStatus, RiskLevel

app = Flask(__name__)
gov_manager = GovernanceManager()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/compliance-summary')
def get_compliance_summary():
    """API endpoint for compliance summary"""
    summary = gov_manager.get_compliance_summary()
    return jsonify(summary)

@app.route('/api/controls')
def get_all_controls():
    """API endpoint for all controls"""
    all_controls = gov_manager.iso27001_controls + gov_manager.pci_dss_controls
    controls_dict = []
    
    for control in all_controls:
        control_dict = {
            'control_id': control.control_id,
            'title': control.title,
            'description': control.description,
            'standard': control.standard,
            'status': control.status.value,
            'risk_level': control.risk_level.value,
            'responsible_team': control.responsible_team,
            'notes': control.notes
        }
        controls_dict.append(control_dict)
    
    return jsonify(controls_dict)

@app.route('/api/update-control', methods=['POST'])
def update_control():
    """API endpoint to update control status"""
    data = request.json
    control_id = data.get('control_id')
    status = ComplianceStatus(data.get('status'))
    notes = data.get('notes', '')
    
    success = gov_manager.update_control_status(control_id, status, notes)
    
    return jsonify({'success': success})

@app.route('/api/risk-assessment')
def get_risk_assessment():
    """API endpoint for risk assessment data"""
    all_controls = gov_manager.iso27001_controls + gov_manager.pci_dss_controls
    
    risk_data = {
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0
    }
    
    non_compliant_by_risk = {
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0
    }
    
    for control in all_controls:
        risk_level = control.risk_level.value
        risk_data[risk_level] += 1
        
        if control.status == ComplianceStatus.NON_COMPLIANT:
            non_compliant_by_risk[risk_level] += 1
    
    return jsonify({
        'total_by_risk': risk_data,
        'non_compliant_by_risk': non_compliant_by_risk
    })

@app.route('/api/alerts')
def get_alerts():
    """API endpoint for active alerts"""
    return jsonify(gov_manager.get_active_alerts())

@app.route('/api/acknowledge-alert', methods=['POST'])
def acknowledge_alert():
    """API endpoint to acknowledge an alert"""
    data = request.json
    alert_id = data.get('alert_id')
    
    success = gov_manager.acknowledge_alert(alert_id)
    return jsonify({'success': success})

@app.route('/api/incidents')
def get_recent_incidents():
    """API endpoint for recent incidents"""
    recent_incidents = [
        {
            "incident_id": inc.incident_id,
            "title": inc.title,
            "description": inc.description,
            "severity": inc.severity.value,
            "occurrence_time": inc.occurrence_time.isoformat(),
            "affected_controls": inc.affected_controls,
            "resolved": inc.resolution_time is not None
        }
        for inc in gov_manager.incidents[-20:]  # Last 20 incidents
    ]
    return jsonify(recent_incidents)

@app.route('/api/trigger-simulation', methods=['POST'])
def trigger_simulation():
    """Manually trigger compliance simulation for demo"""
    gov_manager._check_compliance_drift()
    gov_manager._simulate_incidents()
    gov_manager._check_overdue_reviews()
    
    return jsonify({
        'success': True,
        'message': 'Simulation triggered',
        'active_alerts': len(gov_manager.get_active_alerts()),
        'total_incidents': len(gov_manager.incidents)
    })

@app.route('/api/force-incident', methods=['POST'])
def force_incident():
    """Force create an incident for immediate demo"""
    incident = gov_manager.force_incident()
    
    return jsonify({
        'success': True,
        'incident': {
            'incident_id': incident.incident_id,
            'title': incident.title,
            'severity': incident.severity.value,
            'affected_controls': incident.affected_controls
        },
        'active_alerts': len(gov_manager.get_active_alerts())
    })

@app.route('/api/resolve-incident', methods=['POST'])
def resolve_incident():
    """Resolve an incident"""
    data = request.json
    incident_id = data.get('incident_id')
    
    success = gov_manager.resolve_incident(incident_id)
    return jsonify({'success': success})

@app.route('/api/implement-solution', methods=['POST'])
def implement_solution():
    """Implement a solution for a control"""
    data = request.json
    control_id = data.get('control_id')
    solution_type = data.get('solution_type')
    
    success = gov_manager.implement_solution(control_id, solution_type)
    return jsonify({'success': success})

@app.route('/api/non-compliant-controls')
def get_non_compliant_controls():
    """Get controls that need solutions"""
    all_controls = gov_manager.iso27001_controls + gov_manager.pci_dss_controls
    
    non_compliant = []
    for control in all_controls:
        if control.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.IN_PROGRESS]:
            non_compliant.append({
                'control_id': control.control_id,
                'title': control.title,
                'status': control.status.value,
                'risk_level': control.risk_level.value,
                'automation_level': control.automation_level,
                'incident_count': control.incident_count
            })
    
    return jsonify(non_compliant)

@app.route('/api/compliance-trends')
def get_compliance_trends():
    """API endpoint for compliance trends over time"""
    all_controls = gov_manager.iso27001_controls + gov_manager.pci_dss_controls
    
    # Calculate dynamic risk scores
    total_risk_score = 0
    automation_coverage = 0
    drift_risk = 0
    
    for control in all_controls:
        # Risk scoring based on multiple factors
        base_risk = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}[control.risk_level.value]
        status_multiplier = {
            'compliant': 0.1,
            'in_progress': 0.5,
            'non_compliant': 1.0,
            'not_assessed': 0.8
        }[control.status.value]
        
        incident_factor = min(control.incident_count * 0.2, 1.0)
        control_risk = base_risk * status_multiplier * (1 + incident_factor)
        total_risk_score += control_risk
        
        automation_coverage += control.automation_level
        drift_risk += control.compliance_drift_factor * (1 - control.automation_level)
    
    avg_automation = automation_coverage / len(all_controls) if all_controls else 0
    avg_drift_risk = drift_risk / len(all_controls) if all_controls else 0
    
    return jsonify({
        'total_risk_score': round(total_risk_score, 2),
        'average_automation': round(avg_automation * 100, 1),
        'drift_risk_factor': round(avg_drift_risk * 100, 1),
        'total_incidents': len(gov_manager.incidents),
        'active_alerts': len(gov_manager.get_active_alerts())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
