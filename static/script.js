let severityChartInstance = null;

async function fetchLogs() {
    try {
        const response = await fetch('/api/logs');
        const logs = await response.json();
        updateDashboard(logs);
    } catch (error) {
        console.error("Error fetching logs:", error);
    }
}

function updateDashboard(logs) {
    // Basic Metrics
    const totalCount = logs.length;
    let highSevCount = 0;
    let mediumSevCount = 0;
    let lowSevCount = 0;
    
    logs.forEach(log => {
        const severity = log.Severity ? log.Severity.toUpperCase() : '';
        if (severity === 'HIGH') highSevCount++;
        else if (severity === 'MEDIUM') mediumSevCount++;
        else lowSevCount++;
    });

    document.getElementById('total-count').textContent = totalCount;
    document.getElementById('high-sev-count').textContent = highSevCount;

    if (logs.length > 0) {
        const latestLog = logs[logs.length - 1];
        const ts = latestLog.Timestamp;
        const timeStr = ts.includes(' ') ? ts.split(' ')[1] : ts;
        document.getElementById('latest-time').textContent = timeStr;
    }

    updateTable(logs);
    updateChart(highSevCount, mediumSevCount, lowSevCount);
}

function updateTable(logs) {
    const tbody = document.getElementById('logsBody');
    tbody.innerHTML = ''; 

    const recentLogs = [...logs].reverse().slice(0, 10);

    recentLogs.forEach(log => {
        const tr = document.createElement('tr');
        
        let sevClass = 'severity-low';
        let severityText = log.Severity ? log.Severity.toUpperCase() : 'UNKNOWN';
        if (severityText === 'HIGH') sevClass = 'severity-high';
        if (severityText === 'MEDIUM') sevClass = 'severity-medium';

        tr.innerHTML = `
            <td>${log.Timestamp}</td>
            <td><span class="severity-pill ${sevClass}">${severityText}</span></td>
            <td>${log.Cause || '-'}</td>
            <td style="font-family: monospace; font-size: 0.85rem; color: #94a3b8;">
                ${parseFloat(log.Latitude).toFixed(4)}, ${parseFloat(log.Longitude).toFixed(4)}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function updateChart(high, medium, low) {
    const ctx = document.getElementById('severityChart').getContext('2d');
    
    if (severityChartInstance) {
        severityChartInstance.data.datasets[0].data = [high, medium, low];
        severityChartInstance.update();
        return;
    }

    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter';

    severityChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['High', 'Medium', 'Low'],
            datasets: [{
                data: [high, medium, low],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)', 
                    'rgba(245, 158, 11, 0.8)', 
                    'rgba(59, 130, 246, 0.8)'  
                ],
                borderColor: [
                    '#ef4444',
                    '#f59e0b',
                    '#3b82f6'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#f8fafc' }
                }
            },
            cutout: '75%'
        }
    });
}

// Initial fetch
fetchLogs();
// Poll every 5 seconds
setInterval(fetchLogs, 5000);
