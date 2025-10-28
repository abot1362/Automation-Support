import Head from 'next/head';
import useSWR from 'swr'; // A great library for data fetching

const fetcher = url => fetch(url).then(res => res.json());

export default function TicketsPage() {
  const { data: tickets, error } = useSWR('/api/portal/tickets', fetcher);

  return (
    <div>
      <Head><title>Support Tickets</title></Head>
      <h1>My Support Tickets</h1>
      <button>Create New Ticket</button>
      
      {error && <p>Failed to load tickets.</p>}
      {!tickets && <div aria-busy="true">Loading...</div>}

      {tickets && tickets.map(ticket => (
        <article key={ticket.id}>
          <h5>{ticket.title}</h5>
          <p>Status: <strong>{ticket.status}</strong></p>
          <footer>Last updated: {new Date(ticket.updated_at).toLocaleString()}</footer>
        </article>
      ))}
    </div>
  );
}
