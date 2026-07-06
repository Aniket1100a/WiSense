import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { TopNav } from './TopNav';
import { useAppStore } from '@/store/useAppStore';
import { cn } from '@/lib/utils';

export function AppLayout() {
  const { sidebarOpen } = useAppStore();

  return (
    <div className="flex min-h-screen w-full bg-background/95">
      <Sidebar />
      <div 
        className={cn(
          "flex flex-col flex-1 min-h-screen transition-all duration-300 ease-in-out",
          sidebarOpen ? "lg:pl-[220px]" : "lg:pl-20"
        )}
      >
        <TopNav />
        <main className="flex-1 overflow-auto p-4 md:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl w-full">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
