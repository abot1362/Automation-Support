import Head from 'next/head';
import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function DashboardPage() {
  const [usageData, setUsageData] = useState(null);
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    // Replace with your actual authenticated API fetch function
    fetch('/api/portal/usage-stats')
      .then(res => res.json())
      .then(data => {
        setUsageData(data);
        setLoading(false);
      });
  }, []);

  const chartData = {
    labels: usageData?.map(d => new Date(d.timestamp).toLocaleDateString()) || [],
    datasets: [
      { label: 'Download (MB)', data: usageData?.map(d => d.download_bytes / (1024*1024)) || [] },
    ],
  };

  return (
    <div>
      <Head><title>Dashboard</title></Head>
      <h1>Your Dashboard</h1>
      <article>
        <header>Internet Usage</header>
        {isLoading && <div aria-busy="true">Loading chart...</div>}
        {usageData && <Bar data={chartData} />}
      </article>
    </div>
  );
}
