# app.py
import streamlit as st
import subprocess
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="AI Flashcard Generator", page_icon="🧠")
st.title("🧠 AI Flashcard Generator with PDF/Text Upload")

# --- File upload ---
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

text_sections = []
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text_sections = [page.extract_text() for page in reader.pages if page.extract_text()]
    elif uploaded_file.type == "text/plain":
        text_sections = [uploaded_file.read().decode("utf-8")]
    
    st.subheader("Extracted Text Sections:")
    for i, sec in enumerate(text_sections):
        st.text_area(f"Section {i+1}", sec, height=150)

# --- Select section ---
selected_section = None
if text_sections:
    options = [f"Section {i+1}" for i in range(len(text_sections))]
    selected_idx = st.selectbox("Select section to generate flashcards from:", options)
    selected_section = text_sections[options.index(selected_idx)]

# --- Number of flashcards ---
num_cards = st.slider("Number of flashcards:", 1, 10, 5)

# --- Function to generate flashcards ---
def generate_flashcards(text, num_cards):
    prompt = (
        f"Generate {num_cards} simple question-answer flashcards from the following text. "
        f"Make sure each question ends with a '?' and is followed immediately by its answer. "
        f"Do not write 'Card 1', just Q&A.\n{text}"
    )
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        lines = [line.strip() for line in output.split("\n") if line.strip() and line.strip().lower() != "q&a"]
        
        flashcards = []
        i = 0
        while i < len(lines):
            if lines[i].endswith("?"):
                q = lines[i]
                # Find next line as answer
                a = lines[i+1] if i+1 < len(lines) else "Answer not provided"
                flashcards.append((q, a))
                i += 2
            else:
                i += 1
        return flashcards
    except subprocess.CalledProcessError as e:
        return []
# --- Generate flashcards ---
if st.button("Generate Flashcards"):
    if uploaded_file is None and selected_section is None:
        st.warning("Please upload a file or select text first!")
    else:
        source_text = selected_section if selected_section else st.text_input("Enter a topic/text")
        with st.spinner("Generating flashcards..."):
            flashcards = generate_flashcards(source_text, num_cards)
        
        st.subheader("Generated Flashcards:")
        if not flashcards:
            st.write("No flashcards generated. Make sure your text is not empty!")
        else:
            # Display each flashcard with click-to-show answer
            for i, (q, a) in enumerate(flashcards):
                with st.expander(f"Q{i+1}: {q}"):
                    st.write(f"A: {a}")
