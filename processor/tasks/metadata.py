"""
Metadata extraction task for PDF Gallery.
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional

from domain import PDFExample, Approach
from tasks import Task, TaskContext


class MetadataTask(Task):
    """
    Task to extract metadata from markdown files.
    
    This includes:
    - YAML frontmatter
    - Methods used (via AST parsing)
    - CSS selectors
    - Code complexity metrics
    """
    
    def __init__(self):
        super().__init__(name="metadata", dependencies=[])
    
    def process(self, pdf: PDFExample, context: TaskContext) -> Dict[str, Any]:
        """Extract metadata from all approaches for a PDF."""
        all_metadata = []
        
        for approach in pdf.approaches:
            if not approach.is_published():
                continue
            
            # Get base metadata from approach
            metadata = approach.metadata.copy()
            
            # Add additional extracted data
            content = approach.content
            
            # Extract methods using AST
            methods = self._extract_methods(content)
            method_usage = self._extract_method_usage_details(content)
            
            metadata.update({
                "id": pdf.id,
                "slug": approach.slug,
                "methods": methods,
                "method_usage": method_usage,
                "selectors": self._extract_selectors(content),
                "complexity": self._calculate_complexity(content),
                "approaches": [a.file.name for a in pdf.approaches]
            })
            
            # Save individual metadata
            output_path = context.get_artifact_path(pdf, f"{approach.slug}.json")
            context.write_artifact(output_path, metadata)
            
            all_metadata.append(metadata)
        
        # Save combined metadata for the PDF
        if all_metadata:
            combined_path = context.get_artifact_path(pdf, "metadata.json")
            context.write_artifact(combined_path, all_metadata)
        
        return {"metadata_count": len(all_metadata)}
    
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """Input files are all markdown files."""
        return [approach.file for approach in pdf.approaches]
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """Output files are JSON metadata for each approach."""
        outputs = []
        
        # Individual approach metadata
        for approach in pdf.approaches:
            if approach.is_published():
                outputs.append(context.get_artifact_path(pdf, f"{approach.slug}.json"))
        
        # Combined metadata
        if any(a.is_published() for a in pdf.approaches):
            outputs.append(context.get_artifact_path(pdf, "metadata.json"))
        
        return outputs
    
    def _extract_methods(self, content: str) -> List[str]:
        """Extract natural-pdf methods using AST parsing."""
        methods = set()
        code_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        
        for code in code_blocks:
            try:
                tree = ast.parse(code)
                visitor = NaturalPDFVisitor()
                visitor.visit(tree)
                
                # Simplify method names
                for method in visitor.methods:
                    if '.' in method:
                        simple_name = method.split('.')[-1]
                        methods.add(simple_name)
                    else:
                        methods.add(method)
            except SyntaxError:
                continue
        
        return sorted(list(methods))
    
    def _extract_method_usage_details(self, content: str) -> List[Dict[str, Any]]:
        """Extract detailed method usage including arguments."""
        usage_details = []
        code_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        
        for code in code_blocks:
            try:
                tree = ast.parse(code)
                visitor = DetailedUsageVisitor()
                visitor.visit(tree)
                usage_details.extend(visitor.usage_details)
            except SyntaxError:
                continue
        
        return usage_details
    
    def _extract_selectors(self, content: str) -> List[str]:
        """Extract CSS-like selectors used in find/find_all calls."""
        selectors = set()
        code_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        
        for code in code_blocks:
            lines = code.split('\n')
            for line in lines:
                if '.find' in line:
                    # Extract selector strings
                    single_quote = re.search(r"\.find(?:_all)?\s*\(\s*'([^']*)'", line)
                    double_quote = re.search(r'\.find(?:_all)?\s*\(\s*"([^"]*)"', line)
                    
                    if single_quote:
                        selectors.add(single_quote.group(1))
                    if double_quote:
                        selectors.add(double_quote.group(1))
        
        return sorted(list(selectors))
    
    def _calculate_complexity(self, content: str) -> Dict[str, Any]:
        """Calculate code complexity metrics."""
        code_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        
        total_lines = 0
        total_chars = 0
        
        for code in code_blocks:
            lines = code.strip().split('\n')
            code_lines = [
                line for line in lines 
                if line.strip() and not line.strip().startswith('#')
            ]
            total_lines += len(code_lines)
            total_chars += sum(len(line) for line in code_lines)
        
        return {
            "code_blocks": len(code_blocks),
            "total_lines": total_lines,
            "total_chars": total_chars
        }


# AST Visitors (adapted from metadata_extractor.py)

class NaturalPDFVisitor(ast.NodeVisitor):
    """AST visitor to track natural-pdf objects and their method calls."""
    
    def __init__(self):
        self.methods = set()
        self.natural_pdf_vars = {}
        self.imports = set()
    
    def visit_ImportFrom(self, node):
        """Track imports from natural_pdf."""
        if node.module and 'natural_pdf' in node.module:
            for alias in node.names:
                self.imports.add(alias.name)
                if alias.name in ['PDF', 'Guides', 'Flow']:
                    self.methods.add(alias.name)
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Track variable assignments to identify natural-pdf objects."""
        var_names = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_names.append(target.id)
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        var_names.append(elt.id)
        
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                func_name = node.value.func.id
                if func_name in ['PDF', 'Guides', 'Flow'] or func_name in self.imports:
                    for var_name in var_names:
                        self.natural_pdf_vars[var_name] = func_name
                    self.methods.add(func_name)
            
            elif isinstance(node.value.func, ast.Attribute):
                obj_name = self._get_object_name(node.value.func.value)
                if obj_name in self.natural_pdf_vars or obj_name in ['pdf', 'page', 'table']:
                    method_name = f"{obj_name}.{node.value.func.attr}"
                    self.methods.add(method_name)
                    if not node.value.func.attr.startswith('to_'):
                        for var_name in var_names:
                            self.natural_pdf_vars[var_name] = 'natural_pdf_object'
        
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Track method calls on natural-pdf objects."""
        if isinstance(node.func, ast.Attribute):
            obj_name = self._get_object_name(node.func.value)
            
            # Known natural-pdf methods
            natural_pdf_methods = {
                'find_all', 'find', 'filter', 'pages', 'dissolve', 'extract_table',
                'extract_text', 'groupby', 'classify', 'classify_pages', 'select',
                'exclude', 'merge', 'split', 'crop', 'rotate', 'scale', 'show',
                'save_pdf', 'to_df', 'inspect', 'add_exclusion', 'from_content',
                'extract_each_text', 'extract_each_table', 'info'
            }
            
            if node.func.attr in natural_pdf_methods:
                self.methods.add(node.func.attr)
            elif obj_name in self.natural_pdf_vars or obj_name in ['pdf', 'page', 'table']:
                method_name = f"{obj_name}.{node.func.attr}"
                self.methods.add(method_name)
            
            # Handle chained calls
            elif isinstance(node.func.value, ast.Call):
                self._handle_chained_call(node.func.value)
                self.methods.add(f"{node.func.attr}")
        
        self.generic_visit(node)
    
    def _handle_chained_call(self, node):
        """Recursively handle chained method calls."""
        if isinstance(node.func, ast.Attribute):
            obj_name = self._get_object_name(node.func.value)
            
            if obj_name in self.natural_pdf_vars or obj_name in ['pdf', 'page', 'table']:
                self.methods.add(f"{obj_name}.{node.func.attr}")
            elif isinstance(node.func.value, ast.Call):
                self._handle_chained_call(node.func.value)
                self.methods.add(f"{node.func.attr}")
            else:
                self.methods.add(f"{node.func.attr}")
    
    def _get_object_name(self, node):
        """Get the name of an object from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            base = self._get_object_name(node.value)
            if base:
                return base
        return None
    
    def visit_ListComp(self, node):
        """Handle list comprehensions."""
        for generator in node.generators:
            if isinstance(generator.iter, ast.Attribute):
                obj_name = self._get_object_name(generator.iter.value)
                if obj_name in self.natural_pdf_vars or obj_name in ['pdf', 'page']:
                    self.methods.add(f"{obj_name}.{generator.iter.attr}")
            
            if isinstance(generator.target, ast.Name) and isinstance(generator.iter, ast.Attribute):
                obj_name = self._get_object_name(generator.iter.value)
                if (obj_name in self.natural_pdf_vars or obj_name in ['pdf', 'page']) and generator.iter.attr in ['pages']:
                    self.natural_pdf_vars[generator.target.id] = 'natural_pdf_object'
        
        self.visit(node.elt)
        for generator in node.generators:
            self.visit(generator)


class DetailedUsageVisitor(NaturalPDFVisitor):
    """Extended visitor that captures method arguments and usage details."""
    
    def __init__(self):
        super().__init__()
        self.usage_details = []
    
    def visit_Assign(self, node):
        """Override parent to also track class instantiation usage."""
        super().visit_Assign(node)
        
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            func_name = node.value.func.id
            if func_name in ['PDF', 'Guides', 'Flow']:
                args = [self._extract_arg_value(arg) for arg in node.value.args]
                kwargs = {kw.arg: self._extract_arg_value(kw.value) for kw in node.value.keywords}
                
                self.usage_details.append({
                    'method': func_name,
                    'method_full': func_name,
                    'args': args,
                    'kwargs': kwargs
                })
    
    def visit_Call(self, node):
        """Track method calls with their arguments."""
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            
            natural_pdf_methods = {
                'find_all', 'find', 'filter', 'pages', 'dissolve', 'extract_table',
                'extract_text', 'groupby', 'classify', 'classify_pages', 'select',
                'exclude', 'merge', 'split', 'crop', 'rotate', 'scale', 'show',
                'save_pdf', 'to_df', 'inspect', 'add_exclusion', 'from_content',
                'extract_each_text', 'extract_each_table', 'info'
            }
            
            if method_name in natural_pdf_methods:
                args = [self._extract_arg_value(arg) for arg in node.args]
                kwargs = {kw.arg: self._extract_arg_value(kw.value) for kw in node.keywords}
                
                self.usage_details.append({
                    'method': method_name,
                    'method_full': method_name,
                    'args': args,
                    'kwargs': kwargs
                })
            else:
                obj_name = self._get_object_name(node.func.value)
                if obj_name in self.natural_pdf_vars or obj_name in ['pdf', 'page', 'table']:
                    args = [self._extract_arg_value(arg) for arg in node.args]
                    kwargs = {kw.arg: self._extract_arg_value(kw.value) for kw in node.keywords}
                    
                    self.usage_details.append({
                        'method': method_name,
                        'method_full': f"{obj_name}.{method_name}",
                        'args': args,
                        'kwargs': kwargs
                    })
        
        super().visit_Call(node)
    
    def _extract_arg_value(self, node):
        """Extract the value from an AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif hasattr(ast, 'Str') and isinstance(node, ast.Str):
            return node.s
        elif hasattr(ast, 'Num') and isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            return f"<var:{node.id}>"
        elif isinstance(node, ast.List):
            return [self._extract_arg_value(elt) for elt in node.elts]
        elif isinstance(node, ast.Dict):
            return {
                self._extract_arg_value(k): self._extract_arg_value(v)
                for k, v in zip(node.keys, node.values)
            }
        elif isinstance(node, (ast.NameConstant, ast.Constant)):
            return node.value
        elif isinstance(node, ast.Lambda):
            return "<Lambda>"
        else:
            return f"<{type(node).__name__}>"