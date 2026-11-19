# 🎓 CampusMate – AI Student Assistant

CampusMate is an AI-powered student assistant chatbot designed to help students with academic queries, programming concepts, study guidance, and general educational support.

It uses **Cloudflare Workers AI** to generate intelligent responses through a simple, interactive, and user-friendly chat interface.

## 🚀 Project Overview

CampusMate aims to make learning easier and more accessible by providing students with an AI assistant that can answer questions, explain technical concepts, and offer academic guidance.

## ✨ Features

- 🤖 AI-powered chatbot for student assistance
- 💬 Real-time conversational interface
- 📚 Academic query assistance
- 💻 Programming and technical concept explanations
- 🎨 Simple and user-friendly interface
- 📱 Responsive web design
- ☁️ Cloudflare Workers AI integration

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| HTML | Webpage structure |
| CSS | Styling and design |
| JavaScript | Frontend interaction |
| Cloudflare Workers AI | AI-powered responses |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
Student-chatbot/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── app.js
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pm279675-ui/Student-chatbot.git
```

### 2. Navigate to the Project Directory

```bash
cd Student-chatbot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root directory and add:

```env
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_MODEL=@cf/meta/llama-3.1-8b-instruct
FLASK_DEBUG=false
```

Replace the placeholder values with your actual Cloudflare credentials.

### 7. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 🔐 Security

- API credentials are stored in environment variables.
- The `.env` file should never be uploaded to GitHub.
- The `.gitignore` file helps prevent sensitive files from being committed.
- Never share your API tokens publicly.

## ☁️ Deployment

The application can be deployed using cloud hosting platforms such as:

- Render
- Vercel

Cloudflare Workers AI is used as the AI inference provider.

Deployment requires configuring the appropriate environment variables on the hosting platform.

## 🎯 Project Objective

The main objective of CampusMate is to develop an AI-powered educational assistant that helps students access academic information, understand programming concepts, and improve their learning experience through conversational AI.

## 🔮 Future Enhancements

- Student login and authentication
- Personalized learning recommendations
- Chat history management
- PDF and document-based question answering
- Multilingual student support
- Integration with academic resources

## 👨‍💻 Developer

**Praveen Mishra**

B.Tech – Computer Science and Engineering

## 📄 License

This project is developed for educational and learning purposes.

---

⭐ If you find this project useful, consider giving the repository a star!
