import { useEffect, useState } from 'react';
import Head from 'next/head';

// یک تابع کمکی برای فراخوانی API
async function fetcher(url) {
  const res = await fetch(url);
  if (!res.ok) {
    const error = new Error('An error occurred while fetching the data.');
    error.info = await res.json();
    error.status = res.status;
    throw error;
  }
  return res.json();
}

export default function DevicesPage() {
  const [devices, setDevices] = useState(null);
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    fetcher('/api/devices') // به لطف rewrite، این به بک‌اند ارسال می‌شود
      .then(data => {
        setDevices(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Failed to load devices", error);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <Head>
        <title>Device Management</title>
      </Head>
      <h1>Device Management</h1>
      
      {isLoading && <p>Loading devices...</p>}
      
      {!isLoading && devices && (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Vendor</th>
              <th>Host</th>
            </tr>
          </thead>
          <tbody>
            {devices.map(device => (
              <tr key={device.id}>
                <td>{device.name}</td>
                <td>{device.vendor}</td>
                <td>{device.host}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
