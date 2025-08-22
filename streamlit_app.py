# streamlit_app.py

import streamlit as st
import re
import json

# Carregar o mapeamento de termos autorizados
@st.cache_data
def carregar_mapeamento():
    try:
        with open('termos_autorizados.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Arquivo `termos_autorizados.json` não encontrado. Execute `thesaurus_parser.py` primeiro.")
        return {}

st.title("🔍 Indexador de Termos Autorizados")

st.markdown("""
> Cole um texto abaixo. O sistema identifica termos e sugere **apenas as formas autorizadas** do thesaurus.
""")

# Carregar mapeamento
mapa = carregar_mapeamento()

if not mapa:
    st.stop()

st.success(f"✅ Base carregada! {len(mapa)} variações mapeadas para termos autorizados.")

# Campo de texto
texto = st.text_area("Cole seu texto aqui:", height=200, key="input_text")

if st.button("Sugerir Termos Autorizados"):
    if not texto.strip():
        st.warning("Por favor, cole um texto para análise.")
    else:
        texto_lower = texto.lower()
        encontrado = set()

        # Busca por correspondência exata de palavras
        for variacao, termo_autorizado in mapa.items():
            if re.search(r'\b' + re.escape(variacao) + r'\b', texto_lower):
                encontrado.add(termo_autorizado)

        if encontrado:
            st.markdown("### 🎯 Termos Autorizados Sugeridos")
            for termo in sorted(encontrado):
                st.markdown(f"- **{termo}**")
            st.markdown("---")
            st.markdown("### 📥 Termos para indexação (copia e cola)")
            st.code(", ".join(sorted(encontrado)), language="text")
        else:
            st.info("Nenhum termo do thesaurus foi encontrado no texto.")
