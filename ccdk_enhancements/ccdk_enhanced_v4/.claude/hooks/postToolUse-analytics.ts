import { PostToolUsePayload } from './lib'
import fs from 'fs'
export default async function postToolUse(payload: PostToolUsePayload){
  const entry = {ts:Date.now(), tool:payload.tool_name, success:payload.success}
  fs.appendFileSync('.ccd_analytics.log', JSON.stringify(entry)+"\n")
}
