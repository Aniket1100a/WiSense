import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { ApiResponse } from '@/types/backend';
import { ProviderInfo, DiscoveryResult } from '@/types/api';

export function useProviders() {
  return useQuery({
    queryKey: ['discovery-providers'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiResponse<string[]>>('/api/v1/discovery/providers');
        const providers: ProviderInfo[] = (data.data || []).map(p => ({
          id: p,
          type: (p === 'esp32' ? 'ESP32' : p === 'usb_adapter' ? 'USB Adapter' : p === 'dataset' ? 'Dataset' : p === 'simulator' ? 'Simulator' : p.includes('linux') || p.includes('windows') ? 'Laptop' : 'Intel CSI') as any,
          name: p.replace('_', ' ').toUpperCase(),
          description: `Provider for ${p}`,
          status: 'active',
          supportedCapabilities: ['CSI'],
        }));
        return providers;
      } catch (error) {
        console.error("Failed to fetch providers", error);
        throw error;
      }
    },
  });
}

export function useStartDiscovery() {
  return useMutation({
    mutationFn: async (provider: string) => {
      const { data } = await api.post(`/api/v1/discovery/start`, { provider: provider === 'All' ? 'all' : provider });
      const sensors = data?.data?.sensors || [];
      return sensors.map((s: any) => ({
        id: s.serial_number || Math.random().toString(),
        name: s.name,
        provider: (s.provider === 'esp32' ? 'ESP32' : s.provider === 'usb_adapter' ? 'USB Adapter' : s.provider === 'dataset' ? 'Dataset' : s.provider === 'simulator' ? 'Simulator' : s.provider.includes('linux') || s.provider.includes('windows') ? 'Laptop' : 'Intel CSI'),
        mac: s.mac_address || 'N/A',
        ip: s.ip_address || 'Unknown',
        capabilities: s.metadata?.capabilities || ['CSI'],
        signal: s.metadata?.signal || 'N/A',
        discoveredTime: 'Just now'
      })) as DiscoveryResult[];
    },
  });
}

export function useDiscoveryResults() {
  // Not strictly needed if start mutation returns them, but kept for compatibility
  return useQuery({
    queryKey: ['discovery-results'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiResponse<any[]>>('/api/v1/discovery/results');
        return data.data || [];
      } catch (error) {
        console.error("Failed to fetch discovery results", error);
        throw error;
      }
    },
    refetchInterval: 5000,
  });
}

export function useRegisterDevice() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (device: any) => {
      const { data } = await api.post(`/api/v1/discovery/register`, device);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sensors'] });
      queryClient.invalidateQueries({ queryKey: ['discovery-results'] });
    },
  });
}
