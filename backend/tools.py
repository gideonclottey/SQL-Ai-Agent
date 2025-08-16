import json
import sqlite3
import wikipedia
from typing import Dict, Any
import os

DB_PATH = os.getenv("DB_PATH", "./app.db")

# --------- Tool Implementations ---------

def query_sqlite(query: str) -> Dict[str, Any]:
    if not query.strip().lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed for security reasons."}
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        data = [dict(row) for row in rows]
        return {
            "success": True,
            "data": data,
            "row_count": len(data)
        }
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}
    finally:
        try:
            conn.close()
        except Exception:
            pass


def search_wikipedia(query: str) -> Dict[str, Any]:
    try:
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
        url = wikipedia.page(query).url
        return {"success": True, "summary": summary, "url": url}
    except wikipedia.DisambiguationError as e:
        return {
            "error": "Disambiguation error",
            "options": e.options[:5],
            "message": "Topic is ambiguous. Please be more specific."
        }
    except wikipedia.PageError:
        return {"error": "Page not found", "message": f"No article found for: {query}"}
    except Exception as e:
        return {"error": "Unexpected error", "message": str(e)}

# --------- Gemini Function Declarations (Tool Schemas) ---------
# Compatible with google-generativeai function calling
GEMINI_TOOLS = [
    {
        "function_declarations": [
            {
                "name": "query_sqlite",
                "description": (
                    "Execute a SQLite SELECT query and return results as JSON. "
                    "Only SELECT queries are allowed. Tables include: users(id, email, age, location, signup_date, last_login, job_industry), "
                    "user_activity(id, user_id, activity_date, activity_type)."
                ),
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {"type": "STRING", "description": "SQL SELECT query to execute."}
                    },
                    "required": ["query"]
                },
            },
            {
                "name": "search_wikipedia",
                "description": "Search Wikipedia and return a concise 3-sentence summary of the most relevant article.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {"type": "STRING", "description": "Topic to search for."}
                    },
                    "required": ["query"]
                },
            }
        ]
    }
]