# 🔥 TEST UPDATE — This change is for Git commit test

# 🎬 Netflix Smart Chatbot

A smart chatbot that answers natural-language questions about Netflix titles using **spaCy**, **Sentence Transformers**, and **Gradio**. It supports filters like genre, year, country, director, and actors — and provides rich markdown responses.

![Gradio UI](https://github.com/Harshmohod/chatbot/assets/preview-image.png) <!-- (Optional image link if you want to add a UI preview) -->

---

## 🚀 Features

- 🧠 **Natural language understanding** using spaCy NER and regex
- 📚 **Semantic search** powered by Sentence Transformers (`all-MiniLM-L6-v2`)
- 🔎 Filter by:
  - Genre (e.g., comedy, drama)
  - Release year (after, before, between, exact)
  - Country
  - Director or Actor names
- ⚡ Fast local similarity search (top 1000 titles)
- 🌐 Beautiful UI with Gradio

---

## 📁 Dataset

Uses the [Netflix Movies and TV Shows dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) from Kaggle, saved as `netflix_titles.csv`.

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Harshmohod/chatbot.git
cd chatbot

2. (Optional) Create a virtual environment
bash
Copy
Edit
python -m venv netflix_env
netflix_env\Scripts\activate   # For Windows
# source netflix_env/bin/activate  # For Linux/macOS
3. Install required packages
bash
Copy
Edit
pip install -r requirment.txt
If the en_core_web_sm model is not installed, it will be downloaded automatically on first run.

▶️ Run the App
bash
Copy
Edit
python app.py
The app will:

Generate sentence embeddings from the CSV file

Extract filters from user queries

Launch a Gradio interface at http://localhost:7860/ (or public link if share=True)

🧠 Example Queries You Can Ask
text
Copy
Edit
🎬 Show me comedy movies from India after 2015
🎬 List crime thrillers between 2000 and 2010
🎬 Movies directed by Christopher Nolan
🎬 Action films in the US before 2012
🎬 Horror movies from Japan
📂 Project Structure
plaintext
Copy
Edit
chatbot/
│
├── app.py                  # Main chatbot script
├── netflix_titles.csv      # Netflix dataset
├── requirment.txt          # Python dependencies
├── embeddings.npy          # Saved sentence embeddings (auto-generated)
├── embedding_texts.txt     # Matching text used in embeddings (auto-generated)
└── .gradio/                # Gradio runtime files (auto-created)
🧰 Tech Stack
Tool	Purpose
Python	Core language
spaCy	NLP and entity recognition
sentence-transformers	Semantic embedding (MiniLM)
NumPy	Array operations
Pandas	Data manipulation
Gradio	Web UI for chatbot

📌 Notes
You can run this app locally or deploy it on Hugging Face Spaces or other cloud platforms.

Embeddings are re-generated each time you run the script. For production, you may want to persist them.

🧑‍💻 Author
Harsh Mohod
GitHub: @Harshmohod

📜 License
MIT License – use it freely with attribution.
```
