"""
Dashboard generation task for PDF Gallery.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from domain import PDFExample
from tasks import BatchTask, TaskContext


class DashboardTask(BatchTask):
    """
    Task to generate a static HTML dashboard for backend management.
    
    This includes:
    - All PDFs (published and unpublished)
    - Sorting and filtering capabilities
    - VS Code integration
    """
    
    def __init__(self):
        super().__init__(
            name="dashboard", 
            dependencies=["metadata"]
        )
    
    def process_batch(self, pdfs: List[PDFExample], context: TaskContext) -> Dict[str, Any]:
        """Generate the dashboard HTML."""
        
        # Build metadata from all PDFs (published and unpublished)
        all_metadata = []
        project_root = context.artifacts_dir.parent
        
        for pdf in pdfs:
            # Get metadata for each PDF
            for approach in pdf.approaches:
                if approach.metadata:  # Use the first approach with metadata
                    item = approach.metadata.copy()
                    item['id'] = pdf.id
                    
                    # Add VS Code link
                    md_path = project_root / "content" / "pdfs" / pdf.id / f"{pdf.id}.md"
                    if md_path.exists():
                        item['vscode_link'] = f"vscode://file/{md_path}"
                        item['file_path'] = str(md_path)
                    
                    all_metadata.append(item)
                    break  # Only need one metadata per PDF
        
        # Generate HTML with config
        # Get the R2 base URL - construct it from r2_public_url
        r2_public_url = context.config.get('r2_public_url', 'https://pub-4e99d31d19cb404d8d4f5f7efa51ef6e.r2.dev')
        r2_pdf_base_url = f"{r2_public_url}/pdfs"
        html = self._generate_html(all_metadata, r2_pdf_base_url)
        
        # Write dashboard
        dashboard_path = context.artifacts_dir / "dashboard.html"
        dashboard_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return {
            "total_pdfs": len(all_metadata),
            "published": sum(1 for p in all_metadata if p.get('published', False)),
            "unpublished": sum(1 for p in all_metadata if not p.get('published', False)),
            "dashboard_path": str(dashboard_path)
        }
    
    def _generate_html(self, all_metadata: List[Dict], r2_pdf_base_url: str) -> str:
        """Generate the dashboard HTML."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bad PDFs Backend Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #666;
        }}
        .controls {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            align-items: center;
        }}
        input, select {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}
        input[type="search"] {{
            width: 300px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th, td {{
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        th:hover {{
            background: #e9ecef;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .published {{
            color: #28a745;
            font-weight: 500;
        }}
        .unpublished {{
            color: #dc3545;
            font-weight: 500;
        }}
        .tag {{
            display: inline-block;
            padding: 2px 8px;
            margin: 2px;
            background: #e9ecef;
            border-radius: 3px;
            font-size: 12px;
        }}
        .vscode-link {{
            color: #007acc;
            text-decoration: none;
            font-weight: 500;
        }}
        .vscode-link:hover {{
            text-decoration: underline;
        }}
        .sort-arrow {{
            font-size: 10px;
            margin-left: 5px;
            color: #999;
        }}
        .active-sort {{
            color: #333;
        }}
        .file-size {{
            font-family: monospace;
            color: #666;
        }}
        .description {{
            font-size: 12px;
            color: #666;
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .pdf-title {{
            color: #007acc;
            cursor: pointer;
            text-decoration: none;
        }}
        .pdf-title:hover {{
            text-decoration: underline;
        }}
        .pdf-id {{
            font-size: 11px;
            color: #999;
            font-family: monospace;
            margin-bottom: 2px;
        }}
        .preview-btn {{
            background: #007acc;
            color: white;
            border: none;
            padding: 4px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            margin-right: 8px;
        }}
        .preview-btn:hover {{
            background: #005a9e;
        }}
        
        /* Modal styles */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
        }}
        .modal-content {{
            position: relative;
            background: white;
            margin: 20px auto;
            width: 90%;
            max-width: 1200px;
            height: calc(100vh - 40px);
            border-radius: 8px;
            display: flex;
            flex-direction: column;
        }}
        .modal-header {{
            padding: 20px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .modal-title {{
            font-size: 20px;
            font-weight: 600;
            margin: 0;
        }}
        .modal-body {{
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            gap: 20px;
        }}
        .pdf-preview {{
            flex: 1;
            background: #f5f5f5;
            border-radius: 4px;
            padding: 20px;
            text-align: center;
            position: relative;
            min-height: 600px;
        }}
        .pdf-frame {{
            width: 100%;
            height: 100%;
            border: none;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .pdf-details {{
            flex: 1;
            overflow-y: auto;
        }}
        .detail-section {{
            margin-bottom: 24px;
        }}
        .detail-section h3 {{
            font-size: 16px;
            margin-bottom: 8px;
            color: #333;
        }}
        .close {{
            font-size: 28px;
            font-weight: bold;
            color: #999;
            cursor: pointer;
            background: none;
            border: none;
            padding: 0;
        }}
        .close:hover {{
            color: #333;
        }}
        .nav-buttons {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 100%;
            display: flex;
            justify-content: space-between;
            pointer-events: none;
            padding: 0 20px;
        }}
        .nav-btn {{
            background: rgba(0, 0, 0, 0.7);
            color: white;
            border: none;
            width: 40px;
            height: 60px;
            cursor: pointer;
            pointer-events: all;
            font-size: 20px;
            border-radius: 4px;
        }}
        .nav-btn:hover {{
            background: rgba(0, 0, 0, 0.9);
        }}
        .nav-btn:disabled {{
            opacity: 0.3;
            cursor: not-allowed;
        }}
        .keyboard-hint {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: #666;
            background: rgba(255, 255, 255, 0.9);
            padding: 4px 8px;
            border-radius: 4px;
        }}
        pre {{
            background: #f5f5f5;
            padding: 12px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 13px;
        }}
        .loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 18px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Bad PDFs Backend Dashboard</h1>
        <div class="stats" id="stats"></div>
        
        <div class="controls">
            <input type="search" id="search" placeholder="Search PDFs, tags, descriptions...">
            
            <select id="statusFilter">
                <option value="">All PDFs</option>
                <option value="published">Published Only</option>
                <option value="unpublished">Unpublished Only</option>
            </select>
            
            <select id="sizeFilter">
                <option value="">All Sizes</option>
                <option value="small">Small (&lt; 1MB)</option>
                <option value="medium">Medium (1-5MB)</option>
                <option value="large">Large (&gt; 5MB)</option>
            </select>
            
            <select id="pageFilter">
                <option value="">All Page Counts</option>
                <option value="single">Single Page</option>
                <option value="few">2-10 Pages</option>
                <option value="many">11+ Pages</option>
            </select>
            
            <button onclick="resetFilters()">Reset Filters</button>
        </div>
        
        <table id="pdfTable">
            <thead>
                <tr>
                    <th onclick="sortTable('title')">PDF <span class="sort-arrow" data-col="title"></span></th>
                    <th onclick="sortTable('published')">Status <span class="sort-arrow" data-col="published"></span></th>
                    <th onclick="sortTable('file_size_mb')">Size (MB) <span class="sort-arrow" data-col="file_size_mb"></span></th>
                    <th onclick="sortTable('page_count')">Pages <span class="sort-arrow" data-col="page_count"></span></th>
                    <th onclick="sortTable('submitted_by')">Submitter <span class="sort-arrow" data-col="submitted_by"></span></th>
                    <th>Tags</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody id="tableBody">
            </tbody>
        </table>
    </div>
    
    <!-- Preview Modal -->
    <div id="previewModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title" id="modalTitle">PDF Preview</h2>
                <button class="close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="pdf-preview">
                    <div class="loading" id="pdfLoading">Loading PDF...</div>
                    <iframe id="pdfFrame" class="pdf-frame" style="display: none;"></iframe>
                    <div class="nav-buttons">
                        <button class="nav-btn" id="prevBtn" onclick="navigatePDF(-1)">&lt;</button>
                        <button class="nav-btn" id="nextBtn" onclick="navigatePDF(1)">&gt;</button>
                    </div>
                    <div class="keyboard-hint">Use ← → keys to navigate</div>
                </div>
                <div class="pdf-details">
                    <div class="detail-section">
                        <h3>Details</h3>
                        <div id="pdfDetails"></div>
                    </div>
                    <div class="detail-section">
                        <h3>Queue Management</h3>
                        <label>
                            <input type="checkbox" id="queueCheckbox" onchange="toggleQueue()">
                            <span>Add to processing queue</span>
                        </label>
                        <div id="queueStatus" style="margin-top: 8px; color: #666; font-size: 14px;"></div>
                    </div>
                    <div class="detail-section">
                        <h3>Actions</h3>
                        <button class="vscode-link" id="modalVscodeLink" style="padding: 8px 16px;">Open in VS Code</button>
                    </div>
                    <div class="detail-section">
                        <h3>Raw Metadata</h3>
                        <pre id="rawMetadata"></pre>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Embedded metadata
        const allPDFs = {json.dumps(all_metadata, indent=8)};
        
        let sortColumn = 'file_size_mb';
        let sortDirection = 'desc';
        let filteredPDFs = [...allPDFs];
        
        function updateStats() {{
            const total = allPDFs.length;
            const published = allPDFs.filter(p => p.published).length;
            const unpublished = total - published;
            const totalSize = allPDFs.reduce((sum, p) => sum + (p.file_size_mb || 0), 0);
            const totalPages = allPDFs.reduce((sum, p) => sum + (p.page_count || 0), 0);
            
            document.getElementById('stats').innerHTML = `
                <div><strong>Total PDFs:</strong> ${{total}}</div>
                <div><strong>Published:</strong> <span class="published">${{published}}</span></div>
                <div><strong>Unpublished:</strong> <span class="unpublished">${{unpublished}}</span></div>
                <div><strong>Total Size:</strong> ${{totalSize.toFixed(1)}} MB</div>
                <div><strong>Total Pages:</strong> ${{totalPages.toLocaleString()}}</div>
                <div><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
            `;
        }}
        
        function renderTable() {{
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = filteredPDFs.map((pdf, index) => `
                <tr>
                    <td>
                        <div class="pdf-id">${{pdf.id}}</div>
                        <a href="#" class="pdf-title" onclick="openPreview(${{index}}); return false;">${{pdf.title || pdf.id}}</a>
                        ${{pdf.description ? `<div class="description">${{pdf.description}}</div>` : ''}}
                    </td>
                    <td class="${{pdf.published ? 'published' : 'unpublished'}}">${{pdf.published ? 'Published' : 'Unpublished'}}</td>
                    <td class="file-size">${{(pdf.file_size_mb || 0).toFixed(2)}}</td>
                    <td>${{pdf.page_count || 0}}</td>
                    <td>${{pdf.submitted_by || 'Unknown'}}</td>
                    <td>${{(pdf.tags || []).map(tag => `<span class="tag">${{tag}}</span>`).join('')}}</td>
                    <td>
                        ${{pdf.vscode_link ? `<a href="${{pdf.vscode_link}}" class="vscode-link" title="${{pdf.file_path}}">VS Code</a>` : ''}}
                    </td>
                </tr>
            `).join('');
            
            // Update sort arrows
            document.querySelectorAll('.sort-arrow').forEach(arrow => {{
                arrow.textContent = '';
                arrow.classList.remove('active-sort');
                if (arrow.dataset.col === sortColumn) {{
                    arrow.textContent = sortDirection === 'asc' ? '▲' : '▼';
                    arrow.classList.add('active-sort');
                }}
            }});
        }}
        
        function sortTable(column) {{
            if (sortColumn === column) {{
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            }} else {{
                sortColumn = column;
                sortDirection = 'asc';
            }}
            
            filteredPDFs.sort((a, b) => {{
                let aVal = a[column];
                let bVal = b[column];
                
                // Handle null/undefined
                if (aVal == null) aVal = '';
                if (bVal == null) bVal = '';
                
                // Numeric comparison for numbers
                if (typeof aVal === 'number' && typeof bVal === 'number') {{
                    return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
                }}
                
                // String comparison
                aVal = String(aVal).toLowerCase();
                bVal = String(bVal).toLowerCase();
                
                if (sortDirection === 'asc') {{
                    return aVal.localeCompare(bVal);
                }} else {{
                    return bVal.localeCompare(aVal);
                }}
            }});
            
            renderTable();
        }}
        
        function applyFilters() {{
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const statusFilter = document.getElementById('statusFilter').value;
            const sizeFilter = document.getElementById('sizeFilter').value;
            const pageFilter = document.getElementById('pageFilter').value;
            
            filteredPDFs = allPDFs.filter(pdf => {{
                // Search filter
                if (searchTerm) {{
                    const searchIn = [
                        pdf.id,
                        pdf.title,
                        pdf.description,
                        pdf.submitted_by,
                        ...(pdf.tags || [])
                    ].filter(Boolean).join(' ').toLowerCase();
                    
                    if (!searchIn.includes(searchTerm)) return false;
                }}
                
                // Status filter
                if (statusFilter === 'published' && !pdf.published) return false;
                if (statusFilter === 'unpublished' && pdf.published) return false;
                
                // Size filter
                const size = pdf.file_size_mb || 0;
                if (sizeFilter === 'small' && size >= 1) return false;
                if (sizeFilter === 'medium' && (size < 1 || size > 5)) return false;
                if (sizeFilter === 'large' && size <= 5) return false;
                
                // Page filter
                const pages = pdf.page_count || 0;
                if (pageFilter === 'single' && pages !== 1) return false;
                if (pageFilter === 'few' && (pages < 2 || pages > 10)) return false;
                if (pageFilter === 'many' && pages <= 10) return false;
                
                return true;
            }});
            
            renderTable();
        }}
        
        function resetFilters() {{
            document.getElementById('search').value = '';
            document.getElementById('statusFilter').value = '';
            document.getElementById('sizeFilter').value = '';
            document.getElementById('pageFilter').value = '';
            applyFilters();
        }}
        
        // Event listeners
        document.getElementById('search').addEventListener('input', applyFilters);
        document.getElementById('statusFilter').addEventListener('change', applyFilters);
        document.getElementById('sizeFilter').addEventListener('change', applyFilters);
        document.getElementById('pageFilter').addEventListener('change', applyFilters);
        
        // Initialize with size descending
        sortTable('file_size_mb');
        updateStats();
        
        // Modal and preview functionality
        let currentPDFIndex = 0;
        let processingQueue = JSON.parse(localStorage.getItem('pdfProcessingQueue') || '[]');
        
        function openPreview(index) {{
            currentPDFIndex = index;
            showPDF(filteredPDFs[index]);
            document.getElementById('previewModal').style.display = 'block';
            updateNavigationButtons();
            
            // Preload adjacent PDFs
            preloadAdjacentPDFs(index);
        }}
        
        function closeModal() {{
            document.getElementById('previewModal').style.display = 'none';
            document.getElementById('pdfFrame').src = '';
        }}
        
        function showPDF(pdf) {{
            // Update modal title
            document.getElementById('modalTitle').textContent = pdf.title || pdf.id;
            
            // Show loading
            document.getElementById('pdfLoading').style.display = 'block';
            document.getElementById('pdfFrame').style.display = 'none';
            
            // Set PDF URL - using R2 URL from metadata
            const pdfFilename = pdf.pdf || pdf.id + '.pdf';
            const pdfUrl = `{r2_pdf_base_url}/${{pdf.id}}/${{pdfFilename}}`;
            console.log('Loading PDF:', pdfUrl, 'from metadata:', pdf);
            const frame = document.getElementById('pdfFrame');
            
            frame.onload = function() {{
                document.getElementById('pdfLoading').style.display = 'none';
                document.getElementById('pdfFrame').style.display = 'block';
            }};
            
            frame.src = pdfUrl;
            
            // Update details
            const detailsHtml = `
                <p><strong>ID:</strong> ${{pdf.id}}</p>
                <p><strong>Status:</strong> <span class="${{pdf.published ? 'published' : 'unpublished'}}">${{pdf.published ? 'Published' : 'Unpublished'}}</span></p>
                <p><strong>Size:</strong> ${{(pdf.file_size_mb || 0).toFixed(2)}} MB</p>
                <p><strong>Pages:</strong> ${{pdf.page_count || 0}}</p>
                <p><strong>Submitted by:</strong> ${{pdf.submitted_by || 'Unknown'}}</p>
                ${{pdf.description ? `<p><strong>Description:</strong> ${{pdf.description}}</p>` : ''}}
                ${{pdf.tags && pdf.tags.length ? `<p><strong>Tags:</strong> ${{pdf.tags.map(tag => `<span class="tag">${{tag}}</span>`).join('')}}</p>` : ''}}
            `;
            document.getElementById('pdfDetails').innerHTML = detailsHtml;
            
            // Update raw metadata
            document.getElementById('rawMetadata').textContent = JSON.stringify(pdf, null, 2);
            
            // Update VS Code link
            const vscodeBtn = document.getElementById('modalVscodeLink');
            if (pdf.vscode_link) {{
                vscodeBtn.style.display = 'inline-block';
                vscodeBtn.onclick = () => window.location.href = pdf.vscode_link;
            }} else {{
                vscodeBtn.style.display = 'none';
            }}
            
            // Update queue checkbox
            document.getElementById('queueCheckbox').checked = processingQueue.includes(pdf.id);
            updateQueueStatus();
        }}
        
        function navigatePDF(direction) {{
            const newIndex = currentPDFIndex + direction;
            if (newIndex >= 0 && newIndex < filteredPDFs.length) {{
                currentPDFIndex = newIndex;
                showPDF(filteredPDFs[newIndex]);
                updateNavigationButtons();
                preloadAdjacentPDFs(newIndex);
            }}
        }}
        
        function updateNavigationButtons() {{
            document.getElementById('prevBtn').disabled = currentPDFIndex === 0;
            document.getElementById('nextBtn').disabled = currentPDFIndex === filteredPDFs.length - 1;
        }}
        
        function preloadAdjacentPDFs(index) {{
            // Preload previous and next PDFs
            const preloadFrame = document.createElement('iframe');
            preloadFrame.style.display = 'none';
            
            if (index > 0) {{
                const prevPdf = filteredPDFs[index - 1];
                const prevFilename = prevPdf.pdf || prevPdf.id + '.pdf';
                const prevUrl = `{r2_pdf_base_url}/${{prevPdf.id}}/${{prevFilename}}`;
                preloadFrame.src = prevUrl;
            }}
            
            if (index < filteredPDFs.length - 1) {{
                const nextPdf = filteredPDFs[index + 1];
                const nextFilename = nextPdf.pdf || nextPdf.id + '.pdf';
                const nextUrl = `{r2_pdf_base_url}/${{nextPdf.id}}/${{nextFilename}}`;
                setTimeout(() => {{
                    const nextFrame = document.createElement('iframe');
                    nextFrame.style.display = 'none';
                    nextFrame.src = nextUrl;
                }}, 100);
            }}
        }}
        
        function toggleQueue() {{
            const pdf = filteredPDFs[currentPDFIndex];
            const isChecked = document.getElementById('queueCheckbox').checked;
            
            if (isChecked) {{
                if (!processingQueue.includes(pdf.id)) {{
                    processingQueue.push(pdf.id);
                }}
            }} else {{
                processingQueue = processingQueue.filter(id => id !== pdf.id);
            }}
            
            localStorage.setItem('pdfProcessingQueue', JSON.stringify(processingQueue));
            updateQueueStatus();
        }}
        
        function updateQueueStatus() {{
            const statusDiv = document.getElementById('queueStatus');
            statusDiv.textContent = `Total in queue: ${{processingQueue.length}} PDFs`;
            
            // Update table to show queued items
            renderTable();
        }}
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (document.getElementById('previewModal').style.display === 'block') {{
                if (e.key === 'ArrowLeft') {{
                    navigatePDF(-1);
                }} else if (e.key === 'ArrowRight') {{
                    navigatePDF(1);
                }} else if (e.key === 'Escape') {{
                    closeModal();
                }}
            }}
        }});
        
        // Close modal when clicking outside
        window.onclick = function(event) {{
            const modal = document.getElementById('previewModal');
            if (event.target === modal) {{
                closeModal();
            }}
        }};
    </script>
</body>
</html>"""
    
    def get_inputs(self, pdf: PDFExample) -> List[Path]:
        """Dashboard depends on metadata."""
        # Return markdown files so dashboard rebuilds when PDFs are added/removed
        inputs = []
        for approach in pdf.approaches:
            inputs.append(approach.file)
        return inputs
    
    def get_outputs(self, pdf: PDFExample, context: TaskContext) -> List[Path]:
        """Output files - not used for batch tasks."""
        return []
    
    def get_batch_outputs(self, context: TaskContext) -> List[Path]:
        """Dashboard output file."""
        return [context.artifacts_dir / "dashboard.html"]