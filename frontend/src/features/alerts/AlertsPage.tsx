import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, Info, BellRing } from 'lucide-react';
import { mockAlerts } from '@/mocks/data';

export default function AlertsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Alerts</h1>
        <p className="text-muted-foreground mt-2">
          System notifications and anomaly detections.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Alerts</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {mockAlerts.map((alert) => (
            <div key={alert.id} className="flex gap-4 items-start p-4 border rounded-lg bg-card">
              <div className="mt-0.5">
                {alert.type === 'critical' ? (
                  <AlertTriangle className="h-5 w-5 text-destructive" />
                ) : alert.type === 'warning' ? (
                  <BellRing className="h-5 w-5 text-amber-500" />
                ) : (
                  <Info className="h-5 w-5 text-blue-500" />
                )}
              </div>
              <div className="flex-1 space-y-1">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium leading-none">{alert.title}</p>
                  <span className="text-xs text-muted-foreground">{alert.time}</span>
                </div>
                <p className="text-sm text-muted-foreground">{alert.message}</p>
              </div>
              <Badge variant="outline" className={
                alert.type === 'critical' ? 'border-destructive text-destructive' :
                alert.type === 'warning' ? 'border-amber-500 text-amber-500' :
                'border-blue-500 text-blue-500'
              }>
                {alert.type.toUpperCase()}
              </Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
