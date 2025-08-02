import { SessionStartPayload, HookResponse } from './lib'
import Database from 'better-sqlite3'
import fs from 'fs'

export default async function sessionStart(payload: SessionStartPayload): Promise<HookResponse> {
  const dbPath = '.ccd_memory.db'
  if (fs.existsSync(dbPath)) {
    const db = new Database(dbPath)
    const rows = db.prepare('SELECT content FROM memory ORDER BY ts DESC LIMIT 20').all()
    const mem = rows.map(r=>r.content).join('\n')
    return { action: 'inject_context', context: mem }
  }
  return { action: 'continue' }
}
