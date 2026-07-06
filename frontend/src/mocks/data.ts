export const mockKPIs = {
  activeDevices: 124,
  occupancy: 42,
  alertsToday: 12,
  aiConfidence: 98.4,
};

export const mockDeviceStats = [
  { name: 'Jan', offline: 12, online: 100 },
  { name: 'Feb', offline: 8, online: 110 },
  { name: 'Mar', offline: 15, online: 105 },
  { name: 'Apr', offline: 5, online: 120 },
  { name: 'May', offline: 2, online: 124 },
];

export const mockOccupancyTrend = [
  { time: '08:00', users: 5 },
  { time: '09:00', users: 15 },
  { time: '10:00', users: 32 },
  { time: '11:00', users: 40 },
  { time: '12:00', users: 42 },
  { time: '13:00', users: 38 },
  { time: '14:00', users: 35 },
];

export const mockDevices = [
  { id: 'dev-001', name: 'Lobby Sensor Alpha', status: 'online', type: 'WiFi CSI', location: 'Main Lobby', firmware: 'v2.1.0', lastSeen: 'Just now' },
  { id: 'dev-002', name: 'Conf Room Beta', status: 'online', type: 'WiFi CSI', location: 'Room 302', firmware: 'v2.1.0', lastSeen: '2m ago' },
  { id: 'dev-003', name: 'Hallway Node', status: 'offline', type: 'BLE/WiFi', location: 'East Wing', firmware: 'v2.0.4', lastSeen: '2h ago' },
  { id: 'dev-004', name: 'Cafeteria Main', status: 'warning', type: 'WiFi CSI', location: 'Cafeteria', firmware: 'v2.1.0', lastSeen: '15m ago' },
  { id: 'dev-005', name: 'Executive Suite', status: 'online', type: 'WiFi CSI', location: 'Floor 5', firmware: 'v2.1.0', lastSeen: '1m ago' },
];

export const mockAlerts = [
  { id: 'alert-1', type: 'critical', title: 'Device Offline', message: 'Hallway Node has been offline for > 2 hours.', time: '2 hours ago' },
  { id: 'alert-2', type: 'warning', title: 'High Occupancy', message: 'Main Lobby exceeded threshold capacity (50).', time: '4 hours ago' },
  { id: 'alert-3', type: 'info', title: 'Model Updated', message: 'Human Presence Model v4.2 deployed successfully.', time: '1 day ago' },
];

export const mockModels = [
  { id: 'model-1', name: 'Human Presence v4', accuracy: 98.4, status: 'Active', latency: '45ms', updated: '2023-10-15' },
  { id: 'model-2', name: 'Fall Detection v2', accuracy: 94.2, status: 'Testing', latency: '60ms', updated: '2023-11-02' },
  { id: 'model-3', name: 'Crowd Count v1', accuracy: 89.1, status: 'Draft', latency: '120ms', updated: '2023-11-10' },
];
