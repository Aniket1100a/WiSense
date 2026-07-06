import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { ApiResponse } from '@/types/backend';
import { DashboardOverview, DeviceHealthData, ProviderDistribution, StatusDistribution, SignalHistoryData } from '@/types/api';

export function useDashboardOverview() {
  return useQuery({
    queryKey: ['dashboard-overview'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiResponse<DashboardOverview>>('/api/v1/dashboard/overview');
        return data.data;
      } catch (error: any) {
        if (error?.response?.status === 405 || error?.response?.status === 404) {
          return null; // Not implemented yet
        }
        throw error;
      }
    },
    retry: 1,
  });
}

export function useDashboardDeviceHealth() {
  return useQuery({
    queryKey: ['dashboard-device-health'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiResponse<DeviceHealthData[]>>('/api/v1/dashboard/device-health');
        return data.data;
      } catch (error: any) {
        if (error?.response?.status === 405 || error?.response?.status === 404) {
          return null;
        }
        throw error;
      }
    },
    retry: 1,
  });
}

export function useDashboardProviderDistribution() {
  return useQuery({
    queryKey: ['dashboard-provider-distribution'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiResponse<ProviderDistribution[]>>('/api/v1/dashboard/provider-distribution');
        return data.data;
      } catch (error: any) {
        if (error?.response?.status === 405 || error?.response?.status === 404) {
          return null;
        }
        throw error;
      }
    },
    retry: 1,
  });
}

export function useDashboardStatusDistribution() {
  return useQuery({
    queryKey: ['dashboard-status-distribution'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiResponse<StatusDistribution[]>>('/api/v1/dashboard/status-distribution');
        return data.data;
      } catch (error: any) {
        if (error?.response?.status === 405 || error?.response?.status === 404) {
          return null;
        }
        throw error;
      }
    },
    retry: 1,
  });
}

export function useDashboardSignalHistory() {
  return useQuery({
    queryKey: ['dashboard-signal-history'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiResponse<SignalHistoryData[]>>('/api/v1/dashboard/signal-history');
        return data.data;
      } catch (error: any) {
        if (error?.response?.status === 405 || error?.response?.status === 404) {
          return null;
        }
        throw error;
      }
    },
    retry: 1,
  });
}
