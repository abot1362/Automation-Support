import Head from 'next/head';
import useSWR from 'swr';

const fetcher = url => fetch(url).then(res => res.json());

export default function RdpAccessPage() {
  const { data: connections, error } = useSWR('/api/portal/rdp/connections', fetcher);

  const handleConnect = async (connectionId) => {
    // 1. Fetch a one-time token from your backend
    const res = await fetch(`/api/portal/rdp/${connectionId}/token`);
    const data = await res.json();
    
    // 2. Open the Guacamole URL with the token in a new tab
    if (data.url) {
      window.open(data.url, '_blank');
    } else {
      alert('Failed to get connection token.');
    }
  };

  return (
    <div>
      <Head><title>Remote Desktops</title></Head>
      <h1>Remote Desktops</h1>
      
      {error && <p>Failed to load remote connections.</p>}
      {!connections && <div aria-busy="true">Loading...</div>}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
        {connections && connections.map(conn => (
          <article key={conn.id}>
            <strong>{conn.name}</strong>
            <footer>
              <button onClick={() => handleConnect(conn.id)}>Connect</button>
            </footer>
          </article>
        ))}
      </div>
    </div>
  );
      }
