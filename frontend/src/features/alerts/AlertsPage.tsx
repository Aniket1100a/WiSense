import { Card } from '@/components/ui/card';
import { Clock } from 'lucide-react';

export default function AlertsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Alerts</h1>
        <p className="text-muted-foreground mt-2">
          System notifications and anomaly detections.
        </p>
      </div>

      <Card className="flex flex-col items-center justify-center py-24 text-center border-dashed">
        <div className="bg-primary/10 p-4 rounded-full mb-4">
          <Clock className="h-10 w-10 text-primary" />
        </div>
        <h3 className="text-xl font-medium">Coming Soon</h3>
        <p className="text-muted-foreground max-w-md mt-2">
          Alerts integration is currently being connected to the new backend APIs.
        </p>
      </Card>
    </div>
  );
}
