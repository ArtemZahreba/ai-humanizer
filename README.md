# AI Humanizer

**AI Humanizer** is a web application that uses AI models to rewrite and humanize text. It allows users to select an AI model, choose a writing style, and generate an alternative version of their text.

The application also supports custom prompts and keeps a history of previous humanization requests.

## Features

- **Text Humanization** — rewrite text using AI models.
- **Multiple AI Models** — choose between available models.
- **Writing Styles** — use predefined prompts for different writing styles.
- **Custom Prompts** — create, edit, and manage your own prompts.
- **History** — view previous humanization requests and results.
- **Copy Results** — quickly copy generated text.
- **Dark and Light Themes** — switch between interface themes.
- **Responsive Interface** — use the application on different screen sizes.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy, SQLAlchemy |
| AI Integration | Hugging Face Inference Router |
| AI Client | OpenAI Python SDK |
| Frontend | HTML, CSS, JavaScript |
| Templates | Jinja2 |

## Available AI Models

The application is configured with the following models:

- DeepSeek R1
- Llama 3.1 8B Instruct
- GPT-OSS 120B

Model availability depends on the configured provider and Hugging Face service.

## Project Structure

```text
ai-humanizer/
├── app.py
├── config.py
├── database/
├── routes/
├── services/
├── templates/
├── static/
├── tests/
├── docs/
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ArtemZahreba/ai-humanizer.git
cd ai-humanizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:

```env
HF_TOKEN=your_huggingface_token
FLASK_DEBUG=True
```

Replace `your_huggingface_token` with your Hugging Face access token.

### 5. Run the application

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

The SQLite database and default application data are initialized automatically when the application starts.

## Testing

Run the test modules from the project root:

```bash
python -m tests.test_humanization_api
python -m tests.test_humanization_history_integration
python -m tests.test_delete_history_api
python -m tests.test_prompts_api
python -m tests.test_models_api
```

## Documentation

Detailed technical documentation is available in the [`docs/`](docs/README.md) directory.

It includes:

- Project overview and requirements
- Software architecture
- Database structure
- API documentation
- AI integration details
- Frontend structure
- Testing information
- Architecture, ER, and Use Case diagrams

## Notes

- A valid Hugging Face token is required for AI-powered functionality.
- The maximum input text length is 5,000 characters.
- The application does not currently implement user registration or authentication.
- A browser-generated client ID is used to associate prompts and history with a browser.

## License

No license has been specified for this project yet.