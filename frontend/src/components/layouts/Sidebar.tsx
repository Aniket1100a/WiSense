import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Activity, 
  Wifi, 
  Search,
  BarChart3, 
  BrainCircuit, 
  Bell, 
  FileText, 
  Settings,
  Menu,
  Database
} from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Live Monitor', href: '/live', icon: Activity },
  { name: 'Devices', href: '/devices', icon: Wifi },
  { name: 'Discovery', href: '/discovery', icon: Search },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'AI Models', href: '/models', icon: BrainCircuit },
  { name: 'Alerts', href: '/alerts', icon: Bell },
  { name: 'Reports', href: '/reports', icon: FileText },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const { sidebarOpen, toggleSidebar } = useAppStore();
  const location = useLocation();

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-50 flex flex-col border-r bg-card transition-all duration-300 ease-in-out h-screen",
        sidebarOpen ? "w-[220px]" : "w-20 hidden lg:flex"
      )}
    >
      <div className="flex h-14 items-center justify-between px-4 border-b">
        <Link to="/" className={cn("flex items-center gap-2", !sidebarOpen && "hidden")}>
          <div className="bg-primary/10 p-1.5 rounded-md">
            <Wifi className="h-6 w-6 text-primary" />
          </div>
          <span className="text-xl font-bold tracking-tight">WiSense</span>
        </Link>
        <Button variant="ghost" size="icon" onClick={toggleSidebar} className="ml-auto lg:flex hidden">
          <Menu className="h-5 w-5" />
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-2">
          {navigation.map((item) => {
            const isActive = location.pathname.startsWith(item.href);
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "group flex items-center rounded-md px-3 py-2.5 text-sm font-medium transition-colors",
                  isActive 
                    ? "bg-primary/10 text-primary" 
                    : "text-muted-foreground hover:bg-muted hover:text-foreground",
                  !sidebarOpen && "justify-center"
                )}
                title={!sidebarOpen ? item.name : undefined}
              >
                <item.icon
                  className={cn(
                    "flex-shrink-0 transition-colors",
                    sidebarOpen ? "mr-3 h-5 w-5" : "h-5 w-5",
                    isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"
                  )}
                  aria-hidden="true"
                />
                <span className={cn(!sidebarOpen && "hidden")}>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>
      
      <div className="p-4 border-t">
        <div className={cn("flex items-center gap-3", !sidebarOpen && "justify-center")}>
          <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-medium text-xs">
            AD
          </div>
          {sidebarOpen && (
            <div className="flex flex-col">
              <span className="text-sm font-medium leading-none">Admin User</span>
              <span className="text-xs text-muted-foreground mt-1">admin@wisense.io</span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
