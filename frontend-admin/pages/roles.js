import Head from 'next/head';
import { useEffect, useState } from 'react';
import useSWR from 'swr';

// A simple fetcher for useSWR
const fetcher = (url) => fetch(url, { headers: { 'Authorization': `Bearer ${localStorage.getItem('accessToken')}` } }).then(res => res.json());

export default function RolesPage() {
    // --- State Management ---
    const [selectedRole, setSelectedRole] = useState(null);
    const [assignedPermissions, setAssignedPermissions] = useState(new Set());
    const [isSaving, setIsSaving] = useState(false);

    // --- Data Fetching ---
    const { data: roles, error: rolesError, mutate: mutateRoles } = useSWR('/api/administration/roles');
    const { data: allPermissions, error: permissionsError } = useSWR('/api/administration/roles/all-permissions');

    // --- Effects ---
    // When a role is selected, fetch its assigned permissions
    useEffect(() => {
        if (selectedRole) {
            fetcher(`/api/administration/roles/${selectedRole.id}/permissions`).then(data => {
                setAssignedPermissions(new Set(data.map(p => p.id)));
            });
        } else {
            setAssignedPermissions(new Set());
        }
    }, [selectedRole]);

    // --- Event Handlers ---
    const handlePermissionChange = (permissionId) => {
        setAssignedPermissions(prev => {
            const newSet = new Set(prev);
            if (newSet.has(permissionId)) {
                newSet.delete(permissionId);
            } else {
                newSet.add(permissionId);
            }
            return newSet;
        });
    };

    const handleSavePermissions = async () => {
        if (!selectedRole) return;
        setIsSaving(true);
        try {
            await fetch(`/api/administration/roles/${selectedRole.id}/permissions`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('accessToken')}` },
                body: JSON.stringify(Array.from(assignedPermissions)),
            });
            alert('Permissions updated successfully!');
        } catch (error) {
            alert(`Error saving permissions: ${error.message}`);
        } finally {
            setIsSaving(false);
        }
    };

    // --- UI Rendering ---
    if (rolesError || permissionsError) return <div>Failed to load data.</div>;
    if (!roles || !allPermissions) return <div aria-busy="true">Loading roles and permissions...</div>;

    // Group permissions by module (e.g., 'devices', 'mikrotik') for better display
    const groupedPermissions = allPermissions.reduce((acc, p) => {
        const [module] = p.name.split(':');
        if (!acc[module]) acc[module] = [];
        acc[module].push(p);
        return acc;
    }, {});

    return (
        <div>
            <Head><title>Roles & Permissions</title></Head>
            <h1>Roles & Permissions Management</h1>
            <p>Define roles (work groups) and assign granular permissions to control access across the platform.</p>

            <div className="grid">
                {/* Left Column: List of Roles */}
                <article>
                    <header>
                        <strong>Roles</strong>
                    </header>
                    <div role="list">
                        {roles.map(role => (
                            <a 
                                href="#" 
                                key={role.id} 
                                onClick={(e) => { e.preventDefault(); setSelectedRole(role); }}
                                aria-current={selectedRole?.id === role.id}
                                style={{ display: 'block', marginBottom: '0.5rem' }}
                            >
                                {role.name}
                            </a>
                        ))}
                    </div>
                    <footer><button className="outline">Create New Role</button></footer>
                </article>

                {/* Right Column: Permissions for the selected role */}
                <article>
                    <header>
                        <strong>Permissions for: {selectedRole ? selectedRole.name : 'No role selected'}</strong>
                    </header>
                    
                    {selectedRole ? (
                        <div>
                            {Object.entries(groupedPermissions).map(([moduleName, permissions]) => (
                                <fieldset key={moduleName} style={{ marginBottom: '1rem' }}>
                                    <legend style={{ textTransform: 'capitalize' }}>{moduleName}</legend>
                                    {permissions.map(p => (
                                        <label key={p.id}>
                                            <input
                                                type="checkbox"
                                                checked={assignedPermissions.has(p.id)}
                                                onChange={() => handlePermissionChange(p.id)}
                                                disabled={selectedRole.name === 'Super Admin'}
                                            />
                                            {p.name}
                                        </label>
                                    ))}
                                </fieldset>
                            ))}
                        </div>
                    ) : (
                        <p>Select a role from the left to view and edit its permissions.</p>
                    )}
                    
                    {selectedRole && selectedRole.name !== 'Super Admin' && (
                        <footer>
                            <button onClick={handleSavePermissions} aria-busy={isSaving}>Save Changes</button>
                        </footer>
                    )}
                    {selectedRole && selectedRole.name === 'Super Admin' && (
                         <footer><small>Super Admin has all permissions by default.</small></footer>
                    )}
                </article>
            </div>
        </div>
    );
}
