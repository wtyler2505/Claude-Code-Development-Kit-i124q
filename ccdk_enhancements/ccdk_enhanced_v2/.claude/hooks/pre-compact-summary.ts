import { PreCompactPayload, HookResponse } from './lib'
export default async function preCompact(payload: PreCompactPayload): Promise<HookResponse> {
  const fs = await import('fs')
  fs.appendFileSync('.session_summary', `\n---\nSummary before compact: ${payload.summary}\n`)
  return { action: 'continue' }
}
