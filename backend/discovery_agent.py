// frontend-admin/pages/inventory.js
import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function NetworkInventoryPage() {
    const [inventory, setInventory] = useState([]);
    const [scanStatus, setScanStatus] = useState('Idle. Ready to scan.');
    const [networkRange, setNetworkRange] = useState('192.168.1.0/24');

    useEffect(() => {
        // Setup WebSocket connection to receive live discovery results
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const socket = new WebSocket(`${wsProtocol}//${window.location.host}/api/discovery/ws/subscribe`);

        socket.onopen = () => console.log("Subscribed to discovery feed.");
        socket.onmessage = (event) => {
            const result = JSON.parse(event.data);
            
            if (result.type === 'scan_status') {
                setScanStatus(result.data);
            } else if (result.type === 'device_fingerprinted') {
                setInventory(prevInventory => {
                    const existing = prevInventory.find(d => d.mac === result.data.mac);
                    if (existing) {
                        // Update existing device
                        return prevInventory.map(d => d.mac === result.data.mac ? result.data : d);
                    } else {
                        // Add new device
                        return [...prevInventory, result.data];
                    }
                });
            }
        };

        socket.onclose = () => console.log("Discovery feed disconnected.");

        return () => socket.close(); // Cleanup on component unmount
    }, []);

    const handleStartScan = async () => {
        setInventory([]); // Clear previous results
        setScanStatus('Sending scan command...');
        try {
            await fetch('/api/discovery/scan/arp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' /*, Add Auth Header */ },
                body: JSON.stringify({ target: networkRange })
            });
        } catch (error) {
            setScanStatus(`Error: ${error.message}`);
        }
    };

    return (
        <div>
            <Head><title>Network Inventory</title></Head>
            <h1>Network Inventory & Discovery</h1>
            <article>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <input 
                        type="text" 
                        value={networkRange} 
                        onChange={(e) => setNetworkRange(e.target.value)}
                        placeholder="e.g., 192.168.1.0/24"
                    />
                    <button onClick={handleStartScan}>Start Full Scan</button>
                </div>
                <small>{scanStatus}</small>
            </article>
            <div style={{ overflowX: 'auto' }}>
                <table>
                    <thead>
                        <tr>
                            <th>IP Address</th>
                            <th>Hostname</th>
                            <th>MAC Address</th>
                            <th>Vendor</th>
                            <th>Device Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {inventory.map(device => (
                            <tr key={device.mac}>
                                <td>{device.ip}</td>
                                <td>{device.hostname || device.snmp_sysName || 'N/A'}</td>
                                <td>{device.mac}</td>
                                <td>{device.vendor}</td>
                                <td>{device.type || device.snmp_sysDescr}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
