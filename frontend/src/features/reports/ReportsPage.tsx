import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { DownloadCloud, FileText } from 'lucide-react';

export default function ReportsPage() {
  const reports = [
    { id: 1, name: 'Weekly Occupancy Summary', date: 'Oct 24, 2023', size: '2.4 MB' },
    { id: 2, name: 'System Health & Node Status', date: 'Oct 20, 2023', size: '1.1 MB' },
    { id: 3, name: 'Monthly AI Performance Metrics', date: 'Oct 01, 2023', size: '4.8 MB' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
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

      <Card>
        <CardHeader>
          <CardTitle>Generated Reports</CardTitle>
          <CardDescription>Download past reports in PDF or CSV format.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {reports.map((report) => (
            <div key={report.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
              <div className="flex items-center gap-4">
                <div className="bg-primary/10 p-2 rounded-md">
                  <FileText className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h4 className="text-sm font-medium">{report.name}</h4>
                  <p className="text-xs text-muted-foreground">Generated {report.date} • {report.size}</p>
                </div>
              </div>
              <Button variant="outline" size="sm" className="gap-2">
                <DownloadCloud className="h-4 w-4" /> Download
              </Button>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
