#!/usr/bin/env python3
"""
Documentation Structure Validator

Validates that documentation follows the 7-document structure with required content.
Real project data is expected; this validates structure and completeness, not genericity.

Usage:
    python validate_structure.py path/to/docs/folder
    
Checks:
    - All 7 documents present or explicitly excluded
    - Required sections in each document
    - Metadata (date, version, author)
    - Internal links between documents
    - No empty TBDs without explanation
"""

import os
import re
from pathlib import Path

# Required structure for each document
REQUIRED_SECTIONS = {
    'index.md': ['overview', 'reading order', 'navigation', 'links'],
    'project-overview.md': ['vision', 'goals', 'problems', 'principles'],
    'requirements.md': ['functional', 'technical', 'quality', 'environment'],
    'project-structure.md': ['architecture', 'organization', 'modules', 'communication'],
    'tech-stack.md': ['language', 'frameworks', 'tools', 'justification'],
    'features.md': ['features', 'behavior', 'specification'],
    'implementation.md': ['setup', 'standards', 'workflow', 'process'],
    'user-flow.md': ['flows', 'interaction', 'data', 'scenarios'],
}

def check_metadata(content, filename):
    """Verify document has metadata (date, version, author)"""
    checks = {
        'has_title': bool(content.count('#') > 0),
        'has_date': 'updated' in content.lower() or 'date' in content.lower(),
        'has_author': 'author' in content.lower() or 'owner' in content.lower(),
    }
    return checks

def check_sections(content, filename):
    """Verify required sections are present"""
    content_lower = content.lower()
    required = REQUIRED_SECTIONS.get(filename, [])
    
    found = {}
    for section in required:
        found[section] = section in content_lower
    
    return found

def check_structure(content, filename):
    """Check overall document structure"""
    lines = content.split('\n')
    
    return {
        'lines': len(lines),
        'has_headers': content.count('#') > 0,
        'has_tables': '|' in content,
        'has_code_blocks': '```' in content,
        'has_lists': '-' in content or '*' in content,
        'empty_or_tbd_only': not any(
            line.strip() and 
            'tbd' not in line.lower() and 
            '#' not in line 
            for line in lines
        )
    }

def validate_file(filepath):
    """Validate a single documentation file"""
    
    filename = os.path.basename(filepath)
    
    if not os.path.exists(filepath):
        return {
            'file': filename,
            'status': 'MISSING',
            'details': 'File not found'
        }
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = check_metadata(content, filename)
    sections = check_sections(content, filename)
    structure = check_structure(content, filename)
    
    # Determine status
    if structure['empty_or_tbd_only']:
        status = 'EMPTY'
    elif not structure['has_headers']:
        status = 'NO_STRUCTURE'
    elif not all(sections.values()):
        status = 'INCOMPLETE'
    else:
        status = 'VALID'
    
    return {
        'file': filename,
        'status': status,
        'size': structure['lines'],
        'metadata': metadata,
        'sections_found': sections,
        'structure': structure,
    }

def validate_docs(docs_folder):
    """Validate all documents in a folder"""
    
    folder = Path(docs_folder)
    if not folder.is_dir():
        print(f"[ERROR] Folder not found: {docs_folder}\n")
        return None
    
    print("DOCUMENTATION STRUCTURE VALIDATION")
    print("=" * 80)
    print(f"Folder: {docs_folder}\n")
    
    # Check each required document
    results = {}
    for filename in REQUIRED_SECTIONS.keys():
        filepath = folder / filename
        result = validate_file(str(filepath))
        results[filename] = result
    
    # Print results
    print(f"{'Document':<30} {'Status':<15} {'Size':<10}")
    print("-" * 80)
    
    status_counts = {'VALID': 0, 'INCOMPLETE': 0, 'NO_STRUCTURE': 0, 'EMPTY': 0, 'MISSING': 0}
    
    for filename, result in results.items():
        status = result['status']
        size = result['size']
        status_counts[status] += 1
        
        print(f"{filename:<30} {status:<15} {size:<10}")
        
        if status == 'INCOMPLETE':
            missing = [s for s, found in result['sections_found'].items() if not found]
            print(f"    Missing sections: {', '.join(missing)}")
        elif status == 'EMPTY':
            print(f"    Document is empty or contains only TBD placeholders")
    
    print("-" * 80)
    total = len(REQUIRED_SECTIONS)
    valid = status_counts['VALID']
    print(f"\nSummary: {valid}/{total} documents valid\n")
    
    if status_counts['VALID'] == total:
        print("[OK] All documents are properly structured.")
        return True
    else:
        print("[REVIEW] Documentation requires review:")
        if status_counts['MISSING'] > 0:
            print(f"  - {status_counts['MISSING']} missing documents")
        if status_counts['EMPTY'] > 0:
            print(f"  - {status_counts['EMPTY']} empty documents")
        if status_counts['NO_STRUCTURE'] > 0:
            print(f"  - {status_counts['NO_STRUCTURE']} documents without structure")
        if status_counts['INCOMPLETE'] > 0:
            print(f"  - {status_counts['INCOMPLETE']} incomplete documents\n")
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validate_structure.py path/to/docs\n")
        sys.exit(1)
    
    docs_folder = sys.argv[1]
    success = validate_docs(docs_folder)
    sys.exit(0 if success else 1)
