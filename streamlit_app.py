# streamlit_app.py
import streamlit as st
from thesaurus_parser import parse_sth_file
import re

st.title("🔍 Indexador Automático com Thesaurus")
st.markdown("""
Cole um texto abaixo. O sistema vai identificar palavras e sugerir **termos padronizados** do thesaurus.
""")

# Carregar o thesaurus uma vez e armazenar em cache
@st.cache_data
def carregar_thesaurus():
    return parse_sth_file('sth.txt')

# Tentar carregar
try:
    thesaurus, word_map = carregar_thesaurus()
    st.success(f"✅ Thesaurus carregado! {len(thesaurus)} termos ativos.")
except Exception as e:
    st.error(f"❌ Erro ao carregar o arquivo 'sth.txt': {e}")
    st.stop()

# Campo para colar o texto
texto = st.text_area("Cole seu texto aqui:", height=200, placeholder="Ex: O funcionário desviou verbas públicas e cometeu peculato...")

if st.button("🔍 Sugerir Termos de Indexação"):
    if not texto.strip():
        st.warning("Por favor, cole um texto para análise.")
    else:
        # Extrair palavras do texto (simples, por palavras separadas)
        palavras = re.findall(r'\b[a-zA-ZÀ-ÿçÇãÃõÕ]+(?: [a-zA-ZÀ-ÿçÇãÃõÕ]+)*\b', texto.lower())
        
        # Encontrar correspondências
        termos_encontrados = set()
        detalhes = []

        for palavra in palavras:
            if palavra in word_map:
                termo_padrao = word_map[palavra]
                if termo_padrao not in termos_encontrados:
                    termos_encontrados.add(termo_padrao)
                    detalhes.append(f"🔹 `{palavra}` → **{termo_padrao}**")

        # Mostrar resultados
        if termos_encontrados:
            st.subheader("✅ Termos sugeridos para indexação:")
            st.markdown("\n".join(detalhes))
            st.markdown("---")
            st.markdown(f"**Total de termos sugeridos:** {len(termos_encontrados)}")
        else:
            st.info("❌ Nenhum termo do thesaurus foi encontrado no texto.")
