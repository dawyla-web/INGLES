import streamlit as st
import requests
import speech_recognition as sr
import streamlit.components.v1 as components
import difflib
import random # <--- Biblioteca para sortear
from audio_recorder_streamlit import audio_recorder

# --- Configuração da Página ---
st.set_page_config(page_title="English Master Suite", layout="centered", page_icon="🇬🇧")# --- CÓDIGO FORÇA BRUTA (COM !IMPORTANT) ---
hide_elements = """
    <style>
    /* 1. MANTÉM O MENU (Barra superior visível) */
    header {visibility: visible !important;}
    
    /* 2. ESCONDE O RODAPÉ (Força bruta) */
    footer {visibility: hidden !important; display: none !important;}
    
    /* 3. ESCONDE O BOTÃO VERMELHO (Várias tentativas de alvo para garantir) */
    .stDeployButton {visibility: hidden !important; display: none !important;}
    [data-testid="stDeployButton"] {visibility: hidden !important; display: none !important;}
    
    /* 4. ESCONDE A BARRA COLORIDA */
    [data-testid="stDecoration"] {visibility: hidden !important; display: none !important;}
    
    /* 5. AJUSTE DO TOPO */
    .block-container {
        padding-top: 3rem !important;
    }
    </style>
"""
st.markdown(hide_elements, unsafe_allow_html=True)
# ---------------------------------------------
# ---------------------------------------------
# ---------------------------------------------
# ---------------------------------------------
# ------------------------------------------

# --- MENU PRINCIPAL ---
st.sidebar.title("🇬🇧 English Master")
app_mode = st.sidebar.selectbox("Escolha a Ferramenta:", ["📖 Dicionário & Conjugador", "🎙️ Treino de Pronúncia"])
st.sidebar.divider()

# ==============================================================================
# FERRAMENTA 1: DICIONÁRIO E CONJUGADOR
# ==============================================================================
if app_mode == "📖 Dicionário & Conjugador":
    st.title("📖 Dicionário & Conjugador")

    # --- Banco de Dados Simplificado ---
    irregulars_db = {
        "be": {"past": "was/were", "participle": "been"},
        "become": {"past": "became", "participle": "become"},
        "begin": {"past": "began", "participle": "begun"},
        "break": {"past": "broke", "participle": "broken"},
        "buy": {"past": "bought", "participle": "bought"},
        "come": {"past": "came", "participle": "come"},
        "do": {"past": "did", "participle": "done"},
        "drink": {"past": "drank", "participle": "drunk"},
        "drive": {"past": "drove", "participle": "driven"},
        "eat": {"past": "ate", "participle": "eaten"},
        "go": {"past": "went", "participle": "gone"},
        "have": {"past": "had", "participle": "had"},
        "know": {"past": "knew", "participle": "known"},
        "make": {"past": "made", "participle": "made"},
        "see": {"past": "saw", "participle": "seen"},
        "speak": {"past": "spoke", "participle": "spoken"},
        "take": {"past": "took", "participle": "taken"},
        "think": {"past": "thought", "participle": "thought"},
        "write": {"past": "wrote", "participle": "written"},
    }
    
    # --- Funções ---
    def speak_text_js(text):
        html_code = f"""
        <html><body><script>
        function speak() {{
            var msg = new SpeechSynthesisUtterance("{text}");
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        }}
        </script>
        <button onclick="speak()" style="background-color:#4CAF50;border:none;color:white;padding:5px 15px;border-radius:5px;cursor:pointer;font-size:12px;">
        🔊 Ouvir: "{text}"
        </button></body></html>
        """
        return html_code

    def manual_conjugate(verb, tense, pronoun):
        if verb in irregulars_db:
            past = irregulars_db[verb]["past"]
            participle = irregulars_db[verb]["participle"]
        else:
            past = verb + "d" if verb.endswith('e') else verb + "ed"
            participle = past

        if tense == "Simple Present":
            if verb == "be":
                if pronoun == "I": return "I am"
                elif pronoun in ["He", "She", "It"]: return f"{pronoun} is"
                else: return f"{pronoun} are"
            if pronoun in ["He", "She", "It"]:
                if verb == "have": return f"{pronoun} has"
                if verb == "go": return f"{pronoun} goes"
                if verb == "do": return f"{pronoun} does"
                return f"{pronoun} {verb}s"
            return f"{pronoun} {verb}"

        elif tense == "Simple Past":
            if verb == "be": return f"{pronoun} was" if pronoun in ["I", "He", "She", "It"] else f"{pronoun} were"
            return f"{pronoun} {past}"

        elif tense == "Future (Will)":
            return f"{pronoun} will {verb}"

        elif tense == "Present Perfect":
            aux = "has" if pronoun in ["He", "She", "It"] else "have"
            return f"{pronoun} {aux} {participle}"
        
        return "Tempo não configurado neste modo simples."

    def get_dictionary_data(word):
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            if response.status_code == 200:
                data = response.json()[0]
                example = None
                meanings = data.get('meanings', [])
                if meanings:
                    for definition in meanings[0]['definitions']:
                        if 'example' in definition:
                            example = definition['example']
                            break
                return {"example": example}
        except: pass
        return None

    # --- Interface do Conjugador ---
    st.sidebar.subheader("Filtros do Dicionário")
    verb_input = st.sidebar.text_input("Digite um verbo:", value="go").lower().strip()
    pronoun = st.sidebar.selectbox("Pronome:", ["I", "You", "He", "She", "It", "We", "They"])
    tense = st.sidebar.selectbox("Tempo Verbal:", ["Simple Present", "Simple Past", "Future (Will)", "Present Perfect"])

    if st.sidebar.button("Pesquisar ▶️"):
        st.divider()
        result = manual_conjugate(verb_input, tense, pronoun)
        st.subheader(f"Verbo: {verb_input.upper()}")
        st.markdown(f"### Tempo: *{tense}*")
        st.success(f"🗣️ **{result}**")
        components.html(speak_text_js(result), height=50)

        st.markdown("---")
        st.write("### 🌍 Exemplo Real")
        with st.spinner("Buscando exemplo..."):
            api_data = get_dictionary_data(verb_input)
            if api_data and api_data['example']:
                clean_example = api_data['example'].replace("'", "")
                st.warning(f"**Frase:** _{api_data['example']}_")
                components.html(speak_text_js(clean_example), height=50)
            else:
                st.info("Nenhum exemplo encontrado.")

# ==============================================================================
# FERRAMENTA 2: LABORATÓRIO DE PRONÚNCIA
# ==============================================================================
elif app_mode == "🎙️ Treino de Pronúncia":
    st.title("🎙️ Laboratório de Pronúncia")

    # --- Funções Específicas ---
    def speak_text_js_pronuncia(text):
        html_code = f"""
        <html><body><script>
        function speak() {{
            var msg = new SpeechSynthesisUtterance("{text}");
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        }}
        </script>
        <button onclick="speak()" style="background-color:#E8B62C;border:none;color:black;padding:10px 20px;border-radius:8px;cursor:pointer;font-weight:bold;">
        🔊 Ouvir Modelo
        </button></body></html>
        """
        return html_code

    def recognize_audio(audio_bytes):
        r = sr.Recognizer()
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
        with sr.AudioFile("temp_audio.wav") as source:
            try:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data, language="en-US")
                return text.lower()
            except: return "error"

    def calculate_score(target, spoken):
        matcher = difflib.SequenceMatcher(None, target.lower(), spoken.lower())
        return int(matcher.ratio() * 100)

    # --- Banco de Frases Expandido ---
    practice_sentences = {
        "Nível 1 (Básico)": [
            "I like to study", 
            "The book is on the table", 
            "Can you help me?", 
            "I love pizza",
            "My name is John"
        ],
        "Nível 2 (Intermediário)": [
            "I went to the park yesterday", 
            "She has bought a new car", 
            "They are playing soccer",
            "We have been there before"
        ],
        "Nível 3 (Avançado)": [
            "Three witches watch three swatch watches", 
            "The quick brown fox jumps over the lazy dog",
            "I thought a thought but the thought I thought was not the thought I thought I thought"
        ]
    }

    st.sidebar.subheader("Configurações de Treino")
    
    # 1. Escolha do Nível
    level = st.sidebar.selectbox("Escolha o Nível:", list(practice_sentences.keys()))
    
    # --- NOVA LÓGICA DO BOTÃO "SORTEAR" ---
    
    # Se ainda não tem uma frase na memória, pega a primeira
    if 'current_sentence' not in st.session_state:
        st.session_state['current_sentence'] = practice_sentences[level][0]

    # Botão para sortear
    if st.sidebar.button("🎲 Sortear Nova Frase"):
        lista_atual = practice_sentences[level]
        # Escolhe aleatoriamente
        nova_frase = random.choice(lista_atual)
        st.session_state['current_sentence'] = nova_frase
    
    # Mostra a frase que está na memória (session_state)
    # Nota: Se você mudar de nível, clique em "Sortear" para atualizar a lista
    sentence = st.session_state['current_sentence']
    
    st.sidebar.info(f"Frase atual: {sentence}")
    # ---------------------------------------

    st.subheader("🎯 Frase Alvo:")
    st.markdown(f"## *{sentence}*")
    components.html(speak_text_js_pronuncia(sentence), height=50)

    st.divider()
    st.info("Clique no microfone para gravar e testar sua nota!")

    audio_bytes = audio_recorder(text="", recording_color="#e8b62c", neutral_color="#6aa36f", icon_name="microphone", icon_size="3x")

    if audio_bytes:
        spoken_text = recognize_audio(audio_bytes)
        if spoken_text == "error":
            st.error("Não entendi. Tente de novo.")
        else:
            score = calculate_score(sentence, spoken_text)
            st.write("---")
            col1, col2 = st.columns(2)
            with col1: st.info(f"👂 **Eu entendi:**\n'{spoken_text}'")
            with col2:
                if score == 100: st.success(f"🏆 **{score}/100** - PERFEITO!")
                elif score > 80: st.success(f"✅ **{score}/100** - Muito bom!")
                else: st.warning(f"⚠️ **{score}/100** - Tente de novo.")