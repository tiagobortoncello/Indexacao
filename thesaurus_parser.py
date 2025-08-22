# thesaurus_parser.py

import re
import json

def parse_sth_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    terms = {}
    current_term = None

    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Novo termo (não começa com Use:, TG:, etc.)
        if line.startswith(('Use:', 'Situação:', 'Def.:', 'TG:', 'TE:', 'TR:', 'Usado por:', 'NE:', 'NH:')):
            pass
        else:
            parts = re.split(r'\s+Use:\s+', line, maxsplit=1)
            term = parts[0].strip()
            current_term = term
            if current_term not in terms:
                terms[current_term] = {
                    'use': term,
                    'definicao': '',
                    'tg': '',
                    'te': [],
                    'tr': [],
                    'usado_por': [],
                    'situacao': 'Ativo'
                }

        # Preencher campos
        if current_term and line.startswith('Use:'):
            terms[current_term]['use'] = line.replace('Use:', '').strip()
        elif current_term and line.startswith('Situação:'):
            terms[current_term]['situacao'] = line.replace('Situação:', '').strip()
        elif current_term and line.startswith('Def.:'):
            terms[current_term]['definicao'] = line.replace('Def.:', '').strip()
        elif current_term and line.startswith('TG:'):
            terms[current_term]['tg'] = line.replace('TG:', '').strip()
        elif current_term and line.startswith('TE:'):
            te = line.replace('TE:', '').strip()
            terms[current_term]['te'] = [t.strip() for t in te.split(',') if t.strip()]
        elif current_term and line.startswith('TR:'):
            tr = line.replace('TR:', '').strip()
            terms[current_term]['tr'] = [t.strip() for t in tr.split(',') if t.strip()]
        elif current_term and line.startswith('Usado por:'):
            usado = line.replace('Usado por:', '').strip()
            terms[current_term]['usado_por'] = [t.strip() for t in usado.split(',') if t.strip()]

    return terms