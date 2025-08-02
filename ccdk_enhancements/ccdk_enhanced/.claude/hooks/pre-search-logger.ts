import { PreSearchPayload, HookResponse } from './lib'
export default async function preSearch(payload: PreSearchPayload): Promise<HookResponse> {
  console.log('Search terms:', payload.query)
  return { action: 'continue' }
}
