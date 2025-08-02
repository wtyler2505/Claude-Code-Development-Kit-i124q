import { PostEditPayload } from './lib'
import { exec } from 'child_process'
export default async function postEdit(payload: PostEditPayload){
  if(payload.success){
    exec('gh workflow run CCDK CI -F ref=$(git rev-parse --abbrev-ref HEAD)')
  }
}
