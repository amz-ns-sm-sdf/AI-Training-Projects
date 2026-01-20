const API_URL = 'http://localhost:5013/api';
let selectedWorkflow = null;

async function loadWorkflows() {
    const response = await fetch(`${API_URL}/workflows`);
    const data = await response.json();
    const workflowsDiv = document.getElementById('workflows');
    workflowsDiv.innerHTML = data.workflows.map(w => `
        <div class="workflow-card" onclick="selectWorkflow('${w.id}', this)">
            <div class="workflow-name">⚙️ ${w.name}</div>
            <div class="workflow-trigger">🔔 ${w.trigger}</div>
            <div class="nodes">${w.nodes_count} nodes</div>
        </div>
    `).join('');
}

function selectWorkflow(id, element) {
    selectedWorkflow = id;
    document.querySelectorAll('.workflow-card').forEach(el => el.classList.remove('selected'));
    element.classList.add('selected');
}

async function executeSelected() {
    if (!selectedWorkflow) {
        alert('Select a workflow');
        return;
    }
    const response = await fetch(`${API_URL}/workflow/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workflow_id: selectedWorkflow, input: {} })
    });
    const data = await response.json();
    loadExecutions();
}

async function loadExecutions() {
    const response = await fetch(`${API_URL}/executions`);
    const data = await response.json();
    const historyDiv = document.getElementById('history');
    historyDiv.innerHTML = '<h3>📋 Execution History</h3>' + data.executions.map(e => `
        <div class="execution-item">
            <div class="execution-status">✓ ${e.status.toUpperCase()}</div>
            <div>${e.workflow} - ${e.duration}</div>
            <div style="font-size: 11px; color: #666;">Records: ${e.output.processed_records}</div>
        </div>
    `).join('');
}

window.addEventListener('load', () => {
    loadWorkflows();
    loadExecutions();
    setInterval(loadExecutions, 5000);
});
