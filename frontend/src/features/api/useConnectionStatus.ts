import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface ConnectResponse {
  ok: boolean;
  message: string;
}

export function useConnectionStatus() {
  return useQuery({
    queryKey: ['api-connect'],
    queryFn: async () => {
      const { data } = await api.get<ConnectResponse>('/api/v1/connect');
      return data;
    },
    refetchInterval: 30000, // Check every 30 seconds
    retry: 2,
  });
}
