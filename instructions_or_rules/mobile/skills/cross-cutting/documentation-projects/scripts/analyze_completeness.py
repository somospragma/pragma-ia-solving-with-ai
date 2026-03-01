#!/usr/bin/env python3
"""
Documentation Completeness Analyzer

Analyzes documentation to identify missing content, empty sections, and unexplained TBDs.

Usage:
    python analyze_completeness.py path/to/docs/folder
    
Reports:
    - Documents with TBD markers
    - Empty or minimal sections
    - Documentation coverage estimate
    - Recommendations for gaps
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def analyze_file(filepath):
    """Analyze a single documentation file for completeness"""
    
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Count TBDs
    tbd_count = len([l for l in lines if 'tbd' in l.lower()])
    
    # Count meaningful content (non-empty, non-header, non-tbd)
    meaningful_lines = len([
        l for l in lines 
        if l.strip() and 
        not l.startswith('#') and 
        'tbd' not in l.lower() and
        not l.startswith('-') and
        len(l.strip()) > 5
    ])
    
    # Find empty sections (headers with minimal content below)
    empty_sections = []
    for i, line in enumerate(lines):
        if line.startswith('##'):
            # Check next 5 lines for content
            next_lines = lines[i+1:min(i+6, len(lines))]
            section_content = ''.join(next_lines).strip()
            if not section_content or section_content == 'TBD':
                empty_sections.append(line.strip())
    
    return {
        'lines': len(lines),
        'meaningful_lines': meaningful_lines,
        'tbd_count': tbd_count,
        'empty_sections': empty_sections,
        'completeness_estimate': min(100, max(0, meaningful_lines * 2)),  # Rough estimate
    }

def analyze_folder(docs_folder):
    """Analyze all documents in a folder"""
    
    folder = Path(docs_folder)
    if not folder.is_dir():
        print(f"[ERROR] Folder not found: {docs_folder}\n")
        return None
    
    print("DOCUMENTATION COMPLETENESS ANALYSIS")
    print("=" * 80)
    print(f"Folder: {docs_folder}\n")
    
    # Find all markdown files
    md_files = sorted(folder.glob('*.md'))
    
    if not md_files:
        print("[INFO] No markdown files found.\n")
        return None
    
    # Analyze each file
    results = {}
    for filepath in md_files:
        filename = filepath.name
        analysis = analyze_file(str(filepath))
        if analysis:
            results[filename] = analysis
    
    # Print detailed results
    print(f"{'Document':<30} {'Lines':<8} {'Meaningful':<12} {'TBDs':<6} {'Complete':<10}")
    print("-" * 80)
    
    total_tbd = 0
    total_meaningful = 0
    with_tbd = []
    with_empty = []
    
    for filename in sorted(results.keys()):
        data = results[filename]
        complete_pct = min(100, max(0, data['completeness_estimate']))
        
        print(f"{filename:<30} {data['lines']:<8} {data['meaningful_lines']:<12} "
              f"{data['tbd_count']:<6} {complete_pct}%")
        
        total_tbd += data['tbd_count']
        total_meaningful += data['meaningful_lines']
        
        if data['tbd_count'] > 0:
            with_tbd.append(filename)
        
        if data['empty_sections']:
            with_empty.append((filename, data['empty_sections']))
    
    print("-" * 80)
    print(f"\nSummary:")
    print(f"  Total TBD markers found: {total_tbd}")
    
    if with_tbd:
        print(f"\nDocuments with TBD markers:")
        for filename in with_tbd:
            tbd_count = results[filename]['tbd_count']
            print(f"  - {filename}: {tbd_count} TBD(s)")
    
    if with_empty:
        print(f"\nDocuments with empty sections:")
        for filename, sections in with_empty:
            print(f"  - {filename}:")
            for section in sections[:3]:  # Show first 3
                print(f"      {section}")
            if len(sections) > 3:
                print(f"      ... and {len(sections)-3} more")
    
    print("\nRecommendations:")
    print("  1. Address all TBD markers with real project data")
    print("  2. Remove empty sections or add meaningful content")
    print("  3. Ensure metadata (date, version, author) in each document")
    print("  4. Validate structure using validate_structure.py\n")
    
    return results

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyze_completeness.py path/to/docs\n")
        sys.exit(1)
    
    docs_folder = sys.argv[1]
    analyze_folder(docs_folder)
