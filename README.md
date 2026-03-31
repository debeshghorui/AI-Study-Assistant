# 📚 AI Study Assistant

An AI-powered study tool built with **Streamlit** and **Google Gemini**. Paste your notes and let AI help you summarize, simplify, or answer questions about them.

## Features

- **📝 Summarize** – Get concise bullet-point summaries of your notes.
- **💡 Explain Simply** – Receive beginner-friendly explanations with analogies.
- **❓ Ask a Question** – Ask anything about your notes and get contextual answers.

## Tech Stack

| Layer       | Technology              |
| ----------- | ----------------------- |
| UI          | Streamlit               |
| AI          | Google Gemini (2.0 Flash) |
| Language    | Python 3.10+            |
| Packaging   | uv                      |
| Deployment  | Docker / Cloud Run      |

---

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) installed
- A [Gemini API key](https://aistudio.google.com/apikey)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-study-assistant.git
cd ai-study-assistant
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and paste your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Run locally

```bash
uv run streamlit run app/main.py
```

The app will open at [http://localhost:8501](http://localhost:8501).

---

## Docker

### Build the image

```bash
docker build -t ai-study-assistant .
```

### Run the container

```bash
docker run -p 8080:8080 --env-file .env ai-study-assistant
```

The app will be available at [http://localhost:8080](http://localhost:8080).

---

## Deploy to Google Cloud Run

### 1. Build & push the image

```bash
# Set your GCP project
export PROJECT_ID=your-gcp-project-id

# Build with Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/ai-study-assistant

# Or use Artifact Registry
gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/cloud-run/ai-study-assistant
```

### 2. Deploy

```bash
gcloud run deploy ai-study-assistant \
  --image gcr.io/$PROJECT_ID/ai-study-assistant \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_actual_api_key \
  --port 8080
```

> **Tip:** For production, store your API key in [Secret Manager](https://cloud.google.com/secret-manager) instead of passing it as a plain environment variable.

---

## Project Structure

```
ai-study-assistant/
├── app/
│   ├── __init__.py          # Package marker
│   ├── gemini_client.py     # Gemini API integration
│   └── main.py              # Streamlit UI
├── pyproject.toml            # Dependencies & metadata
├── Dockerfile                # Container config
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## Environment Variables

| Variable         | Required | Description                     |
| ---------------- | -------- | ------------------------------- |
| `GEMINI_API_KEY` | ✅       | Your Google Gemini API key      |

---

## License

MIT