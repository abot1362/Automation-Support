// frontend-admin/pages/login.js
import { useState } from 'react';

export default function LoginPage() {
  const [error, setError] = useState('');

  // این تنظیمات باید از یک API خوانده شوند
  const enabledAuthProviders = ['local', 'ldap']; 

  const handleLogin = async (event, authType) => {
    event.preventDefault();
    setError('');
    // ...
    const username = event.target.username.value;
    const password = event.target.password.value;
    
    try {
      const response = await fetch('/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, type: authType })
      });
      // ... (ادامه منطق لاگین)
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Admin Portal Login</h1>
      
      {/* فرم لاگین محلی */}
      {enabledAuthProviders.includes('local') && (
        <form onSubmit={(e) => handleLogin(e, 'local')}>
          <h3>Login with Local Account</h3>
          <input name="username" type="text" placeholder="Username" required />
          <input name="password" type="password" placeholder="Password" required />
          <button type="submit">Login</button>
        </form>
      )}

      {/* فرم لاگین LDAP/AD */}
      {enabledAuthProviders.includes('ldap') && (
        <form onSubmit={(e) => handleLogin(e, 'ldap')} style={{marginTop: '2rem'}}>
          <h3>Login with Corporate Account (LDAP)</h3>
          <input name="username" type="text" placeholder="Domain Username" required />
          <input name="password" type="password" placeholder="Domain Password" required />
          <button type="submit">Login with LDAP</button>
        </form>
      )}

      {error && <p style={{color: 'red'}}>{error}</p>}
    </div>
  );
}
