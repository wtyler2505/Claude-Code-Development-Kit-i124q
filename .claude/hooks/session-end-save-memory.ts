import { SessionEndPayload, HookResponse } from './lib'
import Database from 'better-sqlite3'
export default async function sessionEnd(payload: SessionEndPayload): Promise<HookResponse> {
  const db = new Database('.ccd_memory.db')
  db.exec('CREATE TABLE IF NOT EXISTS memory(ts INTEGER, content TEXT)')
  const summary = `Session ${payload.session_id} ended after ${payload.duration || 0}ms`
  db.prepare('INSERT INTO memory(ts,content) VALUES (?,?)').run(Date.now(), summary)
  db.close()
  return { action: 'continue' }
}
