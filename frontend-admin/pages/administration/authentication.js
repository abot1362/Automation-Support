import Head from 'next/head';
import { useState, useEffect } from 'react';
import useSWR from 'swr'; // For data fetching

// You would create a simple fetcher function
const fetcher = url => fetch(url, { headers: { /* Your Auth Headers */ } }).then(res => res.json());

export default function AuthenticationProvidersPage() {
    const [activeTab, setActiveTab] = useState('ldap');

    // Fetch existing settings when the page loads
    const { data: settings, error } = useSWR('/api/administration/auth/settings', fetcher);

    if (error) return <div>Failed to load authentication settings.</div>;
    if (!settings) return <div aria-busy="true">Loading settings...</div>;

    return (
        <div>
            <Head>
                <title>Authentication Providers</title>
            </Head>
            <h1>Authentication Providers</h1>
            <p>Configure external authentication sources like Active Directory (LDAP/Kerberos) and RADIUS to enable centralized login and Single Sign-On (SSO).</p>

            {/* Tab Navigation */}
            <nav>
                <ul>
                    <li><a href="#" role="button" className={activeTab === 'ldap' ? '' : 'secondary outline'} onClick={() => setActiveTab('ldap')}>LDAP / Active Directory</a></li>
                    <li><a href="#" role="button" className={activeTab === 'kerberos' ? '' : 'secondary outline'} onClick={() => setActiveTab('kerberos')}>Kerberos (SSO)</a></li>
                    <li><a href="#" role="button" className={activeTab === 'radius' ? '' : 'secondary outline'} onClick={() => setActiveTab('radius')}>RADIUS</a></li>
                </ul>
            </nav>

            {/* Tab Content */}
            {activeTab === 'ldap' && <LdapSettings initialSettings={settings.ldap} />}
            {activeTab === 'kerberos' && <KerberosSettings initialSettings={settings.kerberos} />}
            {activeTab === 'radius' && <RadiusSettings initialSettings={settings.radius} />}
        </div>
    );
}

// --- Component for LDAP Settings ---
function LdapSettings({ initialSettings }) {
    const [formData, setFormData] = useState(initialSettings || {});
    const [isTesting, setIsTesting] = useState(false);
    const [testResult, setTestResult] = useState(null);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    };

    const handleTestConnection = async (e) => {
        e.preventDefault();
        setIsTesting(true);
        setTestResult(null);
        try {
            // API call to test LDAP connection
            const response = await fetch('/api/administration/auth/ldap/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', /* Auth Header */ },
                body: JSON.stringify(formData),
            });
            const result = await response.json();
            setTestResult(result);
        } catch (error) {
            setTestResult({ success: false, message: error.message });
        } finally {
            setIsTesting(false);
        }
    };

    const handleSave = async (e) => {
        e.preventDefault();
        // API call to save LDAP settings
        alert('Saving LDAP settings...');
    };

    return (
        <article>
            <h2>LDAP / Active Directory Settings</h2>
            <form onSubmit={handleSave}>
                <label>
                    <input type="checkbox" name="enabled" checked={formData.enabled || false} onChange={handleChange} />
                    Enable LDAP Authentication
                </label>
                <hr />
                <div className="grid">
                    <label>Server Host
                        <input type="text" name="server" value={formData.server || ''} onChange={handleChange} placeholder="e.g., dc.mycorp.local" />
                    </label>
                    <label>Port
                        <input type="number" name="port" value={formData.port || 389} onChange={handleChange} />
                    </label>
                </div>
                <label>
                    <input type="checkbox" name="use_ssl" checked={formData.use_ssl || false} onChange={handleChange} />
                    Use LDAPS (SSL)
                </label>
                
                <label>Base DN (Distinguished Name)
                    <input type="text" name="base_dn" value={formData.base_dn || ''} onChange={handleChange} placeholder="e.g., ou=Users,dc=mycorp,dc=local" />
                    <small>The starting point for user searches in your directory.</small>
                </label>
                
                <label>Bind Username (Service Account)
                    <input type="text" name="bind_dn" value={formData.bind_dn || ''} onChange={handleChange} placeholder="e.g., cn=service-ldap,ou=Services,dc=mycorp,dc=local" />
                    <small>A read-only user for syncing users and groups.</small>
                </label>
                <label>Bind Password
                    <input type="password" name="bind_password" value={formData.bind_password || ''} onChange={handleChange} />
                </label>

                <footer>
                    <button type="button" onClick={handleTestConnection} className="secondary" aria-busy={isTesting}>Test Connection</button>
                    <button type="submit">Save Settings</button>
                </footer>
            </form>
            {testResult && (
                <p style={{ color: testResult.success ? 'green' : 'red', marginTop: '1rem' }}>
                    <strong>Test Result:</strong> {testResult.message}
                </p>
            )}
        </article>
    );
}

// --- Component for Kerberos Settings ---
function KerberosSettings({ initialSettings }) {
    // This component is mostly instructional as setup is complex
    return (
        <article>
            <h2>Kerberos (SSO) Settings</h2>
            <p>Enabling Kerberos provides a seamless Single Sign-On (SSO) experience for users within your corporate domain. Users will be logged in automatically without entering a password.</p>
            
            <h4>Setup Guide:</h4>
            <ol>
                <li>
                    <strong>Create a Service Principal Name (SPN)</strong> in your Active Directory for the web service.
                    <pre><code>setspn -A HTTP/admin.your-platform.com your_service_account</code></pre>
                </li>
                <li>
                    <strong>Generate a Keytab file</strong> for this SPN on your Domain Controller.
                    <pre><code>ktpass /out http.keytab /princ HTTP/admin.your-platform.com@YOUR.REALM /mapuser your_service_account /pass YourPassword /crypto All /ptype KRB5_NT_PRINCIPAL</code></pre>
                </li>
                <li>
                    <strong>Upload the Keytab file</strong> securely to the backend server.
                    {/* In a real app, this would be a file upload button */}
                    <input type="file" disabled/>
                </li>
                <li>
                    <strong>Enable Kerberos Auth
