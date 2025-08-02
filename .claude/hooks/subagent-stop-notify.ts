import { SubagentPayload, HookResponse } from './lib'
export default async function subagentStop(payload: SubagentPayload): Promise<HookResponse> {
  console.log(`Subagent ${payload.agent_id} stopped${payload.reason ? ': ' + payload.reason : ''}`)
  return { action: 'continue' }
}
