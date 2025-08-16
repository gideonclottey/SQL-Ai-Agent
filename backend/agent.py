import os
import json
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from .tools import GEMINI_TOOLS, query_sqlite, search_wikipedia

SYSTEM_PROMPT = (
    "You are a helpful AI assistant with access to two tools: a SQLite database and Wikipedia.\n"
    "Rules:\n"
    "1) For data questions about our app, prefer the SQLite tool (SELECT-only).\n"
    "2) For general knowledge, use Wikipedia.\n"
    "3) Always cite your source briefly (e.g., 'DB' or 'Wikipedia').\n"
    "4) If a tool returns an error, explain it clearly.\n"
)

class GeminiAgent:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name, tools=GEMINI_TOOLS)

    def _execute_function_call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "query_sqlite":
                return query_sqlite(arguments.get("query", ""))
            elif name == "search_wikipedia":
                return search_wikipedia(arguments.get("query", ""))
            else:
                return {"error": f"Unknown tool: {name}"}
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    def chat(self, user_message: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        # Convert simple history to Gemini 'contents'
        contents = [{"role": "user", "parts": [SYSTEM_PROMPT]}]
        if history:
            for m in history:
                contents.append({"role": m["role"], "parts": [m["content"]]})
        contents.append({"role": "user", "parts": [user_message]})

        # Tool loop
        max_iters = 5
        tool_calls_trace = []

        for _ in range(max_iters):
            resp = self.model.generate_content(contents)
            parts = resp.candidates[0].content.parts if resp.candidates else []

            # Check for function calls
            function_calls = [p.function_call for p in parts if hasattr(p, 'function_call') and p.function_call]

            if not function_calls:
                # Final answer
                text_parts = [getattr(p, 'text', None) for p in parts if hasattr(p, 'text')]
                answer = "\n".join([t for t in text_parts if t]) or "(no content)"
                return {"answer": answer, "tool_calls": tool_calls_trace}

            # Execute each functionCall and append functionResponse
            for fc in function_calls:
                name = fc.name
                args = json.loads(fc.args) if isinstance(fc.args, str) else dict(fc.args)
                result = self._execute_function_call(name, args)
                tool_calls_trace.append({"name": name, "args": args, "result_preview": str(result)[:300]})

                contents.append({
                    "role": "tool",
                    "parts": [{
                        "function_response": {
                            "name": name,
                            "response": result
                        }
                    }]
                })

        return {"answer": "Reached max tool iterations without final answer.", "tool_calls": tool_calls_trace}