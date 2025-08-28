# streamlit_app.py
import streamlit as st
from thesaurus_parser import parse_sth_file
import re

st.title("🔍 Indexador Automático com Thesaurus")
st.markdown("""
Cole um texto abaixo. O sistema vai identificar palavras e sugerir **termos padronizados** do thesaurus.
""")

@st.cache_data
def carregar_thesaurus():
    return parse_sth_file('sth.txt')

try:
    thesaurus, word_map = carregar_thesaurus()
    st.success(f"✅ Thesaurus carregado! {len(word_map)} variações mapeadas.")
except Exception as e:
    st.error(f"❌ Erro ao carregar o arquivo 'sth.txt': {e}")
    st.stop()

texto = st.text_area("Cole seu texto aqui:", height=200, placeholder="Ex: O servidor fez um acordo judicial e pagou imposto atrasado...")

if st.button("🔍 Sugerir Termos de Indexação"):
    if not texto.strip():
        st.warning("Por favor, cole um texto para análise.")
    else:
        # Extrair frases e palavras do texto
        palavras = re.findall(r'\b[a-zA-ZÀ-ÿçÇãÃõÕ]+\b', texto.lower())
        frases = re.findall(r'\b[a-zA-ZÀ-ÿçÇãÃõÕ]+(?:\s+[a-zA-ZÀ-ÿçÇãÃõÕ]+){1,3}\b', texto.lower())

        # Procurar correspondências (do maior para o menor, para pegar frases primeiro)
        termos_encontrados = set()
        detalhes = []

        # Primeiro: frases (2-4 palavras)
        for frase in sorted(frases, key=len, reverse=True):
            if frase in word_map:
                termo = word_map[frase]
                if termo not in termos_encontrados:
                    termos_encontrados.add(termo)
                    detalhes.append(f"🔹 `{frase}` → **{termo}**")

        # Depois: palavras únicas
        for palavra in palavras:
            if palavra in word_map:
                termo = word_map[palavra]
                if termo not in termos_encontrados:
                    termos_encontrados.add(termo)
                    detalhes.append(f"🔹 `{palavra}` → **{termo}**")

        if termos_encontrados:
            st.subheader("✅ Termos sugeridos para indexação:")
            st.markdown("\n".join(detalhes))
            st.markdown("---")
            st.markdown(f"**Total de termos sugeridos:** {len(termos_encontrados)}")
        else:
            st.info("❌ Nenhum termo do thesaurus foi encontrado no texto.")
            st.markdown("💡 Dica: Tente palavras como *acordo*, *imposto*, *serviço*, *abono*, *viagem a serviço*.")
