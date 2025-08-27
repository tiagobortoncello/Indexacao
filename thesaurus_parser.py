# thesaurus_parser.py
def parse_sth_file(file_path):
    """
    Faz o parsing do arquivo sth.txt e retorna um dicionário com os termos,
    seus 'Use', 'Situação', 'Def.', 'Usado por', etc.
    """
    data = {}
    current_term = None
    current_info = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo: {e}")

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Detecta início de novo termo (linhas sem "Use:", "Situação:", etc.)
        if ':' not in line or not any(
            line.startswith(prefix) for prefix in [
                'Use:', 'Situação:', 'Def.:', 'TG:', 'TE:', 'TR:', 'Usado por:', 'NE:', 'NH:'
            ]
        ):
            # Finaliza o termo anterior
            if current_term:
                data[current_term] = current_info
            # Inicia novo termo
            current_term = line
            current_info = {
                'use': None,
                'situacao': 'Inativo',
                'definicao': None,
                'usado_por': [],
                'tg': None,
                'te': [],
                'tr': []
            }
        elif line.startswith('Use:'):
            current_info['use'] = line[len('Use:'):].strip()
        elif line.startswith('Situação:'):
            current_info['situacao'] = line[len('Situação:'):].strip()
        elif line.startswith('Def.:'):
            current_info['definicao'] = line[len('Def.:'):].strip()
        elif line.startswith('Usado por:'):
            usados = line[len('Usado por:'):].strip()
            current_info['usado_por'].extend([u.strip() for u in usados.split(',') if u.strip()])
        elif line.startswith('TG:'):
            current_info['tg'] = line[len('TG:'):].strip()
        elif line.startswith('TE:'):
            te = line[len('TE:'):].strip()
            if te:
                current_info['te'].append(te)
        elif line.startswith('TR:'):
            tr = line[len('TR:'):].strip()
            if tr:
                current_info['tr'].append(tr)
        elif line.startswith('NE:') or line.startswith('NH:'):
            # Ignorar por enquanto ou armazenar se necessário
            pass

    # Adiciona o último termo
    if current_term and current_info:
        data[current_term] = current_info

    return data
