# streamlit_app.py
import streamlit as st
from thesaurus_parser import parse_sth_file

st.title("🔍 Indexador Automático com Thesaurus")
st.markdown("Este app usa um thesaurus para sugerir termos padronizados a partir de palavras digitadas.")

@st.cache_data
def carregar_dados():
    try:
        data = parse_sth_file('sth.txt')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo 'sth.txt': {e}")
        return {}
    
    # Criar mapeamento de palavras para termos (inclui "Use", "Usado por", etc.)
    word_to_terms = {}
    for termo, info in data.items():
        if info['situacao'] != 'Ativo':
            continue
        # Termo principal
        word_to_terms[termo.lower()] = info
        # "Use" como sinônimo
        if info['use']:
            word_to_terms[info['use'].lower()] = info
        # "Usado por"
        for sin in info.get('usado_por', []):
            word_to_terms[sin.lower()] = info
    return word_to_terms

word_to_terms = carregar_dados()

if not word_to_terms:
    st.stop()

# Campo de entrada
entrada = st.text_input("Digite um termo para buscar no thesaurus:")

if entrada:
    entrada_lower = entrada.strip().lower()
    if entrada_lower in word_to_terms:
        info = word_to_terms[entrada_lower]
        st.success("✅ Termo encontrado!")
        st.write(f"**Termo principal (Use):** {info['use']}")
        if info['definicao']:
            st.write(f"**Definição:** {info['definicao']}")
        if info.get('usado_por'):
            st.write(f"**Sinônimos (Usado por):** {', '.join(info['usado_por'])}")
        if info.get('tg'):
            st.write(f"**Termo genérico (TG):** {info['tg']}")
        if info.get('te'):
            st.write(f"**Termos específicos (TE):** {', '.join(info['te'])}")
        if info.get('tr'):
            st.write(f"**Termos relacionados (TR):** {', '.join(info['tr'])}")
    else:
        st.info("❌ Termo não encontrado.")
        # Sugestões parciais
        sugestoes = [term for term in word_to_terms.keys() if entrada_lower in term]
        if sugestoes:
            st.write("**Possíveis correspondências:**")
            for s in sugestoes[:10]:
                st.write(f"- {s.title()}")
