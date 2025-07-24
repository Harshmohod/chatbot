import pandas as pd
import gradio as gr
import spacy
from sentence_transformers import SentenceTransformer, util

# ✅ Load CSV
df = pd.read_csv("netflix_titles.csv")
df.fillna("", inplace=True)
df.columns = [col.lower().strip() for col in df.columns]

# ✅ Load spaCy and sentence-transformer
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Create sentence descriptions for all rows
def row_to_text(row):
    return (
        f"The movie '{row['title']}' is a {row['listed_in']} title from {row['country']} "
        f"released in {row['release_year']}, directed by {row['director']}, starring {row['cast']}. "
        f"Description: {row['description']}"
    )

df["embedding_text"] = df.apply(row_to_text, axis=1)
corpus_embeddings = model.encode(df["embedding_text"].tolist(), convert_to_tensor=True)

# ✅ spaCy for filter extraction (optional enrichment)
def extract_filters(query):
    doc = nlp(query.lower())
    filters = {}

    # Detect genre manually
    GENRES = ['romantic', 'romance', 'comedy', 'action', 'crime', 'horror', 'cartoon', 'anime', 'thriller', 'documentary', 'drama']
    filters["genre"] = [g for g in GENRES if g in query]

    for ent in doc.ents:
        if ent.label_ == "DATE":
            filters["year"] = ent.text
        elif ent.label_ == "GPE":
            filters["country"] = ent.text
        elif ent.label_ == "PERSON":
            filters["person"] = ent.text

    return filters

# ✅ Chatbot function
def chatbot(query):
    filters = extract_filters(query)
    print("Extracted filters:", filters)

    # 1. Embed the query
    query_embedding = model.encode(query, convert_to_tensor=True)

    # 2. Semantic similarity
    scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_indices = scores.argsort(descending=True)

    # 3. Search top 100 results, then filter down if needed
    filtered = []
    for idx in top_indices[:100]:
        row = df.iloc[int(idx)]

        # Apply soft filtering using spaCy-detected filters
        genre_match = True
        country_match = True
        year_match = True
        person_match = True

        # Genre check
        if filters.get("genre"):
            genre_match = any(g.lower() in row["listed_in"].lower() for g in filters["genre"])

        # Country check
        if filters.get("country"):
            country_match = filters["country"].lower() in row["country"].lower()

        # Year check
        if filters.get("year"):
            year_match = str(filters["year"]) in str(row["release_year"])

        # Person check (in cast or director)
        if filters.get("person"):
            person = filters["person"].lower()
            person_match = person in row["cast"].lower() or person in row["director"].lower()

        if genre_match and country_match and year_match and person_match:
            filtered.append(row)

        if len(filtered) >= 10:
            break

    # Build result
    if not filtered:
        return "❌ No results found."

    response = ""
    for row in filtered:
        response += f"🎬 **{row['title']}**\n"
        response += f"📅 Year: {row['release_year']} | 🎭 Genre: {row['listed_in']}\n"
        response += f"🌍 Country: {row['country'] or 'N/A'}\n"
        response += f"🎬 Director: {row['director'] or 'N/A'}\n"
        response += f"👥 Cast: {row['cast'] or 'N/A'}\n"
        response += f"📝 {row['description'][:200]}...\n---\n"

    return response


# ✅ Gradio UI
gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(label="Ask about Netflix titles", placeholder="e.g. romantic Indian movies from 2015 with Shah Rukh Khan"),
    outputs="markdown",
    title="🎬 Netflix Chatbot (Smart Search)",
    description="Ask flexibly: genre, year, actor, director, country. Powered by semantic search + spaCy."
).launch()


