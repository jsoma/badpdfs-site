import { validateArtifacts } from '../utils/artifact-validator.js';

/**
 * Pre-flight check for artifacts
 * This runs during the build process to ensure all required files exist
 */
export function checkArtifacts() {
  const validation = validateArtifacts();
  
  if (!validation.valid) {
    console.error('\n🚨 ARTIFACT VALIDATION FAILED\n');
    console.error('The following errors must be fixed before the site can build:\n');
    
    validation.errors.forEach(error => {
      console.error(`❌ ${error.message}`);
      console.error(`   Fix: ${error.fix}\n`);
    });
    
    if (validation.warnings.length > 0) {
      console.warn('\n⚠️  Warnings:');
      validation.warnings.forEach(warning => {
        console.warn(`- ${warning.message}`);
        console.warn(`  Fix: ${warning.fix}`);
      });
    }
    
    console.error('\n📋 Quick fix - run all processing steps:');
    console.error('   cd processor && source .venv/bin/activate && python build.py build\n');
    
    throw new Error('Artifact validation failed. See errors above.');
  }
  
  if (validation.warnings.length > 0) {
    console.warn('\n⚠️  Artifact validation warnings:');
    validation.warnings.forEach(warning => {
      console.warn(`- ${warning.message}`);
    });
    console.warn('');
  }
  
  return validation;
}