import streamlit as st
import random

# Predefined German-English color pairs
color_pairs = [
    ("Rot", "Red"),
    ("Blau", "Blue"),
    ("Grün", "Green"),
    ("Gelb", "Yellow"),
    ("Orange", "Orange"),
    ("Lila", "Purple"),
    ("Rosa", "Pink"),
    ("Braun", "Brown"),
    ("Grau", "Gray"),
    ("Schwarz", "Black"),
    ("Weiß", "White"),
    ("Hellblau", "Light Blue"),
    ("Dunkelgrün", "Dark Green"),
    ("Hellgrün", "Light Green"),
    ("Dunkelblau", "Dark Blue"),
    ("Beige", "Beige"),
    ("Gold", "Gold"),
    ("Silber", "Silver"),
    ("Türkis", "Turquoise"),
    ("Bunt", "Multicolored")
]

st.title("German Colors Quiz")

# Shuffle and limit number of questions if needed
random.shuffle(color_pairs)

if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.q_index = 0

if st.session_state.q_index < len(color_pairs):
    german, correct_english = color_pairs[st.session_state.q_index]
    options = [correct_english]
    while len(options) < 4:
        _, fake = random.choice(color_pairs)
        if fake not in options:
            options.append(fake)
    random.shuffle(options)

    st.write(f"**Q{st.session_state.q_index + 1}: What is the English translation of '{german}'?**")
    choice = st.radio("Choose one:", options, key=f"q{st.session_state.q_index}")
    if st.button("Submit Answer"):
        if choice == correct_english:
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! Correct answer: {correct_english}")
        st.session_state.q_index += 1
        st.experimental_rerun()
else:
    st.success(f"Quiz completed! Your final score: {st.session_state.score}/{len(color_pairs)}")
    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.q_index = 0
        st.experimental_rerun()
