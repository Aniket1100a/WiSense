import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { ApiResponse, SensorResponse } from '@/types/backend';
import { SensorDevice } from '@/types/api';

// Transform backend SensorResponse to frontend SensorDevice
export const transformSensor = (s: SensorResponse): SensorDevice => {
  return {
    id: s.id,
    name: s.name || 'Unknown',
    status: (s.status?.toLowerCase() as any) || 'offline',
    type: (s.provider?.toUpperCase() as any) || 'ESP32', // Fallback mapping
    provider: s.provider || 'Unknown',
    firmware: s.firmware_version || 'N/A',
    hardwareVersion: s.hardware_version || 'N/A',
    lastSeen: s.updated_at ? new Date(s.updated_at).toLocaleString() : 'Unknown',
    room: s.location || 'Unknown',
    capabilities: s.meta?.capabilities || ['CSI'],
    health: s.meta?.health ?? 100,
    battery: s.meta?.battery ?? 100,
    signalQuality: s.meta?.signalQuality ?? '-50 dBm',
    connectionType: s.meta?.connectionType ?? 'WiFi',
    samplingState: s.meta?.samplingState ?? 'idle',
    providerVersion: s.meta?.providerVersion ?? 'v1.0',
    aiStatus: s.meta?.aiStatus ?? 'inactive',
  };
};

export function useSensors() {
  return useQuery({
    queryKey: ['sensors'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiResponse<SensorResponse[]>>('/api/v1/sensors/');
        if (!data.success && !data.data) throw new Error(data.message);
        return (data.data || []).map(transformSensor);
      } catch (error) {
        console.error("Failed to fetch sensors", error);
        throw error;
      }
    },
  });
}

export function useSensor(id: string) {
  return useQuery({
    queryKey: ['sensor', id],
    queryFn: async () => {
      const { data } = await api.get<ApiResponse<SensorResponse>>(`/api/v1/sensors/${id}`);
      return transformSensor(data.data);
    },
    enabled: !!id,
  });
}

export function useDisconnectSensor() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data } = await api.post(`/api/v1/sensors/disconnect`, { sensor_id: id });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sensors'] });
    },
  });
}
