import { SessionEndPayload } from './lib'
import Database from 'better-sqlite3'
export default async function sessionEnd(payload: SessionEndPayload) {
  const db = new Database('.ccd_memory.db')
  db.exec('CREATE TABLE IF NOT EXISTS memory(ts INTEGER, content TEXT)')
  db.prepare('INSERT INTO memory(ts,content) VALUES (?,?)').run(Date.now(), payload.summary)
}
