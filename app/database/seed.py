from pymongo.database import Database

def seed_if_empty(db: Database) -> None:
    if db.projects.count_documents({}) == 0:
        db.projects.insert_many([
            {
                "title": "DebateX — Multi-Agent LLM Reasoning Engine", "abbr": "DBX",
                "description": "A multi-agent system where LLMs debate, reason, and challenge each other to arrive at more robust answers.",
                "tags": ["Multi-Agent", "LLM"], "stack": ["Python", "LangChain", "VueJS", "Prompt Engineering"],
                "link": "https://github.com/aakashdandekar/DebateX-Multi-Agent-LLM-Reasoning-System", "color": "cyan", "featured": True, "sort_order": 0
            },
            {
                "title": "Lexify — AI Legal Assistant", "abbr": "LEX",
                "description": "An LLM-powered legal assistant that analyzes legal documents and answers queries using RAG.",
                "tags": ["AI Assistant", "RAG"], "stack": ["Python", "FastAPI", "LangChain", "Prompt Engineering"],
                "link": "https://github.com/aakashdandekar/Lexify-AI-Legal-Assistant", "color": "purple", "featured": False, "sort_order": 1
            },
            {
                "title": "Agentix — CLI Agent powered by Ollama", "abbr": "AGX",
                "description": "A modular CLI AI agent with tool-use capabilities — shell, file management, and web browsing.",
                "tags": ["Agent", "CLI"], "stack": ["Python", "Ollama", "LangChain", "CLI"],
                "link": "https://github.com/aakashdandekar/Agentix-CLI-tool-powered-by-Ollama", "color": "blue", "featured": False, "sort_order": 2
            },
            {
                "title": "Speech-to-Text for Wayland", "abbr": "STT",
                "description": "A lightweight STT utility built natively for Wayland on Linux.",
                "tags": ["Voice AI", "Linux"], "stack": ["Python", "Whisper", "Wayland", "Linux"],
                "link": "https://github.com/aakashdandekar/Speech-to-Text-for-Wayland", "color": "green", "featured": False, "sort_order": 3
            },
            {
                "title": "Product Marketplace API", "abbr": "MKT",
                "description": "A FastAPI backend for a product marketplace with JWT auth, image uploads, and full-text search.",
                "tags": ["Backend", "API"], "stack": ["FastAPI", "MongoDB", "JWT", "ImageKit"],
                "link": "https://github.com/aakashdandekar/Product-Marketplace-API", "color": "cyan", "featured": False, "sort_order": 4
            },
            {
                "title": "Freelance Marketplace API", "abbr": "FRX",
                "description": "A backend API for a freelance marketplace with user auth, project management, and MongoDB.",
                "tags": ["Backend", "API"], "stack": ["FastAPI", "MongoDB", "Pydantic", "JWT"],
                "link": "https://github.com/aakashdandekar/Freelance-Marketplace-API", "color": "purple", "featured": False, "sort_order": 5
            }
        ])

    if db.services.count_documents({}) == 0:
        db.services.insert_many([
            {
                "title": "Agentic AI Systems",
                "description": "Design and deploy autonomous agents that plan, reason, use tools, and take actions — from single-agent scripts to complex multi-agent orchestration.",
                "list_items": ["LangChain / LangGraph agents", "Tool-using LLM systems", "Multi-agent coordination", "ReAct & planning loops"], "sort_order": 0
            },
            {
                "title": "Workflow Automation",
                "description": "Eliminate repetitive tasks with intelligent pipelines that connect your tools, data, and processes.",
                "list_items": ["End-to-end process automation", "Data extraction & transformation", "API integrations", "Scheduled & event-driven flows"], "sort_order": 1
            },
            {
                "title": "RAG & Knowledge Systems",
                "description": "Build AI that knows your business. Retrieval-Augmented Generation pipelines for your private data.",
                "list_items": ["Vector database setup", "Document ingestion pipelines", "Semantic search systems", "Custom chatbots on your data"], "sort_order": 2
            },
            {
                "title": "AI Backend APIs",
                "description": "Production-ready FastAPI backends powering your AI features — scalable and ready to integrate.",
                "list_items": ["FastAPI REST APIs", "LLM endpoint integration", "MongoDB / PostgreSQL backends", "Auth, streaming, async pipelines"], "sort_order": 3
            },
            {
                "title": "Voice AI Assistants",
                "description": "Conversational AI that listens, understands, and responds with sub-second latency.",
                "list_items": ["Speech-to-text (Whisper / Groq)", "Streaming LLM responses", "Text-to-speech synthesis", "Wake-word / always-on design"], "sort_order": 4
            },
            {
                "title": "AI Strategy & Consulting",
                "description": "Identify AI opportunities, evaluate tools, and build a roadmap tailored to your goals.",
                "list_items": ["AI readiness assessments", "Tool selection & architecture", "Prototype to production roadmaps", "Team workshops & demos"], "sort_order": 5
            }
        ])

    if db.skill_groups.count_documents({}) == 0:
        db.skill_groups.insert_many([
            {"title": "AI & LLM", "color": "cyan", "skills": ["LangChain", "LangGraph", "LlamaIndex", "Prompt Engineering", "RAG Pipelines"], "sort_order": 0},
            {"title": "Backend & APIs", "color": "purple", "skills": ["Python", "FastAPI", "REST API Design", "Async / Streaming", "JWT Auth", "WebSockets", "Pytest", "Docker"], "sort_order": 1},
            {"title": "Data & Storage", "color": "blue", "skills": ["MongoDB / GridFS", "PostgreSQL", "Vector DBs (Chroma/Pinecone)", "Redis", "Data Pipelines", "ETL Workflows"], "sort_order": 2},
            {"title": "Tools & Platforms", "color": "green", "skills": ["Linux / Bash", "Git / GitHub", "n8n / Make", "Zapier", "AWS"], "sort_order": 3}
        ])

    if db.about_chips.count_documents({}) == 0:
        db.about_chips.insert_many([
            {"name": "Agentic AI", "sort_order": 0}, {"name": "Automation", "sort_order": 1}, {"name": "LangChain", "sort_order": 2},
            {"name": "LlamaIndex", "sort_order": 3}, {"name": "n8n", "sort_order": 4}, {"name": "Zapier", "sort_order": 5}, {"name": "Python", "sort_order": 6}
        ])

    if db.about_values.count_documents({}) == 0:
        db.about_values.insert_many([
            {"num": "01", "title": "Results-First", "description": "Every agent is built to solve a real problem", "sort_order": 0},
            {"num": "02", "title": "Research-Driven", "description": "Always using the best tools for the job", "sort_order": 1},
            {"num": "03", "title": "Transparent", "description": "Clear communication throughout every engagement", "sort_order": 2}
        ])

    if db.contact_items.count_documents({}) == 0:
        db.contact_items.insert_many([
            {"abbr": "@",  "label": "Email", "href": "mailto:aakashdandekar2006@gmail.com", "display": "aakashdandekar2006@gmail.com", "is_external": False, "sort_order": 0},
            {"abbr": "in", "label": "LinkedIn", "href": "https://www.linkedin.com/in/aakash-dandekar-6055a5317/", "display": "linkedin.com/in/aakash-dandekar", "is_external": True, "sort_order": 1},
            {"abbr": "gh", "label": "GitHub", "href": "https://github.com/aakashdandekar", "display": "github.com/aakashdandekar", "is_external": True, "sort_order": 2}
        ])
