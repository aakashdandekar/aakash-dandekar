"""Initial seed data — runs once when tables are empty."""
import json
import sqlite3


def seed_if_empty(conn: sqlite3.Connection) -> None:
    c = conn.cursor()

    if c.execute("SELECT COUNT(*) FROM projects").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO projects (title,abbr,description,tags,stack,link,color,featured,sort_order) VALUES(?,?,?,?,?,?,?,?,?)",
            [
                ("DebateX — Multi-Agent LLM Reasoning Engine", "DBX",
                 "A multi-agent system where LLMs debate, reason, and challenge each other to arrive at more robust answers.",
                 json.dumps(["Multi-Agent", "LLM"]),
                 json.dumps(["Python", "LangChain", "VueJS", "Prompt Engineering"]),
                 "https://github.com/aakashdandekar/DebateX-Multi-Agent-LLM-Reasoning-System", "cyan", 1, 0),
                ("Lexify — AI Legal Assistant", "LEX",
                 "An LLM-powered legal assistant that analyzes legal documents and answers queries using RAG.",
                 json.dumps(["AI Assistant", "RAG"]),
                 json.dumps(["Python", "FastAPI", "LangChain", "Prompt Engineering"]),
                 "https://github.com/aakashdandekar/Lexify-AI-Legal-Assistant", "purple", 0, 1),
                ("Agentix — CLI Agent powered by Ollama", "AGX",
                 "A modular CLI AI agent with tool-use capabilities — shell, file management, and web browsing.",
                 json.dumps(["Agent", "CLI"]),
                 json.dumps(["Python", "Ollama", "LangChain", "CLI"]),
                 "https://github.com/aakashdandekar/Agentix-CLI-tool-powered-by-Ollama", "blue", 0, 2),
                ("Speech-to-Text for Wayland", "STT",
                 "A lightweight STT utility built natively for Wayland on Linux.",
                 json.dumps(["Voice AI", "Linux"]),
                 json.dumps(["Python", "Whisper", "Wayland", "Linux"]),
                 "https://github.com/aakashdandekar/Speech-to-Text-for-Wayland", "green", 0, 3),
                ("Product Marketplace API", "MKT",
                 "A FastAPI backend for a product marketplace with JWT auth, image uploads, and full-text search.",
                 json.dumps(["Backend", "API"]),
                 json.dumps(["FastAPI", "MongoDB", "JWT", "ImageKit"]),
                 "https://github.com/aakashdandekar/Product-Marketplace-API", "cyan", 0, 4),
                ("Freelance Marketplace API", "FRX",
                 "A backend API for a freelance marketplace with user auth, project management, and MongoDB.",
                 json.dumps(["Backend", "API"]),
                 json.dumps(["FastAPI", "MongoDB", "Pydantic", "JWT"]),
                 "https://github.com/aakashdandekar/Freelance-Marketplace-API", "purple", 0, 5),
            ],
        )

    if c.execute("SELECT COUNT(*) FROM services").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO services (title,description,list_items,sort_order) VALUES(?,?,?,?)",
            [
                ("Agentic AI Systems",
                 "Design and deploy autonomous agents that plan, reason, use tools, and take actions — from single-agent scripts to complex multi-agent orchestration.",
                 json.dumps(["LangChain / LangGraph agents", "Tool-using LLM systems", "Multi-agent coordination", "ReAct & planning loops"]), 0),
                ("Workflow Automation",
                 "Eliminate repetitive tasks with intelligent pipelines that connect your tools, data, and processes.",
                 json.dumps(["End-to-end process automation", "Data extraction & transformation", "API integrations", "Scheduled & event-driven flows"]), 1),
                ("RAG & Knowledge Systems",
                 "Build AI that knows your business. Retrieval-Augmented Generation pipelines for your private data.",
                 json.dumps(["Vector database setup", "Document ingestion pipelines", "Semantic search systems", "Custom chatbots on your data"]), 2),
                ("AI Backend APIs",
                 "Production-ready FastAPI backends powering your AI features — scalable and ready to integrate.",
                 json.dumps(["FastAPI REST APIs", "LLM endpoint integration", "MongoDB / PostgreSQL backends", "Auth, streaming, async pipelines"]), 3),
                ("Voice AI Assistants",
                 "Conversational AI that listens, understands, and responds with sub-second latency.",
                 json.dumps(["Speech-to-text (Whisper / Groq)", "Streaming LLM responses", "Text-to-speech synthesis", "Wake-word / always-on design"]), 4),
                ("AI Strategy & Consulting",
                 "Identify AI opportunities, evaluate tools, and build a roadmap tailored to your goals.",
                 json.dumps(["AI readiness assessments", "Tool selection & architecture", "Prototype to production roadmaps", "Team workshops & demos"]), 5),
            ],
        )

    if c.execute("SELECT COUNT(*) FROM skill_groups").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO skill_groups (title,color,skills,sort_order) VALUES(?,?,?,?)",
            [
                ("AI & LLM",        "cyan",   json.dumps(["LangChain", "LangGraph", "LlamaIndex", "Prompt Engineering", "RAG Pipelines"]), 0),
                ("Backend & APIs",  "purple", json.dumps(["Python", "FastAPI", "REST API Design", "Async / Streaming", "JWT Auth", "WebSockets", "Pytest", "Docker"]), 1),
                ("Data & Storage",  "blue",   json.dumps(["MongoDB / GridFS", "PostgreSQL", "Vector DBs (Chroma/Pinecone)", "Redis", "Data Pipelines", "ETL Workflows"]), 2),
                ("Tools & Platforms","green", json.dumps(["Linux / Bash", "Git / GitHub", "n8n / Make", "Zapier", "AWS"]), 3),
            ],
        )

    if c.execute("SELECT COUNT(*) FROM about_chips").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO about_chips (name,sort_order) VALUES(?,?)",
            [("Agentic AI", 0), ("Automation", 1), ("LangChain", 2),
             ("LlamaIndex", 3), ("n8n", 4), ("Zapier", 5), ("Python", 6)],
        )

    if c.execute("SELECT COUNT(*) FROM about_values").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO about_values (num,title,description,sort_order) VALUES(?,?,?,?)",
            [
                ("01", "Results-First",   "Every agent is built to solve a real problem", 0),
                ("02", "Research-Driven", "Always using the best tools for the job", 1),
                ("03", "Transparent",     "Clear communication throughout every engagement", 2),
            ],
        )

    if c.execute("SELECT COUNT(*) FROM contact_items").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO contact_items (abbr,label,href,display,is_external,sort_order) VALUES(?,?,?,?,?,?)",
            [
                ("@",  "Email",    "mailto:aakashdandekar2006@gmail.com", "aakashdandekar2006@gmail.com", 0, 0),
                ("in", "LinkedIn", "https://www.linkedin.com/in/aakash-dandekar-6055a5317/", "linkedin.com/in/aakash-dandekar", 1, 1),
                ("gh", "GitHub",   "https://github.com/aakashdandekar", "github.com/aakashdandekar", 1, 2),
            ],
        )
