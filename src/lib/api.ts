const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  isFallbackDemo?: boolean;
}

export async function apiClient<T>(
  endpoint: string, 
  options?: RequestInit, 
  fallbackData?: T
): Promise<ApiResponse<T>> {
  const url = `${BASE_URL.replace(/\/$/, "")}/${endpoint.replace(/^\//, "")}`;

  try {
    const token = typeof window !== "undefined" ? localStorage.getItem("elevate_auth_token") : null;
    
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options?.headers as Record<string, string> || {}),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    // Allow up to 30s timeout so neural model inference (MPS / CPU) can complete comfortably
    const timeoutMs = (options as any)?.timeout || 30000;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    const response = await fetch(url, {
      ...options,
      headers,
      signal: options?.signal || controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return { data, success: true, isFallbackDemo: false };
  } catch (error) {
    if (fallbackData !== undefined) {
      return {
        data: fallbackData,
        success: true,
        message: "Operating in demo mode with verified sample dataset.",
        isFallbackDemo: true,
      };
    }
    throw error;
  }
}
