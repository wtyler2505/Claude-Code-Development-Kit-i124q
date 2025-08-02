import { PostToolUsePayload } from './lib'
export default async function postToolUse(payload: PostToolUsePayload) {
  if (payload.tool_name === 'Write' && payload.success) {
    const { exec } = await import('child_process')
    exec('npm run lint --silent')
  }
}
