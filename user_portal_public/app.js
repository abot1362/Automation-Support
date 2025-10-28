// app.js - Main logic for the User Portal PWA

// --- Base Setup & Auth ---
const token = localStorage.getItem('accessToken');
if (!token && window.location.pathname.includes('index.html')) {
    window.location.href = 'login.html';
}

const API_BASE = '/api/portal'; // All API calls for the user portal will use this prefix
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

async function fetchData(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, { headers, ...options });
    if (response.status === 401) {
        localStorage.removeItem('accessToken');
        window.location.href = 'login.html';
        throw new Error('Authentication failed. Please login again.');
    }
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'API request failed.');
    }
    return response.json();
}

// --- PWA Setup ---
document.addEventListener('DOMContentLoaded', () => {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('service-worker.js')
            .then(() => console.log('User Service Worker Registered'));
    }
    
    // Navigation Logic
    window.addEventListener('hashchange', navigate);
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', e => {
            e.preventDefault();
            window.location.hash = new URL(item.href).hash;
        });
    });

    document.getElementById('logout-button')?.addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        window.location.href = 'login.html';
    });
    
    navigate(); // Initial page load
});

// --- Router ---
function navigate() {
    const hash = window.location.hash || '#dashboard';
    const pageId = hash.substring(1);
    
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelector(`.nav-item[href="${hash}"]`)?.classList.add('active');
    
    const pageTitleEl = document.getElementById('page-title');
    const appContentEl = document.getElementById('app-content');
    
    pageTitleEl.textContent = document.querySelector(`.nav-item[href="${hash}"]`)?.dataset.pageTitle || 'Dashboard';
    appContentEl.innerHTML = `<div aria-busy="true">Loading...</div>`;

    switch (pageId) {
        case 'dashboard':
            loadDashboardContent(appContentEl);
            break;
        case 'tickets':
            loadTicketsContent(appContentEl);
            break;
        case 'chat':
            appContentEl.innerHTML = '<h2>Chat</h2><p>Chat functionality coming soon.</p>';
            break;
        case 'access':
            loadRemoteAccessContent(appContentEl);
            break;
        case 'profile':
            loadProfileContent(appContentEl);
            break;
        default:
            appContentEl.innerHTML = `<h2>Page Not Found</h2>`;
    }
    lucide.createIcons();
}

// --- Page Content Loaders ---

async function loadDashboardContent(container) {
    try {
        const usageData = await fetchData('/usage-stats');
        container.innerHTML = `
            <article>
                <header>Internet Usage (Last 30 entries)</header>
                <canvas id="usageChart"></canvas>
            </article>
        `;
        // Logic to draw chart with Chart.js using usageData
        new Chart(document.getElementById('usageChart'), {
            type: 'bar',
            data: {
                labels: usageData.map(d => new Date(d.timestamp).toLocaleDateString()),
                datasets: [
                    { label: 'Download (MB)', data: usageData.map(d => d.download_bytes / (1024*1024)) },
                    { label: 'Upload (MB)', data: usageData.map(d => d.upload_bytes / (1024*1024)) }
                ]
            }
        });
    } catch (e) { container.innerHTML = `<p style="color:red">Error loading dashboard: ${e.message}</p>`; }
}

async function loadTicketsContent(container) {
    try {
        const tickets = await fetchData('/tickets');
        let content = `<button>Create New Ticket</button>`;
        if (tickets.length === 0) {
            content += `<p>You have no open support tickets.</p>`;
        } else {
            content += tickets.map(t => `
                <article>
                    <h5>${t.title} <small>(${t.status})</small></h5>
                    <p>Last updated: ${new Date(t.updated_at).toLocaleString()}</p>
                </article>
            `).join('');
        }
        container.innerHTML = content;
    } catch (e) { container.innerHTML = `<p style="color:red">Error loading tickets: ${e.message}</p>`; }
}

async function loadRemoteAccessContent(container) {
    try {
        const connections = await fetchData('/rdp/connections');
        let content = '<h2>Remote Desktops</h2>';
        if (connections.length === 0) {
            content += `<p>You do not have access to any remote desktops.</p>`;
        } else {
            content += '<div class="grid">';
            content += connections.map(c => `
                <article>
                    <i data-lucide="monitor"></i>
                    <strong>${c.name}</strong>
                    <footer><button data-id="${c.id}" class="connect-rdp">Connect</button></footer>
                </article>
            `).join('');
            content += '</div>';
        }
        container.innerHTML = content;
        lucide.createIcons();
    } catch (e) { container.innerHTML = `<p style="color:red">Error loading remote access list: ${e.message}</p>`; }
}

async function loadProfileContent(container) {
    try {
        const user = await fetchData('/me');
        container.innerHTML = `
            <article>
                <h2>${user.full_name || user.username}</h2>
                <p><strong>Username:</strong> ${user.username}</p>
                <p><strong>Email:</strong> ${user.email || 'Not set'}</p>
                <hr>
                <button>Change Password</button>
            </article>
        `;
    } catch (e) { container.innerHTML = `<p style="color:red">Error loading profile: ${e.message}</p>`; }
}
