import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

load_dotenv()

# Set PROVIDER to "openai", "mistral", "google", or "groq"
PROVIDER = "mistral"

if PROVIDER == "openai":
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set in .env")
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        api_key=OPENAI_API_KEY,
        max_tokens=1024,
        max_retries=3,          # auto-retry on rate limit
    )

elif PROVIDER == "mistral":
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY not set in .env")
    llm = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.1,
        api_key=MISTRAL_API_KEY,
        max_tokens=1024,
        max_retries=3,
    )

elif PROVIDER == "google":
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in .env")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        temperature=0.1,
        google_api_key=GOOGLE_API_KEY,
        max_tokens=1024,
        max_retries=3,
    )

elif PROVIDER == "groq":
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in .env")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        api_key=GROQ_API_KEY,
        max_tokens=1024,
        max_retries=3,
    ).bind(parallel_tool_calls=False)

else:
    raise ValueError(f"Unknown PROVIDER '{PROVIDER}'. Choose 'openai', 'mistral', 'google', or 'groq'.")
