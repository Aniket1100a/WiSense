import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Clock } from 'lucide-react';
import { useDashboardOverview } from '@/hooks/useDashboard';
import { Skeleton } from '@/components/ui/skeleton';

export default function DashboardPage() {
  const { data, isLoading, isError } = useDashboardOverview();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Overview of your WiSense spatial intelligence platform.
        </p>
      </div>

      <Card className="flex flex-col items-center justify-center py-24 text-center border-dashed">
        <div className="bg-primary/10 p-4 rounded-full mb-4">
          <Clock className="h-10 w-10 text-primary" />
        </div>
        <h3 className="text-xl font-medium">Coming Soon</h3>
        <p className="text-muted-foreground max-w-md mt-2">
          Dashboard analytics and real-time overview metrics are currently being connected to the new backend APIs.
        </p>
      </Card>
    </div>
  );
}
