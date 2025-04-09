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
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.choices = {}

    total_questions = len(pairs)

    if st.session_state.q_index >= total_questions:
        st.success(f"Quiz Complete! Final Score: {st.session_state.score} / {total_questions}")
        if st.button("Restart Quiz"):
            for key in ["q_index", "score", "submitted", "choices"]:
                st.session_state.pop(key, None)
            st.rerun()
        return  # Stop here

    current_q = st.session_state.q_index
    german, correct = pairs[current_q]

    # Generate consistent options per question
    if current_q not in st.session_state.choices:
        options = [correct]
        while len(options) < 4:
            _, fake = random.choice(pairs)
            if fake not in options:
                options.append(fake)
        random.shuffle(options)
        st.session_state.choices[current_q] = options
    else:
        options = st.session_state.choices[current_q]

    st.write(f"**Q{current_q + 1}: What is the English translation of '{german}'?**")
    selected = st.radio("Choose one:", options, key=f"radio_{current_q}")

    if not st.session_state.submitted:
        if st.button("Submit Answer"):
            st.session_state.submitted = True
            if selected == correct:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct answer: {correct}")
    else:
        if st.button("Next"):
            st.session_state.q_index += 1
            st.session_state.submitted = False
            st.rerun()

# MAIN UI
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
        
