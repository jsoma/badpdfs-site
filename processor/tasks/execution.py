"""
Code execution task for PDF Gallery.
"""

import re
import io
import os
import sys
import json
import ast
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import redirect_stdout, redirect_stderr

from domain import PDFExample, Approach
from tasks import Task, TaskContext

# Try to import matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    plt = None


class ExecutionTask(Task):
    """
    Task to execute Python code blocks in markdown files.
    
    This includes:
    - Running Python code in isolated namespaces
    - Capturing stdout/stderr
    - Capturing matplotlib figures
    - Handling rich outputs (DataFrames, images, etc.)
    """
    
    def __init__(self):
        super().__init__(name="execution", dependencies=["metadata"])
        self.namespace = {}
        self.figures = []
        self.image_counter = 0
        self.current_file_path = None
        self._setup_matplotlib_capture()
    
    def _setup_matplotlib_capture(self):
        """Setup matplotlib to capture figures."""
        if not HAS_MATPLOTLIB:
            return
        
        # Store original show function
        self._original_show = plt.show
        
        def capture_show(*args, **kwargs):
            # Capture all current figures
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                buf.seek(0)
                # Save image to file
                image_path = self._save_image(buf.read(), 'png')
                self.figures.append({
                    'format': 'png',
                    'path': image_path
                })
                plt.close(fig)
        
        plt.show = capture_show
    
    def process(self, pdf: PDFExample, context: TaskContext) -> Dict[str, Any]:
        """Execute code in all published approaches for a PDF."""
        results = []
        
        for approach in pdf.approaches:
            if not approach.is_published():
                continue
            
            # context.log(f"Executing code in {approach.slug}")
            
            # Reset state for each approach
            self.reset_state()
            
            # Process the markdown file
            try:
                result = self._process_approach(approach, context)
                
                # Check for errors in code blocks
                error_count = 0
                for cell_idx, cell in enumerate(result.get('cells', [])):
                    if cell.get('type') == 'code' and cell.get('execution', {}).get('status') == 'error':
                        error_count += 1
                        full_error = cell['execution']['error']
                        # context.log(f"\n{'='*60}", "ERROR")
                        # context.log(f"Code block error in {approach.slug} (cell #{cell_idx + 1}):", "ERROR")
                        # context.log(f"Code snippet: {cell.get('content', '')[:100]}...", "ERROR")
                        # context.log(f"{'='*60}", "ERROR")
                        # context.log(f"Full traceback:\n{full_error}", "ERROR")
                        # context.log(f"{'='*60}\n", "ERROR")
                    elif cell.get('type') == 'tab':
                        for tab_idx, tab_cell in enumerate(cell.get('cells', [])):
                            if tab_cell.get('type') == 'code' and tab_cell.get('execution', {}).get('status') == 'error':
                                error_count += 1
                                full_error = tab_cell['execution']['error']
                                # context.log(f"\n{'='*60}", "ERROR")
                                # context.log(f"Code block error in {approach.slug} (tab cell #{tab_idx + 1}):", "ERROR")
                                # context.log(f"Code snippet: {tab_cell.get('content', '')[:100]}...", "ERROR")
                                # context.log(f"{'='*60}", "ERROR")
                                # context.log(f"Full traceback:\n{full_error}", "ERROR")
                                # context.log(f"{'='*60}\n", "ERROR")
                
                # if error_count > 0:
                #     context.log(f"Found {error_count} code block error(s) in {approach.slug}", "WARNING")
                
                # Save result
                output_path = context.get_artifact_path(
                    pdf, "executions", f"{approach.slug}.json"
                )
                context.write_artifact(output_path, result)
                
                results.append({
                    'approach': approach.slug,
                    'status': 'success',
                    'code_errors': error_count
                })
            except Exception as e:
                # context.log(f"Error executing {approach.slug}: {e}", "ERROR")
                results.append({
                    'approach': approach.slug,
                    'status': 'error',
                    'error': str(e)
                })
        
        return {"executed": len(results), "results": results}
    
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """Input files are markdown files."""
        return [approach.file for approach in pdf.approaches if approach.is_published()]
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """Output files are execution results."""
        outputs = []
        for approach in pdf.approaches:
            if approach.is_published():
                outputs.append(
                    context.get_artifact_path(pdf, "executions", f"{approach.slug}.json")
                )
        return outputs
    
    def reset_state(self):
        """Reset execution state between approaches."""
        self.namespace = {}
        self.figures = []
        self.image_counter = 0
    
    def _process_approach(self, approach: Approach, context: TaskContext) -> Dict[str, Any]:
        """Process a single approach file."""
        # Set current file path for image saving
        self.current_file_path = f"pdfs/{approach.pdf_example.id}/{approach.slug}"
        
        # Parse cells
        cells = self._parse_cells(approach.content)
        
        # Save current directory
        original_cwd = os.getcwd()
        markdown_dir = approach.file.parent.absolute()
        
        try:
            # Change to markdown file's directory
            os.chdir(markdown_dir)
            
            # Execute code cells
            for cell in cells:
                if cell['type'] == 'code':
                    execution_result = self._execute_code(cell['content'], context)
                    cell['execution'] = execution_result
                elif cell['type'] == 'bash':
                    # Skip bash cells
                    cell['execution'] = {
                        'status': 'skipped',
                        'output': f'Bash command skipped: {cell["content"]}',
                        'error': None,
                        'figures': [],
                        'result': None
                    }
                elif cell['type'] == 'tab':
                    # Process cells within tabs
                    for tab_cell in cell.get('cells', []):
                        if tab_cell['type'] == 'code':
                            execution_result = self._execute_code(tab_cell['content'], context)
                            tab_cell['execution'] = execution_result
                        elif tab_cell['type'] == 'bash':
                            tab_cell['execution'] = {
                                'status': 'skipped',
                                'output': f'Bash command skipped',
                                'error': None,
                                'figures': [],
                                'result': None
                            }
        finally:
            # Restore original directory
            os.chdir(original_cwd)
        
        return {
            'file': str(approach.file),
            'metadata': approach.metadata,
            'cells': cells
        }
    
    def _parse_cells(self, content: str) -> List[Dict[str, Any]]:
        """Parse markdown content into cells."""
        # Remove frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Check for tab blocks
        if '/// tab |' in content:
            return self._parse_with_tabs(content)
        else:
            return self._parse_regular_cells(content)
    
    def _parse_with_tabs(self, content: str) -> List[Dict[str, Any]]:
        """Parse markdown content with tab blocks."""
        cells = []
        
        # Pattern for tab blocks
        tab_pattern = r'/// tab \| ([^\n]+)\n(.*?)\n///'
        
        # Split content by tabs
        parts = re.split(r'(/// tab \| [^\n]+\n.*?\n///)', content, flags=re.DOTALL)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Check if this is a tab block
            tab_match = re.match(tab_pattern, part, re.DOTALL)
            if tab_match:
                tab_title = tab_match.group(1).strip()
                tab_content = tab_match.group(2).strip()
                
                # Parse content within tab
                tab_cells = self._parse_regular_cells(tab_content)
                
                cells.append({
                    'type': 'tab',
                    'title': tab_title,
                    'cells': tab_cells
                })
            else:
                # Regular content
                regular_cells = self._parse_regular_cells(part)
                cells.extend(regular_cells)
        
        return cells
    
    def _parse_regular_cells(self, content: str) -> List[Dict[str, Any]]:
        """Parse regular markdown content."""
        # More flexible pattern that allows spaces after language identifier
        pattern = r'```(\w+)(?:\s*)\n(.*?)\n```'
        cells = []
        last_end = 0
        
        for match in re.finditer(pattern, content, re.DOTALL):
            # Add markdown before code block
            if match.start() > last_end:
                markdown_content = content[last_end:match.start()].strip()
                if markdown_content:
                    cells.append({
                        'type': 'markdown',
                        'content': markdown_content
                    })
            
            # Add code block
            language = match.group(1).strip()  # Strip any whitespace from language
            code_content = match.group(2).strip()
            
            if language == 'python':
                cells.append({
                    'type': 'code',
                    'content': code_content
                })
            elif language == 'bash':
                cells.append({
                    'type': 'bash',
                    'content': code_content
                })
            else:
                # Other languages as markdown
                cells.append({
                    'type': 'markdown',
                    'content': f'```{language}\n{code_content}\n```'
                })
            
            last_end = match.end()
        
        # Add remaining markdown
        if last_end < len(content):
            markdown_content = content[last_end:].strip()
            if markdown_content:
                cells.append({
                    'type': 'markdown',
                    'content': markdown_content
                })
        
        return cells
    
    def _execute_code(self, code: str, context: TaskContext) -> Dict[str, Any]:
        """Execute Python code and capture output."""
        # Clear figures
        self.figures = []
        
        # Log the code being executed
        
        # Skip shell commands
        if code.strip().startswith('!'):
            return {
                'status': 'skipped',
                'output': f'Shell command skipped: {code.strip()}',
                'error': None,
                'figures': [],
                'result': None
            }
        
        # Capture stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        result = {
            'status': 'success',
            'output': '',
            'error': None,
            'figures': [],
            'result': None
        }
        
        try:
            # Parse code to separate last expression
            tree = ast.parse(code)
            last_expr = None
            
            # Check if last statement is expression
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last_expr = tree.body[-1]
                tree.body = tree.body[:-1]
                code_without_last = ast.unparse(tree) if tree.body else ""
            else:
                code_without_last = code
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # Execute all but last expression
                if code_without_last:
                    # context.log(f"Executing code: {code_without_last[:100]}...", "DEBUG")
                    exec(code_without_last, self.namespace)
                
                # Evaluate last expression
                if last_expr:
                    expr_str = ast.unparse(last_expr.value)
                    # context.log(f"Evaluating expression: {expr_str[:100]}...", "DEBUG")
                    last_value = eval(expr_str, self.namespace)
            
            # Capture rich output
            if last_expr:
                rich_output = self._capture_rich_output(last_value, context)
                if rich_output:
                    result['result'] = rich_output
            
            # For successful executions, combine stdout and stderr
            stdout_content = stdout_capture.getvalue()
            stderr_content = stderr_capture.getvalue()
            
            # Combine stdout and stderr for display
            combined_output = stdout_content
            if stderr_content:
                combined_output += stderr_content
            
            # Clean up progress output
            combined_output = self._clean_progress_output(combined_output)
            
            result['output'] = combined_output
            
            # Add captured figures
            result['figures'] = self.figures.copy()
            
        except Exception as e:
            result['status'] = 'error'
            result['output'] = stdout_capture.getvalue()
            result['error'] = traceback.format_exc()
        
        return result
    
    def _capture_rich_output(self, obj: Any, context: TaskContext) -> Optional[Dict[str, Any]]:
        """Capture rich output from an object."""
        if obj is None:
            return None
        
        # Check for PIL Image
        if hasattr(obj, '_repr_png_'):
            try:
                png_data = obj._repr_png_()
                image_path = self._save_image(png_data, 'png', context)
                return {
                    'type': 'image/png',
                    'path': image_path
                }
            except:
                pass
        
        # Check for matplotlib figure
        if str(type(obj)) == "<class 'matplotlib.figure.Figure'>":
            buf = io.BytesIO()
            obj.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            image_path = self._save_image(buf.read(), 'png', context)
            return {
                'type': 'image/png',
                'path': image_path
            }
        
        # Check for HTML representation
        if hasattr(obj, '_repr_html_'):
            try:
                html = obj._repr_html_()
                return {
                    'type': 'text/html',
                    'data': html
                }
            except:
                pass
        
        # Always include string representation
        try:
            repr_str = repr(obj)
            return {
                'type': 'text/plain',
                'data': repr_str
            }
        except:
            try:
                return {
                    'type': 'text/plain',
                    'data': str(obj)
                }
            except:
                return None
    
    def _save_image(self, image_data: bytes, format: str, context: TaskContext) -> str:
        """Save image data to file."""
        if not self.current_file_path:
            raise ValueError("No current file path set")
        
        # Create images directory
        images_dir = context.artifacts_dir / "executions" / self.current_file_path / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        self.image_counter += 1
        image_filename = f"image_{self.image_counter}.{format}"
        image_path = images_dir / image_filename
        
        # Save image
        with open(image_path, 'wb') as f:
            f.write(image_data)
        
        # Return relative path from artifacts
        return str(image_path.relative_to(context.artifacts_dir))
    
    def _clean_progress_output(self, output: str) -> str:
        """Clean up repetitive progress output."""
        if not output:
            return output
        
        lines = output.split('\n')
        cleaned_lines = []
        last_progress_line = None
        
        # Pattern to match progress lines
        progress_pattern = re.compile(r'^Progress:\s*\|.*\|\s*\d+\.?\d*%\s*Complete\s*$')
        
        for line in lines:
            if progress_pattern.match(line.strip()):
                # Store the last progress line, don't add duplicates
                last_progress_line = line
            else:
                # If we had progress lines before this, add the last one
                if last_progress_line is not None:
                    cleaned_lines.append(last_progress_line)
                    last_progress_line = None
                # Add the non-progress line
                cleaned_lines.append(line)
        
        # Don't forget the final progress line if it exists
        if last_progress_line is not None:
            cleaned_lines.append(last_progress_line)
        
        return '\n'.join(cleaned_lines)
    
    def __del__(self):
        """Restore original plt.show."""
        if HAS_MATPLOTLIB and hasattr(self, '_original_show'):
            plt.show = self._original_show