import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { UploadCloud, Play, Settings2 } from 'lucide-react';
import { mockModels } from '@/mocks/data';

export default function ModelsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">AI Models</h1>
          <p className="text-muted-foreground mt-2">
            Manage, train, and deploy spatial AI models to your edge nodes.
          </p>
        </div>
        <Button className="gap-2">
          <UploadCloud className="h-4 w-4" /> Import Model
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {mockModels.map((model) => (
          <Card key={model.id} className="flex flex-col">
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle className="text-xl">{model.name}</CardTitle>
                <Badge variant={model.status === 'Active' ? 'default' : 'secondary'}
                       className={model.status === 'Active' ? 'bg-primary/20 text-primary hover:bg-primary/30 border-primary/20' : ''}>
                  {model.status}
                </Badge>
              </div>
              <CardDescription className="font-mono text-xs text-muted-foreground pt-1">
                {model.id}
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col justify-between">
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Accuracy</span>
                  <span className="font-medium text-green-500">{model.accuracy}%</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Inference Latency</span>
                  <span className="font-medium">{model.latency}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Last Updated</span>
                  <span className="font-medium">{model.updated}</span>
                </div>
              </div>
              
              <div className="flex gap-2 mt-auto">
                <Button variant="outline" size="sm" className="w-full gap-2">
                  <Settings2 className="h-4 w-4" /> Config
                </Button>
                <Button size="sm" className="w-full gap-2" variant={model.status === 'Active' ? 'secondary' : 'default'}>
                  <Play className="h-4 w-4" /> {model.status === 'Active' ? 'Redeploy' : 'Deploy'}
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
