# thesaurus_parser.py

import re
import json

def parse_sth_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dividir por blocos (cada termo começa com uma linha que não é campo)
    lines = content.split('\n')
    terms = {}
    current_term = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith('NH:') or line.startswith('Def.:') or line.startswith('NE:'):
            continue  # Ignora definições, notas, origens

        # Detecta novo termo (não começa com Use:, TG:, etc.)
        if not line.startswith(('Use:', 'Situação:', 'TG:', 'TE:', 'TR:', 'Usado por:', 'NE:', 'Def.:')):
            # Extrai o termo principal (antes do "Use:", se houver)
            parts = re.split(r'\s+Use:\s+', line, maxsplit=1)
            term = parts[0].strip()
            current_term = term
            if current_term not in terms:
                terms[current_term] = {
                    'use': current_term,  # padrão: ele mesmo
                    'usado_por': [],
                    'situacao': 'Ativo'
                }

        # Preenche os campos
        if current_term and line.startswith('Use:'):
            use_term = line.replace('Use:', '').strip()
            terms[current_term]['use'] = use_term

        elif current_term and line.startswith('Situação:'):
            situacao = line.replace('Situação:', '').strip()
            terms[current_term]['situacao'] = situacao

        elif current_term and line.startswith('Usado por:'):
            usado_por = line.replace('Usado por:', '').strip()
            if usado_por:
                terms[current_term]['usado_por'] = [t.strip() for t in usado_por.split(',') if t.strip()]

    # Filtra apenas termos ATIVOS
    termos_ativos = {t: info for t, info in terms.items() if info['situacao'] == 'Ativo'}

    # Mapeia: todas as formas (sinônimos, usado por) → termo autorizado final
    mapa_termos = {}

    for termo, info in termos_ativos.items():
        # Encadeia o "Use:" até o final
        atual = info['use']
        while atual in termos_ativos and termos_ativos[atual]['use'] != atual:
            atual = termos_ativos[atual]['use']

        # Adiciona o termo principal
        mapa_termos[termo.lower()] = atual

        # Adiciona todos os "Usado por"
        for sin in info.get('usado_por', []):
            mapa_termos[sin.lower()] = atual

    return mapa_termos

# Gera o mapeamento final
if __name__ == '__main__':
    mapping = parse_sth_file('sth..txt')
    with open('termos_autorizados.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(mapping)} formas mapeadas para termos autorizados.")
    print("Arquivo salvo: termos_autorizados.json")
