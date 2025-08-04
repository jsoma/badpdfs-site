import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)
const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Source and destination paths
const artifactsSource = path.join(__dirname, '..', '..', 'artifacts')
const artifactsDest = path.join(__dirname, '..', 'public', 'artifacts')

// Function to copy artifacts
async function copyArtifacts() {
  try {
    console.log('📁 Copying artifacts...')
    await execAsync(`node ${path.join(__dirname, 'copy-artifacts.js')}`)
    console.log('✅ Artifacts copied successfully')
  } catch (error) {
    console.error('❌ Error copying artifacts:', error)
  }
}

// Initial copy
await copyArtifacts()

// Watch for changes
console.log(`👀 Watching for changes in ${artifactsSource}...`)

fs.watch(artifactsSource, { recursive: true }, async (eventType, filename) => {
  if (filename) {
    console.log(`📝 Detected ${eventType} in ${filename}`)
    await copyArtifacts()
  }
})

// Keep the process running
process.on('SIGINT', () => {
  console.log('\n👋 Stopping artifact watcher...')
  process.exit(0)
})