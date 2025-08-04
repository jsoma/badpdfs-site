import fs from 'fs';
import path from 'path';

/**
 * Validates that required artifacts exist and are properly formatted
 * @returns {Object} Validation result with errors and warnings
 */
export function validateArtifacts() {
  const errors = [];
  const warnings = [];
  const projectRoot = process.cwd();
  const artifactsDir = path.join(projectRoot, '..', 'artifacts');
  const publicArtifactsDir = path.join(projectRoot, 'public', 'artifacts');
  
  // Check if artifacts directory exists
  if (!fs.existsSync(artifactsDir)) {
    errors.push({
      type: 'MISSING_DIR',
      message: `Artifacts directory not found at ${artifactsDir}`,
      fix: 'Run: cd processor && python build.py build'
    });
    return { errors, warnings, valid: false };
  }
  
  // Required files in artifacts directory
  const requiredFiles = [
    {
      name: 'all_metadata.json',
      validate: (content) => {
        const data = JSON.parse(content);
        return Array.isArray(data) && data.length > 0;
      },
      errorMsg: 'all_metadata.json is empty or invalid',
      fix: 'Run: cd processor && python generate_artifacts.py'
    },
    {
      name: 'valid_pdfs.json',
      validate: (content) => {
        const data = JSON.parse(content);
        return Array.isArray(data);
      },
      errorMsg: 'valid_pdfs.json is empty or invalid',
      fix: 'Run: cd processor && python validate_artifacts.py'
    }
  ];
  
  // Check processor artifacts
  for (const file of requiredFiles) {
    const filePath = path.join(artifactsDir, file.name);
    if (!fs.existsSync(filePath)) {
      errors.push({
        type: 'MISSING_FILE',
        file: file.name,
        message: `Required file ${file.name} not found in processor artifacts`,
        fix: file.fix
      });
    } else {
      try {
        const content = fs.readFileSync(filePath, 'utf-8');
        if (!file.validate(content)) {
          errors.push({
            type: 'INVALID_FILE',
            file: file.name,
            message: file.errorMsg,
            fix: file.fix
          });
        }
      } catch (e) {
        errors.push({
          type: 'PARSE_ERROR',
          file: file.name,
          message: `Failed to parse ${file.name}: ${e.message}`,
          fix: file.fix
        });
      }
    }
  }
  
  // Check if artifacts are synced to frontend
  if (!fs.existsSync(publicArtifactsDir)) {
    errors.push({
      type: 'MISSING_PUBLIC_ARTIFACTS',
      message: 'Artifacts not synced to frontend public directory',
      fix: 'Run: cd processor && python fix_execution_paths.py'
    });
  } else {
    // Check if files are in sync
    for (const file of requiredFiles) {
      const processorPath = path.join(artifactsDir, file.name);
      const publicPath = path.join(publicArtifactsDir, file.name);
      
      if (fs.existsSync(processorPath) && !fs.existsSync(publicPath)) {
        warnings.push({
          type: 'NOT_SYNCED',
          file: file.name,
          message: `${file.name} exists in processor but not in frontend`,
          fix: 'Run: cd processor && python fix_execution_paths.py'
        });
      } else if (fs.existsSync(processorPath) && fs.existsSync(publicPath)) {
        // Check if files are different
        const processorContent = fs.readFileSync(processorPath, 'utf-8');
        const publicContent = fs.readFileSync(publicPath, 'utf-8');
        if (processorContent !== publicContent) {
          warnings.push({
            type: 'OUT_OF_SYNC',
            file: file.name,
            message: `${file.name} is out of sync between processor and frontend`,
            fix: 'Run: cd processor && python fix_execution_paths.py'
          });
        }
      }
    }
  }
  
  // Check for execution files
  const executionsDir = path.join(publicArtifactsDir, 'executions', 'pdfs');
  if (!fs.existsSync(executionsDir)) {
    warnings.push({
      type: 'NO_EXECUTIONS',
      message: 'No execution results found',
      fix: 'Run: cd processor && python execute_markdown.py ../content -v'
    });
  } else {
    // Check if we have execution files for valid PDFs
    try {
      const validPdfsPath = path.join(publicArtifactsDir, 'valid_pdfs.json');
      if (fs.existsSync(validPdfsPath)) {
        const validPdfs = JSON.parse(fs.readFileSync(validPdfsPath, 'utf-8'));
        let missingExecutions = 0;
        
        for (const pdfId of validPdfs) {
          const pdfExecDir = path.join(executionsDir, pdfId);
          if (!fs.existsSync(pdfExecDir)) {
            missingExecutions++;
          }
        }
        
        if (missingExecutions > 0) {
          warnings.push({
            type: 'MISSING_EXECUTIONS',
            message: `${missingExecutions} valid PDFs are missing execution results`,
            fix: 'Run: cd processor && python execute_markdown.py ../content -v'
          });
        }
      }
    } catch (e) {
      // Non-critical error
    }
  }
  
  return {
    errors,
    warnings,
    valid: errors.length === 0
  };
}

/**
 * Creates a helpful error page content
 */
export function createErrorPage(validation) {
  const { errors, warnings } = validation;
  
  let content = '# Build Artifacts Missing\n\n';
  
  if (errors.length > 0) {
    content += '## Errors\n\n';
    content += 'The following critical issues must be fixed:\n\n';
    
    for (const error of errors) {
      content += `### ${error.type}\n`;
      content += `- **Issue**: ${error.message}\n`;
      content += `- **Fix**: \`${error.fix}\`\n\n`;
    }
  }
  
  if (warnings.length > 0) {
    content += '## Warnings\n\n';
    content += 'The following issues should be addressed:\n\n';
    
    for (const warning of warnings) {
      content += `- ${warning.message}\n`;
      content += `  - Fix: \`${warning.fix}\`\n`;
    }
  }
  
  content += '\n## Quick Fix\n\n';
  content += 'To rebuild all artifacts, run:\n\n';
  content += '```bash\n';
  content += 'cd processor\n';
  content += 'source .venv/bin/activate  # On macOS/Linux\n';
  content += 'python build.py build\n';
  content += '```\n';
  
  return content;
}