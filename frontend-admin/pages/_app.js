import '../styles/globals.css'; // Assuming you use Tailwind CSS or a global stylesheet
import Sidebar from '../components/layout/Sidebar';
import AuthProvider from '../contexts/AuthContext'; // A wrapper for managing login state

function MyApp({ Component, pageProps }) {
  return (
    <AuthProvider>
      <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr' }}>
        <Sidebar />
        <main style={{ padding: '1.5rem', height: '100vh', overflowY: 'auto' }}>
          <Component {...pageProps} />
        </main>
      </div>
    </AuthProvider>
  );
}

export default MyApp;
