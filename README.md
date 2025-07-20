# 📚 Knowledge Assistance LLM

A **Django-based AI-powered knowledge management assistant** that allows users to upload documents (PDFs) and ask natural language questions based on the content. Uses **Google's Gemini API** and **FAISS** for semantic search over vector embeddings.

---

## 🚀 Features

* 📄 Upload documents via Django admin
* 🧠 Ask questions based on uploaded content
* 🔍 Semantic search with FAISS vector store
* 🤖 Gemini API integration for LLM responses
* 🛡️ Environment-safe with `.env` configuration
* 🔗 RESTful API endpoints (Postman collection included)

---

## 🏗️ Project Structure

```
llm-powered-knowledge-assistant/
│
├── knowledge_assistance_llm/           # Main project directory
│   ├── faiss_index/                    # FAISS vector index storage
│   ├── knowledge_assistance_llm/       # Django project settings
│   ├── knowledge_base/                 # App: Handles document upload & storage
│   ├── llm_assistant/                  # App: Handles question-answering logic
│   ├── media/                          # Uploaded PDF files
│   ├── db.sqlite3                      # SQLite database
│   └── manage.py                       # Django management script
│
├── venv/                               # Python virtual environment
├── .env                                # Environment variables
├── .env.example                        # Example environment file
├── .gitignore                          # Git ignore rules
├── authenticatepy-eed22-3139f52e3ec8.json  # Gemini/Google credentials (not committed)
├── Knowledge_Assistance_LLM.postman_collection.json  # Postman API collection
└── requirements.txt                    # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Parth1304/LLM_Powered_Knowledge_Assistant.git
cd llm-powered-knowledge-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the root of the project:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

GEMINI_API_KEY=your-gemini-api-key
GOOGLE_APPLICATION_CREDENTIALS=authenticatepy-eed22-3139f52e3ec8.json
GOOGLE_API_VERSION=v1

DATABASE_URL=sqlite:///db.sqlite3
MEDIA_URL=/media/
STATIC_URL=/static/
```

> ⚠️ **Important:** Never commit `.env` files to Git.

### 5. Run Migrations

```bash
cd knowledge_assistance_llm
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Start the Server

```bash
python manage.py runserver
```

---

## 📫 API Endpoints

| Method | Endpoint                              | Description                       |
| ------ | ------------------------------------- | --------------------------------- |
| GET    | `/api/v1/knowledge-base/documents/`   | List all uploaded documents       |
| POST   | `/api/v1/llm-assistant/ask-question/` | Ask a question based on documents |
| GET    | `/admin/`                             | Django Admin panel (upload docs)  |

> 📄 Use the included **Postman collection** to test all endpoints easily.

---

## 🧠 Technologies Used

* Python 3.11+
* Django
* Google Gemini API
* FAISS (Facebook AI Similarity Search)
* LangChain (optional)
* SQLite or PostgreSQL
* python-dotenv

---

## 🔒 .gitignore Recommendations

```
.env
*.json
venv/
media/
db.sqlite3
```

---

## 📄 License

MIT License — use freely, modify responsibly.

---

## 🙋‍♂️ Contact

Built with ❤️ by [Parth](https://github.com/YOUR_USERNAME)

---

