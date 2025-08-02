import { ToolUsePayload, HookResponse } from './lib'
export default async function postToolUse(payload: ToolUsePayload): Promise<HookResponse> {
  if (payload.tool === 'Write' || payload.tool === 'Edit') {
    const { exec } = await import('child_process')
    exec('npm run lint --silent', () => {})
  }
  return { action: 'continue' }
}
