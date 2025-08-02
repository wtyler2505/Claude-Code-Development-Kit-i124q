// Hook type definitions for CCDK Enhancement Kits

export interface SessionStartPayload {
  session_id: string;
  timestamp: number;
  project_path?: string;
}

export interface SessionEndPayload {
  session_id: string;
  timestamp: number;
  duration?: number;
}

export interface TaskPayload {
  session_id: string;
  task: string;
  result?: any;
  timestamp: number;
}

export interface SearchPayload {
  session_id: string;
  query: string;
  files?: string[];
  timestamp: number;
}

export interface ToolUsePayload {
  session_id: string;
  tool: string;
  params?: any;
  result?: any;
  timestamp: number;
}

export interface EditPayload {
  session_id: string;
  file: string;
  changes?: any;
  timestamp: number;
}

export interface CompactPayload {
  session_id: string;
  summary?: string;
  timestamp: number;
}

export interface SubagentPayload {
  session_id: string;
  agent_id: string;
  reason?: string;
  timestamp: number;
}

export interface HookResponse {
  action: 'continue' | 'stop' | 'modify';
  message?: string;
  modifications?: any;
}

// Default hook response
export const continueResponse: HookResponse = { action: 'continue' };