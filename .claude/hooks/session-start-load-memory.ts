import { SessionStartPayload, HookResponse } from './lib'
import Database from 'better-sqlite3'
import fs from 'fs'

export default async function sessionStart(payload: SessionStartPayload): Promise<HookResponse> {
  const dbPath = '.ccd_memory.db'
  if (fs.existsSync(dbPath)) {
    const db = new Database(dbPath)
    try {
      // Ensure table exists
      db.exec('CREATE TABLE IF NOT EXISTS memory(ts INTEGER, content TEXT)')
      const rows = db.prepare('SELECT content FROM memory ORDER BY ts DESC LIMIT 20').all()
      const mem = rows.map((r: any) => r.content).join('\n')
      db.close()
      return { action: 'continue', message: `Loaded ${rows.length} memories` }
    } catch (error) {
      db.close()
      // If error, just continue without loading memory
      return { action: 'continue' }
    }
  }
  return { action: 'continue' }
}
