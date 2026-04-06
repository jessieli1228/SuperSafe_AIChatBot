# Secure Coding Chatbot: Meta-Prompting Log

## Goal: To transform a generic LLM into a specialized Security Mentor for Python developers.

## 1. Persona Definition (Version 1.0)
**System Instruction:** > "You are a Python Security Mentor. Be concise and focus on Python code security."

**Purpose:** To restrict the AI's domain knowledge to Python. This prevents "hallucinations" (like the Java JDBC errors seen in early testing) and ensures the user gets direct, actionable security advice.

## 2. Context Logic (The "Full Message" Strategy)
**Mechanism:** The chatbot doesn't just see the user's question. It receives a bundled prompt:
- **If code is present:** `Context (Python): {editor_content} + Question: {prompt}`
- **If editor is empty:** `Just the {prompt}`

**Result:** The AI provides "Context-Aware" mentoring, meaning it "sees" what the user is typing in the editor before it answers.

## Version 1.1: Engagement Tuning
**Requirement:** Increase user retention and learning depth.
**Update:** Added a "Guided Learning" instruction to the Meta-Prompt.
**Instruction:** "At the end of every response, provide one brief, engaging follow-up question..."
**Result:** The AI now acts as a proactive tutor rather than a reactive search engine.

## Version 1.2: Unified Global Mentor (Both for learning resources page and code workspace)
**Strategy:** Consolidated individual page bots into a single 'Security & Education Mentor' function.
**Logic Updates:**
- **Shared Memory:** Switched to a single `st.session_state.messages` list so the conversation follows the user from the Learning Center to the Workspace.
- **Context Dispatcher:** The prompt now dynamically includes `[Workspace Context]` or `[Learning Center Context]` based on where the user is, allowing the same model to act as a Code Auditor and a Teaching Assistant simultaneously.
- **Engagement Loop:** Hardcoded the instruction to provide proactive "Would you like to..." follow-ups to maximize student engagement.
**System Instruction:** "You are a Python Security & Education Mentor. "
                                "Your goal is to help users write secure code and understand cybersecurity concepts. "
                                "Be concise, encouraging, and always provide one brief \'Would you like to...\' "
                                "follow-up question at the end of every response."