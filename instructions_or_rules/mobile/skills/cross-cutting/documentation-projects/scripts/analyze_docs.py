#!/usr/bin/env python3
"""
Analizador de Completitud de Documentación - Matriz Automatizada

Uso:
    python analyze_docs.py path/to/docs/folder
    
Output:
    Matriz de análisis completa con estado de cada documento
"""

import os
import re
from pathlib import Path
import json

# Patrones que sugieren datos específicos/sensibles en el contenido
SENSITIVE_PATTERNS = [
    r'https?://',                                          # URLs absolutas
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # emails
    r'\b(?:\d{1,3}\.){3}\d{1,3}\b',                      # IPs
    r'/home/\w+|/Users/\w+|C:\\\\Users\\\\',             # rutas absolutas
    r'sk-[A-Za-z0-9]{20,}',                               # API keys estilo OpenAI
    r'eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+',              # JWTs
    r'Bearer\s+[A-Za-z0-9\-_.]{10,}',                    # Bearer tokens
    r'(?i)password\s*[:=]\s*\S+',                         # passwords inline
    r'(?i)secret\s*[:=]\s*\S+',                           # secrets inline
    r'(?i)api[_-]?key\s*[:=]\s*\S+',                      # API keys inline
]

REQUIRED_DOCS = {
    'index.md': 'Guía de navegación',
    'project-overview.md': 'Visión, objetivos',
    'requirements.md': 'Requisitos funcionales y técnicos',
    'project-structure.md': 'Arquitectura, estructura',
    'tech-stack.md': 'Tecnologías, justificaciones',
    'features.md': 'Funcionalidades, características',
    'implementation.md': 'Guía de desarrollo, estándares',
    'user-flow.md': 'Flujos de usuario, datos',
}

def analyze_file(filepath):
    """Analiza un archivo markdown"""
    
    if not os.path.exists(filepath):
        return {
            'exists': False,
            'size': 0,
            'has_tbd': False,
            'has_headers': False,
            'genericidad': 'N/A'  # BUG FIXED: era 'genericidade' (typo)
        }
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_tbd = 'TBD' in content or 'tbd' in content
    has_headers = bool(content.count('#')) > 0
    size = len(content)
    
    # Detectar posibles datos específicos usando regex amplios
    has_specific_data = any(
        re.search(pattern, content) for pattern in SENSITIVE_PATTERNS
    )
    
    return {
        'exists': True,
        'size': size,
        'has_tbd': has_tbd,
        'has_headers': has_headers,
        'has_specific_data': has_specific_data,
        'genericidad': 'Específico' if has_specific_data else ('TBD' if has_tbd else 'Genérico'),
    }

def generate_matrix(docs_folder):
    """Genera matriz de análisis"""
    
    folder = Path(docs_folder)
    if not folder.is_dir():
        print(f"[ERROR] Carpeta no encontrada: {docs_folder}")
        return None
    
    print("\nANALISIS DE DOCUMENTACION")
    print("=" * 100)
    print(f"Carpeta analizada: {docs_folder}\n")
    
    # Encabezado
    print(f"{'Documento':<25} {'Existe':<10} {'Contenido':<12} {'Genérico':<15} {'Acción':<20}")
    print("-" * 100)
    
    results = {}
    total = len(REQUIRED_DOCS)
    found = 0
    
    for filename, description in REQUIRED_DOCS.items():
        filepath = folder / filename
        analysis = analyze_file(str(filepath))
        
        results[filename] = analysis
        
        # Determinar estado
        if not analysis['exists']:
            estado = '[NO]'
            contenido = 'N/A'
            genericity = 'N/A'
            accion = 'CREAR'
        else:
            found += 1
            estado = '[SÍ]'
            
            if analysis['size'] < 100:
                contenido = '[Mínimo]'
            elif analysis['has_tbd']:
                contenido = '[Parcial]'
            else:
                contenido = '[Completo]'
            
            genericity = analysis['genericidad']
            
            if analysis['has_tbd']:
                accion = 'COMPLETAR'
            elif analysis['has_specific_data']:
                accion = 'GENERALIZAR'
            else:
                accion = 'LISTO'
        
        print(f"{filename:<25} {estado:<10} {contenido:<12} {genericity:<15} {accion:<20}")
    
    print("-" * 100)
    print(f"\nResumen: {found}/{total} documentos encontrados ({found*100//total}%)")
    print("=" * 100 + "\n")
    
    return results

def export_matrix_json(results, output_file):
    """Exporta matriz a JSON"""
    
    matrix_data = {
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'documents': results
    }
    
    with open(output_file, 'w') as f:
        json.dump(matrix_data, f, indent=2)
    
    print(f"[OK] Matriz exportada a: {output_file}\n")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python analyze_docs.py path/to/docs")
        sys.exit(1)
    
    docs_folder = sys.argv[1]
    results = generate_matrix(docs_folder)
    
    if results:
        output = Path(docs_folder).parent / 'documentation-analysis.json'
        export_matrix_json(results, str(output))
