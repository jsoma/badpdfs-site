import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Source and destination paths
const artifactsSource = path.join(__dirname, '..', '..', 'artifacts')
const artifactsDest = path.join(__dirname, '..', 'public', 'artifacts')

// Create destination directory if it doesn't exist
if (!fs.existsSync(artifactsDest)) {
  fs.mkdirSync(artifactsDest, { recursive: true })
}

// Function to copy directory recursively
function copyDir(src, dest) {
  // Create destination directory
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true })
  }

  // Read directory
  const entries = fs.readdirSync(src, { withFileTypes: true })

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name)
    const destPath = path.join(dest, entry.name)

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath)
    } else {
      fs.copyFileSync(srcPath, destPath)
    }
  }
}

console.log('Copying artifacts to public directory...')

// Check if validation files exist
const validPdfs = path.join(artifactsSource, 'valid_pdfs.json')
if (!fs.existsSync(validPdfs)) {
  console.error('❌ valid_pdfs.json not found. Run validation first!')
  process.exit(1)
}

copyDir(artifactsSource, artifactsDest)
console.log('✓ Artifacts copied successfully')