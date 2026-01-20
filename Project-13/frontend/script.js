const API_URL = 'http://localhost:5012/api/mcp';
let selectedService = null;

async function loadServices() {
    const response = await fetch(`${API_URL}/services`);
    const data = await response.json();
    const servicesDiv = document.getElementById('services');
    servicesDiv.innerHTML = data.services.map(s => `
        <div class="service-card" onclick="selectService('${s.id}')">
            <div class="service-name">🔧 ${s.name}</div>
            <div class="service-desc">${s.description}</div>
        </div>
    `).join('');
}

function selectService(serviceId) {
    selectedService = serviceId;
}

async function sendRequest() {
    if (!selectedService) {
        alert('Select a service');
        return;
    }
    const payload = document.getElementById('payload').value;
    const response = await fetch(`${API_URL}/request`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ service: selectedService, payload })
    });
    const data = await response.json();
    const respDiv = document.getElementById('response');
    respDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    respDiv.classList.add('show');
}

window.addEventListener('load', loadServices);
