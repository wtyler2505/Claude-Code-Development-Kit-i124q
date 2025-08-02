import { EditPayload, HookResponse } from './lib'
import { exec } from 'child_process'
export default async function postEdit(payload: EditPayload): Promise<HookResponse> {
  // Only run CI if we have gh CLI available
  exec('gh --version', (error) => {
    if (!error) {
      exec('gh workflow run CCDK CI -F ref=$(git rev-parse --abbrev-ref HEAD)', () => {})
    }
  })
  return { action: 'continue' }
}
