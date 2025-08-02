import { PostTaskPayload } from './lib'
import fs from 'fs'

export default async function postTask(payload: PostTaskPayload) {
  const summary = `Task ${payload.task_name} completed in ${payload.duration_ms}ms\n`
  fs.appendFileSync('.task_log', summary)
}
