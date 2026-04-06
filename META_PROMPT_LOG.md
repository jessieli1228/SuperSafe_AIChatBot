# Secure Coding Chatbot: Meta-Prompting Log

## Goal: To transform a generic LLM into a specialized Security Mentor for Python developers.

## 1. Persona Definition (Current Version)
**System Instruction:** > "You are a Python Security Mentor. Be concise and focus on Python code security."

**Purpose:** To restrict the AI's domain knowledge to Python. This prevents "hallucinations" (like the Java JDBC errors seen in early testing) and ensures the user gets direct, actionable security advice.

## 2. Context Logic (The "Full Message" Strategy)
**Mechanism:** The chatbot doesn't just see the user's question. It receives a bundled prompt:
- **If code is present:** `Context (Python): {editor_content} + Question: {prompt}`
- **If editor is empty:** `Just the {prompt}`

**Result:** The AI provides "Context-Aware" mentoring, meaning it "sees" what the user is typing in the editor before it answers.