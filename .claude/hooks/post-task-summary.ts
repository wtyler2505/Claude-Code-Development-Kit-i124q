import { TaskPayload, HookResponse } from './lib'
import fs from 'fs'

export default async function postTask(payload: TaskPayload): Promise<HookResponse> {
  const summary = `Task completed at ${new Date(payload.timestamp).toISOString()}\n`
  fs.appendFileSync('.task_log', summary)
  return { action: 'continue' }
}
