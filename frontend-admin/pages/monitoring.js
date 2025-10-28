// frontend-admin/pages/monitoring.js

import Head from 'next/head';
import { useState } from 'react';
import LiveInterfaceTraffic from '../components/monitoring/LiveInterfaceTraffic';
import UserUsageReports from '../components/monitoring/UserUsageReports';

export default function MonitoringPage() {
    const [activeTab, setActiveTab] = useState('live');

    return (
        <div>
            <Head><title>Network Monitoring</title></Head>
            <h1>Network Monitoring</h1>

            <nav>
                <ul>
                    <li><a href="#" role="button" className={activeTab === 'live' ? '' : 'secondary'} onClick={() => setActiveTab('live')}>Live Interface Traffic</a></li>
                    <li><a href="#" role="button" className={activeTab === 'user' ? '' : 'secondary'} onClick={() => setActiveTab('user')}>User Usage Reports</a></li>
                </ul>
            </nav>

            {activeTab === 'live' && <LiveInterfaceTraffic />}
            {activeTab === 'user' && <UserUsageReports />}
        </div>
    );
}
