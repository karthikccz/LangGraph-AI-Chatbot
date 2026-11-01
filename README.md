# 🤖 LangGraph AI Chatbot

A conversational AI chatbot built using **LangGraph, LangChain, Groq, Streamlit, and SQLite**.

The application supports **multi-turn conversations**, **persistent chat history**, **multiple chat threads**, **chat renaming**, **chat deletion**, and **streaming AI responses**.

---

## 🚀 Features

- 💬 Interactive AI chatbot
- ⚡ Streaming responses
- 🧠 Multi-turn conversation memory
- 🗂️ Multiple conversation threads
- ➕ Create a new chat
- ✏️ Rename conversations
- 🗑️ Delete conversations
- 💾 Persistent chat history using SQLite
- 🔄 Load previous conversations
- 🆔 Unique thread ID for every conversation
- 🌐 User-friendly Streamlit interface
- 🤖 Groq LLM integration using LangChain

---

## 🛠️ Tech Stack

- **Python**
- **LangGraph**
- **LangChain**
- **Groq**
- **Streamlit**
- **SQLite**
- **python-dotenv**

---

## 📂 Project Structure

```text
CHATBOT/
│
├── backend.py              # LangGraph backend and SQLite memory
├── frontend.py             # Streamlit user interface
├── requirements.txt        # Project dependencies
├── .gitignore              # Files ignored by Git
├── README.md               # Project documentation
│
├── .env                    # API key (not pushed to GitHub)
└── chatbot.db              # SQLite database (generated automatically)
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project folder:

```bash
cd CHATBOT
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Add Your Groq API Key

Before running the application, create a file named:

```text
.env
```

inside the project folder.

Add your Groq API key to the `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Example

```text
CHATBOT/
│
├── backend.py
├── frontend.py
├── requirements.txt
├── .env              ← Add your API key here
└── .gitignore
```

> ⚠️ **Important:** Never upload your `.env` file or API key to GitHub.

Make sure your `.gitignore` contains:

```gitignore
.env
venv/
__pycache__/
*.db
```

---

## ▶️ Run the Application

After activating your virtual environment, run:

```bash
streamlit run frontend.py
```

The application will open in your browser.

---

## 🧠 How It Works

```text
User
  │
  ▼
Streamlit Frontend
  │
  ▼
LangGraph
  │
  ▼
Groq LLM
  │
  ▼
AI Response
  │
  ▼
SQLite Checkpointer
```

Each conversation receives a unique **Thread ID**.

```text
Thread ID
   │
   ├── Conversation 1
   │
   ├── Conversation 2
   │
   └── Conversation 3
```

The SQLite checkpointer stores the conversation state, allowing previous conversations to be loaded later.

---

## 💬 Chat Management

The application allows users to:

### ➕ Create New Chats

Every new chat receives a unique Thread ID.

### ✏️ Rename Chats

Users can rename conversations directly from the sidebar.

### 🗑️ Delete Chats

Users can delete conversations from the sidebar.

### 🔄 Load Previous Chats

Previously saved conversations can be loaded using the conversation list.

---

## 🗃️ Database

The project uses SQLite for persistent conversation memory.

```text
chatbot.db
```

LangGraph uses `SqliteSaver` to store conversation checkpoints.

Chat titles are also stored in the SQLite database.

---

## 📦 Requirements

Example dependencies:

```text
streamlit
langgraph
langchain
langchain-groq
langgraph-checkpoint-sqlite
python-dotenv
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🔮 Future Improvements

- Automatic chat title generation using AI
- User authentication
- Cloud database integration
- Conversation search
- File upload and document chat
- RAG integration
- Multiple LLM model selection
- Deployment to Streamlit Cloud

---

## 👨‍💻 Author

**Karthik Kumar**

B.Tech – Artificial Intelligence & Machine Learning

---

## ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub!
