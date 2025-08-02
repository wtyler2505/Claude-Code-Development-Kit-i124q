import { SessionStartPayload, HookResponse } from './lib'
import Database from 'better-sqlite3'

const db = new Database(process.cwd() + '/.ccd_memory.db')
db.prepare('CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY,start INTEGER)').run()

export default async function sessionStart(payload: SessionStartPayload): Promise<HookResponse> {
  db.prepare('INSERT OR IGNORE INTO sessions(id,start) VALUES (?,?)').run(payload.session_id, Date.now())
  return { action: 'continue' }
}
