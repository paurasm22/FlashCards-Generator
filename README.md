# 🧠 AI Flashcard Generator

A simple **Streamlit web app** that generates question-answer flashcards from PDF or TXT files using **LLaMA 3 via Ollama**.  
It helps students quickly convert study material into interactive flashcards for easier learning.

---

## 📌 Features

- Upload a PDF or TXT file containing study material
- Extract text from PDF pages or TXT files
- Select a section (for multi-page PDFs)
- Choose the number of flashcards to generate
- Generate **interactive flashcards** with expandable answers
- Uses a **pre-trained LLaMA 3 model** via Ollama for Q&A generation

---

## 🛠 Requirements

- Python 3.10+
- Streamlit (`pip install streamlit`)
- PyPDF2 (`pip install PyPDF2`)
- Ollama ([Download and install](https://ollama.com/))  
  > Ollama provides the LLaMA 3 model. The app communicates with it via CLI.

---

## 💾 Installation & Setup

Follow these steps to set up the project locally:

### 1️⃣ Clone the repository

```bash
git clone <your-github-repo-url>
cd <repo-folder>
