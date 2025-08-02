import { SubagentStopPayload } from './lib'
export default async function subagentStop(payload: SubagentStopPayload) {
  console.log(`Subagent ${payload.subagent_name} finished with status: ${payload.status}`)
}
