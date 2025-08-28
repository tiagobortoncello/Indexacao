# thesaurus_parser.py
import re

def parse_sth_file(file_path):
    """
    Lê e corrige o arquivo sth.txt mal formatado.
    Retorna:
    - thesaurus: dicionário com termos ativos
    - word_map: mapeia sinônimos → termo padrão
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # Substitui quebras de linha erradas e normaliza
    content = re.sub(r'\n+', '\n', content)  # Remove múltiplas quebras
    content = re.sub(r'\s+', ' ', content)  # Normaliza espaços
    content = content.replace('Situação: Ativo', '\nSituação: Ativo')
    content = content.replace('Situação: Inativo', '\nSituação: Inativo')

    # Divide por blocos (onde há "Situação: Ativo" ou "Situação: Inativo")
    blocks = []
    current = ""
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if 'Situação: ' in line:
            if current:
                blocks.append(current + " " + line)
            else:
                blocks.append(line)
            current = ""
        else:
            if not current:
                current = line
            else:
                current += " " + line

    if current:
        blocks.append(current)

    thesaurus = {}
    word_map = {}

    for block in blocks:
        block = block.strip()
        if not block or 'Situação: Inativo' in block:
            continue

        # Extrair campos
        term_match = re.match(r'^([^U][^S][^T][^N][^H][^D][^A][^C][^E][^F][^G][^L][^M][^O][^P][^Q][^R][^I][^J][^K][^X][^Y][^Z][^W][^0-9][^ ]+)', block)
        if not term_match:
            continue

        term = term_match.group(1).strip()

        use_match = re.search(r'Use:\s*([^S][^I][^T][^U][^A][^C][^A][^O][^:]+?)(?:\s+[A-Z]+:|$)', block)
        use = use_match.group(1).strip() if use_match else None

        usado_por_match = re.search(r'Usado por:\s*([^N][^E][^:]+?)(?:\s+[A-Z]+:|$)', block)
        usado_por = [s.strip() for s in usado_por_match.group(1).split(',')] if usado_por_match else []

        # Só se for Ativo
        if 'Situação: Ativo' not in block:
            continue

        termo_padrao = use or term

        # Mapear termo principal
        word_map[term.lower()] = termo_padrao
        if use:
            word_map[use.lower()] = termo_padrao
        for sin in usado_por:
            word_map[sin.lower()] = termo_padrao

        thesaurus[term] = termo_padrao

    return thesaurus, word_map
