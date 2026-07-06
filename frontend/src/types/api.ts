export type DeviceStatus = 'online' | 'offline' | 'error' | 'warning';
export type DeviceType = 'ESP32' | 'Laptop' | 'USB Adapter' | 'Dataset' | 'Simulator' | 'Intel CSI';
export type ProviderType = 'ESP32' | 'Laptop' | 'USB Adapter' | 'Dataset' | 'Simulator' | 'Intel CSI';

export interface SensorDevice {
  id: string;
  name: string;
  status: DeviceStatus;
  type: DeviceType;
  provider: string;
  firmware: string;
  hardwareVersion: string;
  lastSeen: string;
  room: string;
  capabilities: string[];
  health: number;
  battery: number;
  signalQuality: string;
  connectionType: string;
  samplingState: 'active' | 'idle' | 'error';
  providerVersion: string;
  aiStatus: 'active' | 'inactive' | 'training';
}

export interface ProviderDistribution {
  name: string;
  value: number;
}

export interface StatusDistribution {
  name: string;
  value: number;
}

export interface DashboardOverview {
  totalSensors: number;
  activeSensors: number;
  activeSensorsChange: string;
  totalAlerts: number;
  avgSignalQuality: string;
  aiModelsActive: number;
}

export interface DeviceHealthData {
  time: string;
  health: number;
}

export interface SignalHistoryData {
  time: string;
  value: number;
}

export interface ProviderInfo {
  id: string;
  type: ProviderType;
  name: string;
  description: string;
  status: 'active' | 'inactive' | 'error';
  supportedCapabilities: string[];
}

export interface DiscoveryResult {
  id: string;
  name: string;
  provider: ProviderType;
  mac: string;
  ip: string;
  capabilities: string[];
  signal: string;
  discoveredTime: string;
}
