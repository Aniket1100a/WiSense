import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileText, Clock } from 'lucide-react';

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Reports</h1>
          <p className="text-muted-foreground mt-2">
            Generated summaries and data exports.
          </p>
        </div>
        <Button className="gap-2">
          <FileText className="h-4 w-4" /> Generate New
        </Button>
      </div>

      <Card className="flex flex-col items-center justify-center py-24 text-center border-dashed">
        <div className="bg-primary/10 p-4 rounded-full mb-4">
          <Clock className="h-10 w-10 text-primary" />
        </div>
        <h3 className="text-xl font-medium">Coming Soon</h3>
        <p className="text-muted-foreground max-w-md mt-2">
          Report generation features are currently being connected to the new backend APIs.
        </p>
      </Card>
    </div>
  );
}
