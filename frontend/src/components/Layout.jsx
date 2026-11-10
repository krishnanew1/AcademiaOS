import { Outlet, useNavigate, NavLink, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { tokenUtils } from '../api';
import './Layout.css';

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  // Close the mobile menu whenever the route changes.
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  // Get user role from localStorage
  const userRole = localStorage.getItem('user_role');

  // If no role is found, try to get it from user_info
  if (!userRole) {
    const userInfo = localStorage.getItem('user_info');
    if (userInfo) {
      try {
        const parsed = JSON.parse(userInfo);
        if (parsed.role) {
          localStorage.setItem('user_role', parsed.role);
        }
      } catch (e) {
        console.error('Error parsing user info:', e);
      }
    }
  }

  const handleLogout = () => {
    tokenUtils.clearTokens();
    localStorage.removeItem('user_info');
    localStorage.removeItem('user_role');
    navigate('/');
  };

  // Get dashboard path based on role
  const getDashboardPath = () => {
    switch (userRole) {
      case 'ADMIN':
        return '/admin';
      case 'FACULTY':
        return '/faculty';
      case 'STUDENT':
        return '/student';
      default:
        return '/admin';
    }
  };

  // Role-based navigation items
  const getNavigationItems = () => {
    switch (userRole) {
      case 'ADMIN':
        return [
          { path: '/admin', label: 'Dashboard', icon: '', isDashboard: true },
          { path: '/admin/settings', label: 'Settings', icon: '' },
          { path: '/admin/students', label: 'Students', icon: '' },
          { path: '/admin/registration-tracking', label: 'Reg. Tracking', icon: '' },
          { path: '/admin/academics', label: 'Academics', icon: '' },
          { path: '/admin/attendance', label: 'Attendance', icon: '' },
          { path: '/admin/faculty', label: 'Faculty', icon: '' },
          { path: '/admin/grades', label: 'Grades', icon: '' },
          { path: '/admin/timetables', label: 'Timetables', icon: '' },
        ];
      case 'FACULTY':
        return [
          { path: '/faculty', label: 'Dashboard', icon: '', isDashboard: true },
          { path: '/faculty/grades', label: 'Grades', icon: '' },
          { path: '/faculty/attendance', label: 'Attendance', icon: '' },
          { path: '/faculty/timetable', label: 'My Timetable', icon: '' },
          { path: '/faculty/works', label: 'My Works', icon: '' },
        ];
      case 'STUDENT':
        return [
          { path: '/student', label: 'Dashboard', icon: '', isDashboard: true },
          { path: '/student/register', label: 'Semester Reg.', icon: '' },
          { path: '/student/timetable', label: 'Timetable', icon: '' },
          { path: '/student/attendance', label: 'My Attendance', icon: '' },
          { path: '/student/faculty', label: 'Faculty', icon: '' },
          { path: '/student/grades', label: 'Grades', icon: '' },
          { path: '/student/reports', label: 'Reports', icon: '' },
        ];
      default:
        return [
          { path: '/admin', label: '📊 Dashboard', icon: '📊', isDashboard: true },
        ];
    }
  };

  const navigationItems = getNavigationItems();

  return (
    <div className="layout-container">
      {/* Top Navbar */}
      <header className="layout-header">
        <div className="header-content">
          <div className="header-left">
            <button
              className="menu-toggle-btn"
              aria-label={menuOpen ? 'Close navigation menu' : 'Open navigation menu'}
              aria-expanded={menuOpen}
              aria-controls="layout-sidebar-nav"
              onClick={() => setMenuOpen((v) => !v)}
            >
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                strokeWidth="2" strokeLinecap="round" aria-hidden="true">
                {menuOpen ? (
                  <>
                    <line x1="6" y1="6" x2="18" y2="18" />
                    <line x1="18" y1="6" x2="6" y2="18" />
                  </>
                ) : (
                  <>
                    <line x1="3" y1="6" x2="21" y2="6" />
                    <line x1="3" y1="12" x2="21" y2="12" />
                    <line x1="3" y1="18" x2="21" y2="18" />
                  </>
                )}
              </svg>
            </button>
            <h1 className="header-title">Academic ERP</h1>
            {userRole && (
              <span className="user-role-badge">
                {userRole === 'ADMIN' ? 'Admin' : userRole === 'FACULTY' ? 'Faculty' : 'Student'}
              </span>
            )}
          </div>
          <div className="header-right">
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="layout-body">
        {/* Backdrop for mobile menu */}
        {menuOpen && (
          <div
            className="sidebar-backdrop"
            onClick={() => setMenuOpen(false)}
            aria-hidden="true"
          />
        )}
        {/* Sidebar Navigation */}
        <aside className={`layout-sidebar${menuOpen ? ' open' : ''}`} id="layout-sidebar-nav">
          <nav className="sidebar-nav" aria-label="Primary">
            <ul className="nav-list">
              {navigationItems.map((item) => (
                <li key={item.path} className="nav-item">
                  <NavLink 
                    to={item.path}
                    end={item.isDashboard}
                    className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                    onClick={() => setMenuOpen(false)}
                  >
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        {/* Main Content Area */}
        <main className="layout-main">
          <div className="main-content">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;