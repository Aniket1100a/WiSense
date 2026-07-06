import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, Plus, MoreHorizontal, Activity, Signal, Wifi, Cpu, Laptop as LaptopIcon, Usb, Database, Box, AlertCircle, RefreshCcw } from 'lucide-react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { DeviceStatus, DeviceType } from '@/types/api';
import { useSensors } from '@/hooks/useSensors';

const getTypeIcon = (type: DeviceType) => {
  switch (type) {
    case 'ESP32': return <Cpu className="h-4 w-4" />;
    case 'Laptop': return <LaptopIcon className="h-4 w-4" />;
    case 'USB Adapter': return <Usb className="h-4 w-4" />;
    case 'Dataset': return <Database className="h-4 w-4" />;
    case 'Simulator': return <Box className="h-4 w-4" />;
    default: return <Wifi className="h-4 w-4" />;
  }
};

const getStatusColor = (status: DeviceStatus) => {
  switch (status) {
    case 'online': return 'bg-green-500/10 text-green-500 border-green-500/20';
    case 'offline': return 'bg-muted text-muted-foreground border-border';
    case 'warning': return 'bg-amber-500/10 text-amber-500 border-amber-500/20';
    case 'error': return 'bg-destructive/10 text-destructive border-destructive/20';
    default: return 'bg-muted text-muted-foreground border-border';
  }
};

const getStatusDot = (status: DeviceStatus) => {
  switch (status) {
    case 'online': return 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]';
    case 'offline': return 'bg-muted-foreground';
    case 'warning': return 'bg-amber-500';
    case 'error': return 'bg-destructive animate-pulse';
    default: return 'bg-muted-foreground';
  }
};

export default function DevicesPage() {
  const [search, setSearch] = useState('');
  const { data: devices, isLoading, isError, refetch } = useSensors();
  
  // viewState logic handled dynamically
  const viewState = isLoading ? 'loading' : isError ? 'error' : (!devices || devices.length === 0) ? 'empty' : 'ready';

  const [statusFilter, setStatusFilter] = useState('');
  const [providerFilter, setProviderFilter] = useState('');
  const [roomFilter, setRoomFilter] = useState('');
  const [capabilityFilter, setCapabilityFilter] = useState('');

  // Filter logic
  const filteredDevices = (devices || []).filter(device => {
    const matchesSearch = 
      device.name.toLowerCase().includes(search.toLowerCase()) || 
      device.id.toLowerCase().includes(search.toLowerCase()) ||
      device.type.toLowerCase().includes(search.toLowerCase()) ||
      device.room.toLowerCase().includes(search.toLowerCase());
    
    const matchesStatus = statusFilter === '' || device.status === statusFilter;
    const matchesProvider = providerFilter === '' || device.provider === providerFilter;
    const matchesRoom = roomFilter === '' || device.room === roomFilter;
    const matchesCapability = capabilityFilter === '' || device.capabilities.includes(capabilityFilter);

    return matchesSearch && matchesStatus && matchesProvider && matchesRoom && matchesCapability;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Device Management</h1>
          <p className="text-muted-foreground mt-2">
            Manage your WiFi sensing nodes, virtual devices, and datasets.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button className="gap-2">
            <Plus className="h-4 w-4" /> Add Device
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4 mb-6">
        <div className="flex items-center justify-between">
          <div className="relative w-full max-w-sm">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search devices, types, or rooms..."
              className="pl-8 bg-card"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
        
        <div className="flex flex-wrap gap-2 text-sm">
          {/* Filters */}
          <select 
            className="bg-card border rounded-md px-3 py-1.5 text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All Statuses</option>
            <option value="online">Online</option>
            <option value="offline">Offline</option>
            <option value="warning">Warning</option>
            <option value="error">Error</option>
          </select>
          <select 
            className="bg-card border rounded-md px-3 py-1.5 text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            value={providerFilter}
            onChange={(e) => setProviderFilter(e.target.value)}
          >
            <option value="">All Providers</option>
            <option value="Espressif">Espressif</option>
            <option value="Intel">Intel</option>
            <option value="Realtek">Realtek</option>
            <option value="Internal Storage">Internal Storage</option>
            <option value="SensingEngine">SensingEngine</option>
          </select>
          <select 
            className="bg-card border rounded-md px-3 py-1.5 text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            value={roomFilter}
            onChange={(e) => setRoomFilter(e.target.value)}
          >
            <option value="">All Rooms</option>
            <option value="Main Lobby">Main Lobby</option>
            <option value="Room 302">Room 302</option>
            <option value="East Wing">East Wing</option>
            <option value="Cafeteria">Cafeteria</option>
            <option value="Cloud">Cloud</option>
            <option value="Virtual Space A">Virtual Space A</option>
            <option value="Exec Boardroom">Exec Boardroom</option>
          </select>
          <select 
            className="bg-card border rounded-md px-3 py-1.5 text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            value={capabilityFilter}
            onChange={(e) => setCapabilityFilter(e.target.value)}
          >
            <option value="">All Capabilities</option>
            <option value="CSI">CSI</option>
            <option value="BLE">BLE</option>
            <option value="Occupancy">Occupancy</option>
            <option value="Compute">Compute</option>
            <option value="Replay">Replay</option>
            <option value="Training">Training</option>
            <option value="High-Res">High-Res</option>
          </select>
        </div>
      </div>

      {viewState === 'loading' && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map(i => (
            <Card key={i} className="overflow-hidden">
              <CardHeader className="pb-4">
                <div className="flex justify-between items-start">
                  <div className="space-y-2">
                    <Skeleton className="h-5 w-32" />
                    <Skeleton className="h-4 w-20" />
                  </div>
                  <Skeleton className="h-8 w-8 rounded-full" />
                </div>
              </CardHeader>
              <CardContent className="pb-2 space-y-4">
                <div className="flex gap-2">
                  <Skeleton className="h-6 w-16 rounded-full" />
                  <Skeleton className="h-6 w-16 rounded-full" />
                </div>
                <div className="space-y-2">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-4/5" />
                  <Skeleton className="h-4 w-full" />
                </div>
              </CardContent>
              <CardFooter className="pt-4 border-t bg-muted/20">
                <Skeleton className="h-4 w-24" />
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      {viewState === 'error' && (
        <Card className="border-destructive/20 bg-destructive/5 flex flex-col items-center justify-center py-16 text-center">
          <AlertCircle className="h-10 w-10 text-destructive mb-4" />
          <h3 className="text-lg font-medium">Failed to load devices</h3>
          <p className="text-muted-foreground max-w-sm mt-2 mb-6">
            We encountered an error while communicating with the device registry. Please check your connection and try again.
          </p>
          <Button variant="outline" onClick={() => refetch()}>
            <RefreshCcw className="mr-2 h-4 w-4" />
            Retry Connection
          </Button>
        </Card>
      )}

      {viewState === 'empty' || (viewState === 'ready' && filteredDevices.length === 0) ? (
        <Card className="flex flex-col items-center justify-center py-16 text-center border-dashed">
          <div className="bg-primary/10 p-4 rounded-full mb-4">
            <Wifi className="h-8 w-8 text-primary" />
          </div>
          <h3 className="text-lg font-medium">No devices found</h3>
          <p className="text-muted-foreground max-w-sm mt-2 mb-6">
            {search ? `No devices match your search for "${search}".` : "You haven't added any devices to your network yet."}
          </p>
          {search ? (
            <Button variant="outline" onClick={() => setSearch('')}>Clear Search</Button>
          ) : (
            <Button>
              <Plus className="mr-2 h-4 w-4" /> Add Your First Device
            </Button>
          )}
        </Card>
      ) : null}

      {viewState === 'ready' && filteredDevices.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredDevices.map((device) => (
            <Card key={device.id} className="flex flex-col transition-all hover:shadow-md hover:border-primary/20">
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <div className={`w-2 h-2 rounded-full ${getStatusDot(device.status)}`} />
                      <CardTitle className="text-base">{device.name}</CardTitle>
                    </div>
                    <CardDescription className="font-mono text-xs">{device.id}</CardDescription>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger render={<Button variant="ghost" className="h-8 w-8 p-0" />}>
                      <span className="sr-only">Open menu</span>
                      <MoreHorizontal className="h-4 w-4" />
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Connect</DropdownMenuItem>
                      <DropdownMenuItem>Disconnect</DropdownMenuItem>
                      <DropdownMenuItem>Start Capture</DropdownMenuItem>
                      <DropdownMenuItem>Stop Capture</DropdownMenuItem>
                      <DropdownMenuItem>Open Live Monitor</DropdownMenuItem>
                      <DropdownMenuItem>Configure</DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">Restart</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </CardHeader>
              
              <CardContent className="pb-4 flex-1">
                <div className="flex flex-wrap gap-2 mb-5">
                  <Badge variant="outline" className={`gap-1 font-normal ${getStatusColor(device.status)}`}>
                    <span className="capitalize">{device.status}</span>
                  </Badge>
                  <Badge variant="secondary" className="gap-1 font-normal">
                    {getTypeIcon(device.type)}
                    {device.type}
                  </Badge>
                  <Badge variant="outline" className="font-normal text-muted-foreground">
                    {device.connectionType}
                  </Badge>
                </div>
                
                <div className="grid grid-cols-2 gap-y-4 gap-x-2 text-sm">
                  <div>
                    <span className="text-muted-foreground text-xs block mb-1">Room</span>
                    <span className="font-medium truncate block" title={device.room}>{device.room}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground text-xs block mb-1">Provider</span>
                    <span className="truncate block" title={device.provider}>{device.provider}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground text-xs block mb-1">Firmware</span>
                    <span className="truncate block" title={device.firmware}>{device.firmware}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground text-xs block mb-1">Hardware</span>
                    <span className="truncate block" title={device.hardwareVersion}>{device.hardwareVersion}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground text-xs block mb-1">Sampling State</span>
                    <span className="truncate block capitalize" title={device.samplingState}>{device.samplingState}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground text-xs block mb-1">Signal Quality</span>
                    <div className="flex items-center gap-1.5">
                      <Signal className="h-3 w-3 text-muted-foreground" />
                      <span>{device.signalQuality}</span>
                    </div>
                  </div>
                  <div>
                    <span className="text-muted-foreground text-xs block mb-1">AI Status</span>
                    <span className="truncate block capitalize" title={device.aiStatus}>{device.aiStatus}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground text-xs block mb-1">Provider Version</span>
                    <span className="truncate block" title={device.providerVersion}>{device.providerVersion}</span>
                  </div>
                </div>

                <div className="mt-5 space-y-3">
                  <div>
                    <div className="flex justify-between text-xs mb-1.5">
                      <span className="text-muted-foreground">Health / Battery</span>
                      <span className="font-medium">{device.health}% / {device.battery}%</span>
                    </div>
                    <Progress value={device.health} className="h-1.5 mb-1" />
                    <Progress value={device.battery} className="h-1.5 bg-secondary [&>div]:bg-amber-500" />
                  </div>
                  
                  <div>
                    <span className="text-muted-foreground text-xs block mb-2">Capabilities</span>
                    <div className="flex flex-wrap gap-1.5">
                      {device.capabilities.map(cap => (
                        <span key={cap} className="text-[10px] bg-secondary px-1.5 py-0.5 rounded-sm border">
                          {cap}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
              
              <CardFooter className="pt-3 pb-3 border-t bg-muted/10 text-xs text-muted-foreground flex justify-between items-center mt-auto">
                <div className="flex items-center gap-1.5">
                  <Activity className="h-3.5 w-3.5" />
                  Last seen: {device.lastSeen}
                </div>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
