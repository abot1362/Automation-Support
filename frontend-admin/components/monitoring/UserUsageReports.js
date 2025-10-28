// frontend-admin/components/monitoring/UserUsageReports.js
import { useState } from 'react';
import { Bar } from 'react-chartjs-2';

export default function UserUsageReports() {
    const [username, setUsername] = useState('');
    const [deviceId, setDeviceId] = useState(''); // User needs to select a device
    const [usageData, setUsageData] = useState(null);
    const [isLoading, setLoading] = useState(false);

    const handleFetchUsage = async () => {
        if (!username || !deviceId) {
            alert("Please enter a username and select a device.");
            return;
        }
        setLoading(true);
        // Date range for the last 30 days
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(endDate.getDate() - 30);

        try {
            const response = await fetch(`/api/monitoring/users/${username}/usage?device_id=${deviceId}&start_date=${startDate.toISOString()}&end_date=${endDate.toISOString()}`);
            const data = await response.json();
            setUsageData(data);
        } catch (error) {
            console.error(error);
            alert("Failed to fetch usage data.");
        } finally {
            setLoading(false);
        }
    };

    const chartData = {
        labels: usageData?.map(d => d.date) || [],
        datasets: [
            { label: 'Download (GB)', data: usageData?.map(d => (d.total_download / (1024**3)).toFixed(2)) || [], backgroundColor: 'rgba(75, 192, 192, 0.5)' },
            { label: 'Upload (GB)', data: usageData?.map(d => (d.total_upload / (1024**3)).toFixed(2)) || [], backgroundColor: 'rgba(255, 99, 132, 0.5)' },
        ],
    };

    return (
        <article>
            <div className="grid">
                {/* You need a device selector here */}
                <input type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Enter username (e.g., from Hotspot/PPP)" />
                <button onClick={handleFetchUsage} aria-busy={isLoading}>Fetch Last 30 Days Usage</button>
            </div>
            
            {usageData && (
                <div style={{marginTop: '2rem'}}>
                    <h4>Usage for: {username}</h4>
                    <Bar data={chartData} options={{ responsive: true, scales: { y: { beginAtZero: true } } }} />
                </div>
            )}
        </article>
    );
}
