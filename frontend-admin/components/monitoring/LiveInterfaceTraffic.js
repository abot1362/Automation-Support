// frontend-admin/components/monitoring/LiveInterfaceTraffic.js

import { useState, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function LiveInterfaceTraffic() {
    const [devices, setDevices] = useState([]);
    const [selectedDevice, setSelectedDevice] = useState('');
    const [charts, setCharts] = useState({}); // { 'ether1': { chartData, chartOptions }, ... }
    const socketRef = useRef(null);

    // Fetch list of MikroTik devices on component mount
    useEffect(() => {
        fetch('/api/devices?vendor=MikroTik') // API needs to support filtering
            .then(res => res.json())
            .then(data => setDevices(data));
    }, []);

    // Handle WebSocket connection when a device is selected
    useEffect(() => {
        if (!selectedDevice) return;

        // Close previous socket if it exists
        if (socketRef.current) socketRef.current.close();

        setCharts({}); // Clear old charts
        
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const token = localStorage.getItem('accessToken');
        const socket = new WebSocket(`${wsProtocol}//${window.location.host}/ws/traffic/${selectedDevice}?token=${token}`);
        socketRef.current = socket;

        socket.onopen = () => console.log(`Traffic socket connected for device ${selectedDevice}`);
        
        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            
            if (message.type === 'interfaces_list') {
                // Initialize charts for all interfaces
                const initialCharts = {};
                message.data.forEach(ifaceName => {
                    initialCharts[ifaceName] = {
                        chartData: {
                            labels: [],
                            datasets: [
                                { label: 'Download (Mbps)', data: [], borderColor: 'rgb(75, 192, 192)' },
                                { label: 'Upload (Mbps)', data: [], borderColor: 'rgb(255, 99, 132)' },
                            ],
                        },
                    };
                });
                setCharts(initialCharts);
            }
            
            if (message.type === 'traffic_update') {
                const rates = message.data;
                const now = new Date().toLocaleTimeString();

                setCharts(prevCharts => {
                    const newCharts = { ...prevCharts };
                    Object.keys(rates).forEach(ifaceName => {
                        if (newCharts[ifaceName]) {
                            const labels = [...newCharts[ifaceName].chartData.labels, now];
                            const rxData = [...newCharts[ifaceName].chartData.datasets[0].data, (rates[ifaceName].rx_bps / 1000000).toFixed(2)];
                            const txData = [...newCharts[ifaceName].chartData.datasets[1].data, (rates[ifaceName].tx_bps / 1000000).toFixed(2)];

                            // Keep chart history limited
                            if (labels.length > 30) {
                                labels.shift();
                                rxData.shift();
                                txData.shift();
                            }

                            newCharts[ifaceName].chartData = {
                                labels,
                                datasets: [ { ...newCharts[ifaceName].chartData.datasets[0], data: rxData }, { ...newCharts[ifaceName].chartData.datasets[1], data: txData }]
                            };
                        }
                    });
                    return newCharts;
                });
            }
        };

        return () => socket.close();
    }, [selectedDevice]);

    return (
        <article>
            <label htmlFor="device-select">Select MikroTik Device to Monitor:</label>
            <select id="device-select" value={selectedDevice} onChange={e => setSelectedDevice(e.target.value)}>
                <option value="">-- Please choose a device --</option>
                {devices.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
            </select>

            <div className="grid">
                {Object.keys(charts).map(ifaceName => (
                    <div key={ifaceName}>
                        <h6>{ifaceName}</h6>
                        <Line data={charts[ifaceName].chartData} options={{ animation: false, maintainAspectRatio: true }} />
                    </div>
                ))}
            </div>
        </article>
    );
}
