import streamlit as st
import requests
import fitz  # PyMuPDF
import random

st.title("Auto Quiz Generator from GitHub PDF")

@st.cache_data
def fetch_pdf_text(raw_url):
    response = requests.get(raw_url)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)
    doc = fitz.open("temp.pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_word_pairs(text):
    pairs = []
    lines = text.split("\n")
    for line in lines:
        try:
            line = line.strip()
            if not line or "-" not in line:
                continue
            parts = line.split("-")
            if len(parts) != 2:
                continue
            german, english = map(str.strip, parts)
            if german and english:
                pairs.append((german, english))
        except:
            continue
    return pairs

def run_quiz(pairs):
    random.shuffle(pairs)
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.score = 0

    if st.session_state.q_index < len(pairs):
        german, correct = pairs[st.session_state.q_index]
        options = [correct]
        while len(options) < 4:
            _, fake = random.choice(pairs)
            if fake not in options:
                options.append(fake)
        random.shuffle(options)

        st.write(f"**Q{st.session_state.q_index + 1}: What is the English translation of '{german}'?**")
        choice = st.radio("Choose one:", options, key=f"choice_{st.session_state.q_index}")
        if st.button("Submit"):
            if choice == correct:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct answer: {correct}")
            st.session_state.q_index += 1
            st.experimental_rerun()
    else:
        st.success(f"Quiz Complete! Score: {st.session_state.score}/{len(pairs)}")
        if st.button("Restart"):
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.experimental_rerun()

# --- MAIN APP ---

pdf_url = st.text_input("Enter RAW GitHub PDF URL:")

if pdf_url:
    try:
        with st.spinner("Reading and extracting..."):
            pdf_text = fetch_pdf_text(pdf_url)
            word_pairs = extract_word_pairs(pdf_text)
        if word_pairs:
            st.success(f"Loaded {len(word_pairs)} word pairs.")
            run_quiz(word_pairs)
        else:
            st.warning("No valid word pairs found in the PDF.")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
