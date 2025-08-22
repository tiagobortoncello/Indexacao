# streamlit_app.py

import streamlit as st
import re
from thesaurus_parser import parse_sth_file

# Carregar o thesaurus (faz isso uma vez)
@st.cache_data
def carregar_thesaurus():
    data = parse_sth_file('sth..txt')
    # Criar um mapeamento de palavras para termos
    word_to_terms = {}
    for termo, info in data.items():
        if info['situacao'] != 'Ativo':
            continue
        # Adiciona o termo principal
        word_to_terms[termo.lower()] = info
        # Adiciona "Usado por"
        for sin in info.get('usado_por', []):
            word_to_terms[sin.lower()] = info
    return data, word_to_terms

st.title("🔍 Indexador Automático com Thesaurus")

st.markdown("""
> Cole um texto abaixo. O sistema vai sugerir **termos padronizados** do thesaurus.
""")

# Carregar dados
try:
    thesaurus, word_map = carregar_thesaurus()
    st.success(f"✅ Thesaurus carregado! {len(thesaurus)} termos ativos.")
except Exception as e:
    st.error(f"❌ Erro ao carregar o thesaurus: {e}")
    st.stop()

# Campo de texto
texto = st.text_area("Cole seu texto aqui:", height=200)

if st.button("Sugerir Termos"):
    if not texto.strip():
        st.warning("Por favor, cole um texto.")
    else:
        texto_lower = texto.lower()
        encontrado = {}

        for palavra, info in word_map.items():
            if re.search(r'\b' + re.escape(palavra) + r'\b', texto_lower):
                use = info['use']
                if use not in encontrado:
                    encontrado[use] = info

        if encontrado:
            st.markdown("### 🎯 Termos Sugeridos")
            for termo, info in encontrado.items():
                with st.expander(f"**{termo}**"):
                    st.write(f"**Termo original:** {info.get('use', '')}")
                    if info.get('definicao'):
                        st.write(f"*{info['definicao']}*")
                    if info.get('tg'):
                        st.write(f"🔹 Geral: {info['tg']}")
        else:
            st.info("Nenhum termo do thesaurus foi encontrado no texto.")