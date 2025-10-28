import '../styles/globals.css';
import BottomNav from '../components/layout/BottomNav';
import AuthProvider from '../contexts/AuthContext';

function MyApp({ Component, pageProps }) {
  return (
    <AuthProvider>
      <div>
        <main style={{ padding: '1rem', marginBottom: '80px' }}>
          <Component {...pageProps} />
        </main>
        <BottomNav />
      </div>
    </AuthProvider>
  );
}

export default MyApp;
