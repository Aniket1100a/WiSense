import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Cpu, Laptop, Usb, Database, Box, Wifi, Search, XCircle, Clock, Server, Plus, Activity, PlayCircle, StopCircle, RefreshCcw } from 'lucide-react';
import { ProviderType, DiscoveryResult } from '@/types/api';
import { useProviders, useStartDiscovery, useRegisterDevice } from '@/hooks/useDiscovery';

type ScanStatus = 'idle' | 'scanning' | 'complete' | 'error';

const getProviderIcon = (type: ProviderType) => {
  switch (type) {
    case 'ESP32': return <Cpu className="h-5 w-5" />;
    case 'Laptop': return <Laptop className="h-5 w-5" />;
    case 'USB Adapter': return <Usb className="h-5 w-5" />;
    case 'Dataset': return <Database className="h-5 w-5" />;
    case 'Simulator': return <Box className="h-5 w-5" />;
    case 'Intel CSI': return <Server className="h-5 w-5" />;
    default: return <Wifi className="h-5 w-5" />;
  }
};

export default function DiscoveryPage() {
  const [scanStatus, setScanStatus] = useState<ScanStatus>('idle');
  const [selectedProvider, setSelectedProvider] = useState<ProviderType | 'All'>('All');
  const [progress, setProgress] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [results, setResults] = useState<DiscoveryResult[]>([]);

  const { data: providers = [], isLoading: providersLoading } = useProviders();
  const startScanMutation = useStartDiscovery();
  const registerDeviceMutation = useRegisterDevice();

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (scanStatus === 'scanning') {
      interval = setInterval(() => {
        setProgress(p => {
          if (p >= 100) {
            setScanStatus('complete');
            return 100;
          }
          return p + 2;
        });
        setElapsed(e => e + 1);
      }, 100);
    } else {
      setProgress(0);
      setElapsed(0);
    }
    return () => clearInterval(interval);
  }, [scanStatus]);

  const startScan = async (provider: ProviderType | 'All') => {
    setSelectedProvider(provider);
    setScanStatus('scanning');
    setResults([]);
    try {
      const discovered = await startScanMutation.mutateAsync(provider);
      // Wait for progress to reach 100 before setting complete, 
      // but we can set results as soon as mutation resolves.
      setResults(discovered);
    } catch (e) {
      console.error(e);
      setScanStatus('error');
    }
  };

  const stopScan = () => {
    setScanStatus('idle');
  };

  const refreshScan = () => {
    startScan(selectedProvider);
  };

  const filteredProviders = providers.filter(p => selectedProvider === 'All' || p.type === selectedProvider);

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Discovery</h1>
          <p className="text-muted-foreground mt-2">
            Scan the environment for available WiSense providers and new devices.
          </p>
        </div>
        
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="outline" className="px-3 py-1.5 text-sm h-9 bg-card">
            Status: {scanStatus === 'scanning' ? <span className="text-amber-500 ml-1 flex items-center"><Activity className="w-3 h-3 mr-1 animate-pulse" /> Scanning...</span> : <span className="text-muted-foreground ml-1 capitalize">{scanStatus}</span>}
          </Badge>
          <Badge variant="outline" className="px-3 py-1.5 text-sm h-9 bg-card">
            Selected: <span className="text-foreground font-medium ml-1">{selectedProvider}</span>
          </Badge>

          <div className="h-9 w-px bg-border mx-1 hidden sm:block"></div>

          {scanStatus !== 'scanning' ? (
            <>
              <Button onClick={() => startScan(selectedProvider)} className="gap-2 bg-primary">
                <PlayCircle className="h-4 w-4" /> Start Scan
              </Button>
              <Button onClick={refreshScan} variant="outline" className="gap-2" disabled={scanStatus === 'scanning'}>
                <RefreshCcw className="h-4 w-4" /> Refresh
              </Button>
            </>
          ) : (
            <Button onClick={stopScan} variant="destructive" className="gap-2">
              <StopCircle className="h-4 w-4" /> Stop Scan
            </Button>
          )}
        </div>
      </div>

      {scanStatus === 'scanning' && (
        <Card className="border-primary/20 bg-primary/5">
          <CardContent className="pt-6 pb-6">
            <div className="flex flex-col items-center justify-center space-y-4">
              <div className="flex items-center gap-3">
                <Search className="h-6 w-6 text-primary animate-pulse" />
                <h3 className="text-lg font-medium text-primary">Searching for {selectedProvider === 'All' ? 'all providers' : selectedProvider}...</h3>
              </div>
              <div className="w-full max-w-xl space-y-2">
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Scanning network interfaces</span>
                  <span>{elapsed / 10}s elapsed</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <div>
        <h2 className="text-xl font-semibold mb-4">Available Providers</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {providers.map(provider => (
            <Card key={provider.id} className={`transition-all hover:border-primary/50 cursor-pointer ${selectedProvider === provider.type ? 'ring-2 ring-primary border-primary' : ''}`} onClick={() => setSelectedProvider(provider.type)}>
              <CardHeader className="pb-3 flex flex-row items-start justify-between space-y-0">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${provider.status === 'active' ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'}`}>
                    {getProviderIcon(provider.type)}
                  </div>
                  <div>
                    <CardTitle className="text-base">{provider.name}</CardTitle>
                    <Badge variant={provider.status === 'active' ? 'default' : 'secondary'} className={provider.status === 'active' ? 'bg-green-500/10 text-green-500 hover:bg-green-500/20 mt-1 font-normal' : 'mt-1 font-normal'}>
                      {provider.status}
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pb-4">
                <p className="text-sm text-muted-foreground line-clamp-2 min-h-[40px]">
                  {provider.description}
                </p>
                <div className="mt-4 space-y-2">
                  <span className="text-xs text-muted-foreground">Supported Capabilities</span>
                  <div className="flex flex-wrap gap-1.5">
                    {provider.supportedCapabilities.map(cap => (
                      <span key={cap} className="text-[10px] bg-secondary px-1.5 py-0.5 rounded-sm border">
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>
              </CardContent>
              <CardFooter className="pt-0 pb-4">
                <Button variant="secondary" className="w-full text-xs h-8" onClick={(e) => { e.stopPropagation(); startScan(provider.type); }} disabled={scanStatus === 'scanning'}>
                  <Search className="h-3.5 w-3.5 mr-2" />
                  Scan {provider.type}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>

      {(scanStatus === 'complete' || results.length > 0) && (
        <div className="pt-4 border-t">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Discovery Results</h2>
            <Badge variant="secondary" className="font-normal">{results.length} devices found</Badge>
          </div>
          
          {results.length === 0 ? (
            <Card className="flex flex-col items-center justify-center py-12 text-center border-dashed">
              <div className="bg-muted p-3 rounded-full mb-3">
                <XCircle className="h-6 w-6 text-muted-foreground" />
              </div>
              <h3 className="text-base font-medium">No devices discovered</h3>
              <p className="text-sm text-muted-foreground max-w-sm mt-1 mb-4">
                We couldn't find any unregistered {selectedProvider !== 'All' ? selectedProvider : ''} devices on the network.
              </p>
              <Button variant="outline" onClick={() => startScan(selectedProvider)} size="sm">
                Try Again
              </Button>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {results.map(result => (
                <Card key={result.id} className="overflow-hidden">
                  <CardHeader className="bg-muted/30 pb-3 border-b">
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-base font-medium">{result.name}</CardTitle>
                        <div className="flex items-center gap-1.5 mt-1.5 text-xs text-muted-foreground">
                          {getProviderIcon(result.provider)}
                          <span>{result.provider}</span>
                        </div>
                      </div>
                      <Badge variant="outline" className="bg-background text-[10px] font-mono">
                        {result.mac}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-4 pb-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-xs text-muted-foreground block mb-1">IP Address</span>
                        <span className="font-mono">{result.ip}</span>
                      </div>
                      <div>
                        <span className="text-xs text-muted-foreground block mb-1">Signal</span>
                        <span>{result.signal}</span>
                      </div>
                    </div>
                    <div className="mt-4">
                      <span className="text-xs text-muted-foreground block mb-2">Capabilities</span>
                      <div className="flex flex-wrap gap-1.5">
                        {result.capabilities.map(cap => (
                          <span key={cap} className="text-[10px] bg-primary/10 text-primary px-1.5 py-0.5 rounded-sm">
                            {cap}
                          </span>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="pt-3 pb-3 border-t flex justify-between items-center bg-muted/10">
                    <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                      <Clock className="h-3.5 w-3.5" />
                      {result.discoveredTime}
                    </div>
                    <Button size="sm" className="h-8 text-xs gap-1.5" onClick={() => registerDeviceMutation.mutate(result)} disabled={registerDeviceMutation.isPending}>
                      <Plus className="h-3.5 w-3.5" />
                      Register
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
