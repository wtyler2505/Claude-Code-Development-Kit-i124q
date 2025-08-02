import { NotificationPayload } from './lib'
import { exec } from 'child_process'
export default async function notification(payload: NotificationPayload){
  const msg = payload.title || 'Claude notification'
  exec(`(which say && say "${msg}") || (which espeak && espeak "${msg}") || true`)
}
