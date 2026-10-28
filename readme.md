# 🎬 ContextCue

### Context-Aware Movie Dialogue System

ContextCue is a conversational movie assistant built with **Python, Streamlit, and the Gemini API**. It maintains conversation history and tracks movie-related entities to make follow-up questions more coherent.

For example, after asking **“Tell me about Interstellar”**, a user can ask **“Who directed it?”** without repeating the film title. ContextCue uses conversation history and stored context to help Gemini interpret the reference.

> **Project status:** Functional MVP. Core conversational features and baseline tests are implemented; deployment and additional reliability improvements are planned.

## Features

- **Movie Q&A:** Discuss films, actors, directors, and related topics using Gemini.
- **Multi-turn conversations:** Preserve user and assistant messages within a Streamlit session.
- **Entity extraction:** Identify movie, director, and actor names explicitly mentioned in the latest user message.
- **Structured context tracking:** Maintain `current_movie`, `current_director`, and `current_actor`.
- **Basic topic switching:** When a different movie is explicitly mentioned, clear the previously stored director and actor.
- **New Conversation:** Reset both conversation history and tracked context.
- **Context inspection:** View the current structured context in an expandable panel.
- **Basic error handling:** Display user-friendly messages for API failures without saving failed responses as assistant turns.

## Tech Stack

| Component | Technology |
| --- | --- |
| Language | Python |
| Interface | Streamlit |
| Language model | Google Gemini API (`google-genai` SDK) |
| Configuration | `python-dotenv` |
| Testing | `pytest` and custom evaluation scripts |

The Gemini model is configured through the `GEMINI_MODEL` environment variable; model availability depends on your API access.

## System Architecture

```text
                       User message
                            |
                            v
                     Streamlit UI
                            |
             +--------------+---------------+
             |                              |
             v                              v
     Conversation history          Entity extraction
      (session_state)                 (Gemini API)
             |                              |
             |                              v
             |                        Context update
             |                      (movie/director/actor)
             |                              |
             +---------------+--------------+
                             |
                             v
                 Prompt + history + context
                             |
                             v
                         Gemini API
                             |
                             v
                     Assistant response
                             |
                             v
              Save successful turn and context
```

### Request Flow

1. A user submits a movie-related question in the Streamlit chat.
2. `context_extractor.py` asks Gemini to extract only entities explicitly named in that message.
3. `context_tracker.py` merges extracted entities with the stored context, resetting director and actor fields when a new movie is detected.
4. `llm_client.py` sends the conversation history and formatted context to Gemini to generate a response.
5. On success, `app.py` displays the answer and saves the completed turn and updated context.
6. If extraction fails, the app can still attempt a response using conversation history. If response generation fails, the failed turn is not saved as a successful conversation.

## Project Structure

```text
ContextCue/
├── app.py                    # Streamlit interface and session state
├── llm_client.py             # Gemini response generation
├── context_extractor.py      # Gemini-based entity extraction
├── context_tracker.py        # Context creation, formatting, and updates
├── test_context_tracker.py   # Context tracking unit tests
├── test_context_extractor.py # Live entity extraction tests
├── evaluate_extractor.py     # Entity extraction evaluation
├── evaluate_context.py       # Context consistency evaluation
├── requirements.txt          # Python dependencies
├── .env                      # Local API credentials (do not commit)
├── .gitignore                # Files excluded from Git
└── README.md
```

Other local development utilities or manual test scripts may also be present.

## Getting Started

### 1. Prerequisites

- Python 3.12 (the project was developed with Python 3.12.4)
- A Gemini API key
- Git (optional, for cloning and publishing)

### 2. Clone or open the project

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

If the project is not on GitHub yet, simply open its folder in VS Code.

### 3. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Ensure `requirements.txt` includes at least `streamlit`, `google-genai`, `python-dotenv`, and `pytest`.

### 5. Configure environment variables

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Use a Gemini model available to your account. **Never commit `.env` or expose API keys in screenshots or logs.**

### 6. Run the app

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal (typically `http://localhost:8501`).

## Example Conversation

**User:** Tell me about Interstellar.

**ContextCue:** Interstellar is a science-fiction film directed by Christopher Nolan...

**User:** Who directed it?

**ContextCue:** Interstellar was directed by Christopher Nolan.

**User:** I like Christopher Nolan.

**ContextCue:** Christopher Nolan is known for films such as Inception and The Dark Knight...

**Tracked context after these messages:**

```json
{
  "current_movie": "Interstellar",
  "current_director": "Christopher Nolan",
  "current_actor": null
}
```

The extractor intentionally does **not** populate the director field from the assistant's answer alone: it extracts names explicitly present in the latest **user** message.

## Testing and Evaluation

The following results were observed during development:

| Test suite | Passed | Scope |
| --- | ---: | --- |
| Context tracker unit tests | 5 / 5 | Initialization, updates, retention, topic switching, capitalization |
| Context extractor tests | 4 / 4 | Explicit film/director/actor extraction and no-entity case |
| Entity extraction evaluation | 20 / 20 | Expected target-field matches on a small curated set |
| Context consistency evaluation | 8 / 8 | Sequential context updates using predefined extracted entities |
| **Total** | **37 / 37** | **Across the listed test scenarios** |

The 20-case extraction evaluation achieved **100% target-field accuracy** on that specific dataset, with **0 API errors** in the successful run. This is **not** a claim of 100% general accuracy. The context consistency evaluation tests deterministic state-update logic, not full end-to-end chatbot correctness.

### Run tests

```bash
python -m pytest test_context_tracker.py -v
python -m pytest test_context_extractor.py -v
python evaluate_extractor.py
python evaluate_context.py
```

**Note:** The extractor tests and `evaluate_extractor.py` call the live Gemini API and consume quota. The evaluation script spaces out requests and retries some temporary errors; API limits may still apply.

## Limitations

- **Explicit-mention extraction:** The extractor reads only the latest user message, so pronouns like “it” do not themselves create new entity values. Follow-up interpretation relies on conversation history and stored context.
- **Simple topic switching:** The context tracker assumes a newly mentioned movie becomes the active movie; comparisons involving multiple films or more complex topic changes are not fully handled.
- **Possible stale entities:** Director/actor changes without a movie change may require more advanced relation-aware context management.
- **API dependence:** Responses and extraction require Gemini availability, network access, and sufficient quota.
- **Evaluation scope:** Current tests cover curated examples and do not establish broad real-world performance or factual accuracy of every generated answer.
- **No external retrieval:** This MVP does not use RAG or a dedicated movie knowledge base.

## Future Improvements

- More robust handling of API rate limits and retry timing.
- Larger, more diverse evaluation datasets and end-to-end conversation tests.
- Relation-aware context tracking and better handling of multi-movie conversations.
- Deployment with secure secret management.
- Optional retrieval-augmented generation (RAG) using a movie knowledge base.

## Security

Keep API credentials out of version control. A minimal `.gitignore` should include:

```gitignore
.env
.venv/
__pycache__/
.pytest_cache/
*.pyc
```

## Project Purpose

ContextCue was developed as a hands-on AI engineering portfolio project to explore **LLM API integration, prompt engineering, structured entity extraction, conversation state management, and evaluation**. It focuses on practical application architecture rather than training a language model from scratch.

---

**ContextCue — Making movie conversations more context-aware.**
