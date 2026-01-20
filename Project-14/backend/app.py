from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# N8N Workflow Simulator
WORKFLOWS = {
    'email_notification': {
        'name': 'Email Notification',
        'trigger': 'Webhook',
        'nodes': ['Webhook', 'Process', 'Email'],
        'description': 'Sends email notifications'
    },
    'data_sync': {
        'name': 'Data Sync',
        'trigger': 'Schedule',
        'nodes': ['Schedule', 'Fetch Data', 'Transform', 'Save'],
        'description': 'Syncs data from source to destination'
    },
    'slack_alert': {
        'name': 'Slack Alert',
        'trigger': 'Webhook',
        'nodes': ['Webhook', 'Filter', 'Slack'],
        'description': 'Sends alerts to Slack'
    },
    'form_handler': {
        'name': 'Form Handler',
        'trigger': 'Webhook',
        'nodes': ['Webhook', 'Validate', 'Database', 'Email'],
        'description': 'Processes form submissions'
    }
}

EXECUTIONS = []

def execute_workflow(workflow_id, input_data):
    """Simulate workflow execution"""
    if workflow_id not in WORKFLOWS:
        return None
    
    workflow = WORKFLOWS[workflow_id]
    execution = {
        'id': f'exec_{len(EXECUTIONS) + 1}',
        'workflow': workflow_id,
        'status': 'success',
        'started_at': datetime.now().isoformat(),
        'duration': '1.2s',
        'nodes_executed': workflow['nodes'],
        'output': {
            'message': f'Workflow {workflow["name"]} executed successfully',
            'processed_records': 42,
            'errors': 0
        }
    }
    EXECUTIONS.append(execution)
    return execution

@app.route('/api/workflows', methods=['GET'])
def list_workflows():
    """List available workflows"""
    return jsonify({
        "workflows": [
            {
                'id': k,
                'name': v['name'],
                'trigger': v['trigger'],
                'description': v['description'],
                'nodes_count': len(v['nodes'])
            }
            for k, v in WORKFLOWS.items()
        ]
    })

@app.route('/api/workflow/<workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    """Get workflow details"""
    if workflow_id not in WORKFLOWS:
        return jsonify({"error": "Workflow not found"}), 404
    
    w = WORKFLOWS[workflow_id]
    return jsonify({
        "id": workflow_id,
        "name": w['name'],
        "trigger": w['trigger'],
        "nodes": w['nodes'],
        "description": w['description']
    })

@app.route('/api/workflow/execute', methods=['POST'])
def execute():
    """Execute a workflow"""
    try:
        data = request.json
        workflow_id = data.get('workflow_id', '')
        input_data = data.get('input', {})
        
        if workflow_id not in WORKFLOWS:
            return jsonify({"error": "Workflow not found"}), 404
        
        execution = execute_workflow(workflow_id, input_data)
        
        return jsonify({
            "status": "success",
            "execution": execution
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/executions', methods=['GET'])
def list_executions():
    """List execution history"""
    return jsonify({
        "executions": EXECUTIONS[-10:],  # Last 10
        "total": len(EXECUTIONS)
    })

if __name__ == '__main__':
    app.run(debug=False, port=5013, use_reloader=False)
