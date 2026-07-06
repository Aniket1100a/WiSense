import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/layouts/AppLayout';
import { AuthLayout } from '@/components/layouts/AuthLayout';

import Dashboard from '@/features/dashboard/DashboardPage';
import LiveMonitor from '@/features/dashboard/LiveMonitorPage';
import Devices from '@/features/devices/DevicesPage';
import Analytics from '@/features/analytics/AnalyticsPage';
import Models from '@/features/models/ModelsPage';
import Alerts from '@/features/alerts/AlertsPage';
import Reports from '@/features/reports/ReportsPage';
import Settings from '@/features/settings/SettingsPage';
import Login from '@/features/auth/LoginPage';
import NotFound from '@/components/layouts/NotFound';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/dashboard" replace />,
  },
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'live', element: <LiveMonitor /> },
      { path: 'devices', element: <Devices /> },
      { path: 'analytics', element: <Analytics /> },
      { path: 'models', element: <Models /> },
      { path: 'alerts', element: <Alerts /> },
      { path: 'reports', element: <Reports /> },
      { path: 'settings', element: <Settings /> },
    ],
  },
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      { path: 'login', element: <Login /> },
      // other auth routes like register, forgot-password could go here
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
]);
