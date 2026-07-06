import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Activity, Radio, Signal, Users } from 'lucide-react';

export default function LiveMonitorPage() {
  return (
    <div className="space-y-6 flex flex-col h-full">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <Activity className="h-8 w-8 text-primary animate-pulse" />
            Live Monitor
          </h1>
          <p className="text-muted-foreground mt-2">
            Real-time inference and raw signal analysis.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="status-pulse"></div>
          <span className="text-sm font-medium text-muted-foreground">Live Connection Active</span>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3 flex-1">
        <Card className="col-span-1 md:col-span-2 flex flex-col">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Radio className="h-5 w-5 text-primary" />
              CSI Signal Stream
            </CardTitle>
            <CardDescription>
              Raw Channel State Information (Subcarrier Amplitude)
            </CardDescription>
          </CardHeader>
          <CardContent className="flex-1 flex items-center justify-center visual-map sensing-grid mx-6 mb-6">
            <div className="text-center space-y-4">
              <Signal className="h-12 w-12 text-muted-foreground mx-auto opacity-50" />
              <p className="text-muted-foreground text-sm max-w-sm">
                Real-time charting placeholder. Connect to the WebSocket API to stream 
                raw CSI matrices.
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5 text-primary" />
                Live Inference
              </CardTitle>
              <CardDescription>
                AI Model Outputs
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="font-medium">Presence</span>
                <Badge variant="default" className="bg-green-500 hover:bg-green-600">Detected</Badge>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="font-medium">Motion Level</span>
                <span className="text-primary font-bold">High</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="font-medium">Occupancy Est.</span>
                <span className="font-bold">4 People</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="font-medium">Confidence</span>
                <span className="text-green-500 font-bold">98.2%</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Active Node</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">ID:</span>
                  <span className="font-mono">dev-001</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Location:</span>
                  <span>Main Lobby</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Ping:</span>
                  <span className="text-green-500">12ms</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
