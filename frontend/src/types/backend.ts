export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  pagination: any;
  errors: any;
}

export interface SensorResponse {
  id: string;
  name: string;
  description: string | null;
  provider: string;
  sensor_type: string;
  status: 'ONLINE' | 'OFFLINE' | 'CONNECTING' | 'ERROR' | 'DISABLED';
  firmware_version: string | null;
  hardware_version: string | null;
  serial_number: string | null;
  mac_address: string | null;
  ip_address: string | null;
  location: string | null;
  room_id: string | null;
  is_active: boolean;
  meta: any;
  created_at: string;
  updated_at: string;
}

export interface RoomResponse {
  id: string;
  name: string;
  description: string | null;
}

export interface CapabilityResponse {
  id: string;
  name: string;
}
