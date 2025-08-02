import { PostToolUsePayload, HookResponse } from './lib'
export default async function postToolUse(payload: PostToolUsePayload): Promise<HookResponse>{
  if(payload.success && payload.output){
    return { action:'inject_context', context:`Tool ${payload.tool_name} output:\n${payload.output}` }
  }
  return { action:'continue'}
}
