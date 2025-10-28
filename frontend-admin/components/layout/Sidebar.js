import Link from 'next/link';
import { useRouter } from 'next/router';
// آیکون‌ها را از یک کتابخانه مانند 'lucide-react' وارد کنید

export default function Sidebar() {
  const router = useRouter();

  const navItems = [
    { href: '/', icon: 'LayoutDashboard', label: 'Main Dashboard' },
    // ... تمام آیتم‌های منو به صورت یک آرایه
  ];

  return (
    <aside style={{ height: '100vh', padding: '1.5rem', borderRight: '1px solid #e5e7eb' }}>
      <h2>Unified Platform</h2>
      <nav>
        {navItems.map(item => (
          <Link key={item.href} href={item.href}>
            <a className={router.pathname === item.href ? 'active' : ''}>
              {/* <Icon name={item.icon} /> */}
              <span>{item.label}</span>
            </a>
          </Link>
        ))}
      </nav>
    </aside>
  );
}
