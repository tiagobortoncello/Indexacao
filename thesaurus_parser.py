# thesaurus_parser.py
def parse_sth_file(file_path):
    """
    Lê o arquivo sth.txt e retorna:
    - thesaurus: dicionário com todos os termos ativos
    - word_map: mapeamento de palavras (sinônimos, variações) → termo padrão
    """
    thesaurus = {}
    word_map = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # Dividir o conteúdo por blocos (cada termo)
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip() and not line.startswith('#')]
        if not lines:
            continue

        term = None
        use = None
        situacao = "Inativo"
        usado_por = []

        for line in lines:
            if not term and ':' not in line:
                term = line
            elif line.startswith('Use:'):
                use = line[len('Use:'):].strip()
            elif line.startswith('Situação:'):
                situacao = line[len('Situação:'):].strip()
            elif line.startswith('Usado por:'):
                sin_list = line[len('Usado por:'):].strip()
                usado_por = [s.strip() for s in sin_list.split(',') if s.strip()]

        # Só considera se estiver Ativo
        if situacao != 'Ativo':
            continue

        # O termo principal
        termo_padrao = use or term

        if not termo_padrao:
            continue

        # Adiciona o termo principal
        thesaurus[term] = termo_padrao
        word_map[term.lower()] = termo_padrao

        # Adiciona o "Use" como variação
        if use:
            word_map[use.lower()] = termo_padrao

        # Adiciona os "Usado por"
        for sin in usado_por:
            word_map[sin.lower()] = termo_padrao

    return thesaurus, word_map
