import streamlit as st
import requests
import fitz  # PyMuPDF
import random

@st.cache_data
def load_pdf_text(url):
    response = requests.get(url)
    with open("colors.pdf", "wb") as f:
        f.write(response.content)
    doc = fitz.open("colors.pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
st.subheader("Debug: Raw PDF Text Preview")
lines = raw_text.split("\n")
for i, line in enumerate(lines):
    st.write(f"{i+1}: {repr(line)}")
    
def parse_colors(text):
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
        except Exception as e:
            st.warning(f"Error processing line: {line} | Error: {e}")
    return pairs

def make_quiz(questions):
    random.shuffle(questions)
    for idx, (german, correct_english) in enumerate(questions):
        options = [correct_english]
        while len(options) < 4:
            _, fake = random.choice(questions)
            if fake not in options:
                options.append(fake)
        random.shuffle(options)

        st.write(f"**Q{idx+1}: What is the English translation of '{german}'?**")
        choice = st.radio("Choose one:", options, key=f"q{idx}")
        if st.button(f"Submit Answer {idx+1}", key=f"submit{idx}"):
            if choice == correct_english:
                st.success("Correct!")
            else:
                st.error(f"Wrong! Correct answer: {correct_english}")
            st.write("---")

# Streamlit App
st.title("German Colors Quiz")

pdf_url = st.text_input("Enter GitHub raw PDF URL:")
if pdf_url:
    raw_text = load_pdf_text(pdf_url)
    color_pairs = parse_colors(raw_text)
    if color_pairs:
        make_quiz(color_pairs)
    else:
        st.warning("No valid color translations found in the PDF.")
      
