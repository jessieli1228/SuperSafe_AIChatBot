import streamlit as st
import sqlite3
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://api.apiyi.com/v1"
)
from security_utils import generate_entropy_histogram_data

from streamlit_ace import st_ace

AVERAGE_BASELINE = 3.01
DANGER_THRESHOLD = 4.50
from database_utils import initialize_db, hash_password, verify_password, get_user_id, save_message, load_messages, clear_chat_history
st.set_page_config(page_title="SuperSafe AI", layout="wide", initial_sidebar_state="collapsed")

def set_page(page):
    st.session_state.page = page

if "page" not in st.session_state:
    st.session_state.page = "home"


def home_page():
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        div[data-testid="stVerticalBlock"] {
            background-color: #1e1e1e;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 800px; /* Set max-width for the home container */
            margin: 0 auto;   /* Center the home container */
            text-align: center;
        }
        h1 {
            color: #4CAF50;
            font-size: 2.5em;
            margin-bottom: 0.5em;
        }
        p {
            color: #cccccc;
            font-size: 1.1em;
            line-height: 1.6;
            margin-bottom: 2em;
        }
        .stButton > button {
            width: auto;
            padding: 10px 30px;
            border-radius: 20px;
            border: 1px solid #4CAF50;
            color: #ffffff;
            background-color: #4CAF50;
            font-size: 1.2em;
            cursor: pointer;
            display: block;
            margin: 0 auto;
        }
        .stButton > button:hover {
            background-color: #45a049;
            border-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style=\'text-align: center;\'>" \
                "<h1>SuperSafe: AI-powered Secure Coding</h1>" \
                "<p>An interactive AI coding mentor that identifies security risks—like hard-coded API keys—and teaches developers to build safer, production-ready software.</p>" \
                "</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True) # Add some space
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if 'code_input' not in st.session_state:
    st.session_state.code_input = ''
def login_page():
    # Toggle between Login and Sign Up
    st.session_state.auth_mode = st.radio("", ["Login", "Sign Up"], key="auth_toggle_radio", horizontal=True)



    st.markdown("<h1 style=\'text-align: center;\'>SuperSafe AI Mentor Login</h1>", unsafe_allow_html=True)

    with st.container():
        st.markdown(f"""
            <style>
                .stApp {{ 
                    background-color: #0e1117;
                    color: #ffffff;
                }}
                .stTextInput > label {{ 
                    color: #ffffff;
                }}
                .stButton > button {{ 
                    width: 100%;
                    border-radius: 20px;
                    border: 1px solid #4CAF50;
                    color: #ffffff;
                    background-color: #4CAF50;
                }}
                .stButton > button:hover {{ 
                    background-color: #45a049;
                    border-color: #45a049;
                }}
                div[data-testid="stVerticalBlock"] {{ 
                    background-color: #1e1e1e;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                    max-width: 400px;
                    margin: 0 auto;
                }}
                h1 {{ 
                    color: #4CAF50;
                }}
            </style>
        """, unsafe_allow_html=True)
        
        st.write("") # For spacing
        st.write("") # For spacing
        st.write("") # For spacing

        with st.form("login_form"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            submit_text = 'Login' if st.session_state.auth_mode == 'Login' else 'Create Account'
            if st.form_submit_button(submit_text):
                # Placeholder for actual database verification
                initialize_db()
                conn = sqlite3.connect("users.db")
                c = conn.cursor()

                if st.session_state.auth_mode == "Login":
                    c.execute("SELECT * FROM users WHERE username = ?", (st.session_state.username,))
                    user = c.fetchone()
                    if user:
                        stored_hash, stored_salt = user[1], user[2]
                        if verify_password(st.session_state.password, stored_hash, stored_salt):
                            st.session_state.logged_in = True
                            st.session_state.user_id = user[0]  # Store user_id
                            st.session_state.messages = load_messages(st.session_state.user_id) # Load messages
                            set_page("dashboard")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Invalid username or password")
                else: # Sign Up mode
                    c.execute("SELECT * FROM users WHERE username = ?", (st.session_state.username,))
                    user = c.fetchone()
                    if user:
                        st.error("Username already exists. Please choose a different one.")
                    else:
                        hashed_password, salt = hash_password(st.session_state.password)
                        c.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                                  (st.session_state.username, hashed_password, salt))
                        conn.commit()
                        st.success("Account created successfully! Please log in.")

                conn.close()

def dashboard_page():

    st.markdown("""
        <style>
            .stApp { 
                background-color: #0e1117;
                color: #ffffff;
            }
            .stMetric > div > div:first-child { /* Value */
                color: #4CAF50;
            }
            .stMetric > div > div:nth-child(2) { /* Label */
                color: #cccccc;
            }
            div[data-testid="stVerticalBlock"] {
                background-color: #1e1e1e;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                margin-bottom: 20px;
            }
            .stButton > button {
                width: 100%;
                border-radius: 15px;
                border: 1px solid #007bff;
                color: #ffffff;
                background-color: #007bff;
            }
            .stButton > button:hover {
                background-color: #0056b3;
                border-color: #0056b3;
            }
            h2 {
                color: #4CAF50;
            }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.warning("Please login to access the dashboard.")
        set_page("login")
        st.rerun()
        return

    st.markdown("<h1 style=\'color: #4CAF50;\'>Dashboard</h1>", unsafe_allow_html=True)

    # Top stats bar
    st.write("### Security Points")
    st.metric(label="Total Points", value="1250", delta="50")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        with st.container():
            st.markdown("<h2>Resume Session</h2>", unsafe_allow_html=True)
            st.progress(70)
            st.write("Continue your last secure coding session.")
            st.button("Resume", on_click=set_page, args=("workspace",))

    with col2:
        with st.container():
            st.markdown("<h2>New Code Segment</h2>", unsafe_allow_html=True)
            st.write("Start analyzing a new piece of code.")
            st.button("Start New", on_click=set_page, args=("workspace",))

    with col3:
        with st.container():
            st.markdown("<h2>Training Modules</h2>", unsafe_allow_html=True)
            st.write("Enhance your secure coding skills.")
            st.button("Browse Modules", on_click=set_page, args=("training",))

# New unified chatbot render function
def render_unified_chatbot(context_label, context_data=""):
    """
    One bot to rule them all. 
    Handles both Workspace code and Learning Page tutorials.
    """
    st.markdown("### 🤖 Security & Study Mentor")

    if "hide_history" not in st.session_state:
        st.session_state.hide_history = False

    st.markdown("""
        <style>
            .stButton > button {
                font-size: 12px !important;
                padding: 4px 8px !important;
                border-radius: 5px !important;
                height: auto !important;
                width: auto !important;
            }
            .clear-chat-memory-button > button {
                background-color: #e0e0e0 !important;
                color: #333333 !important; 
                border: 1px solid #c0c0c0 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])
    with col1:
        if st.button("Clear Chat Memory", key="permanent_wipe", help="Deletes all chat messages from the database and clears the current chat view.", use_container_width=True):
            clear_chat_history(st.session_state.user_id)  # Clear DB
            st.session_state.messages = []  # Clear UI Memory
            st.session_state.hide_history = False # Reset hide_history
            st.success("Chat history wiped locally and on disk.")
            st.rerun()  # Force the whole app to restart.
    with col2:
        if st.button("Hide History (Memory Saved)", key="soft_clear", help="Clears the current chat view, but keeps messages in the database for future context.", use_container_width=True):
            st.session_state.messages = []  # Clear UI Memory
            st.session_state.hide_history = True
            st.success("Chat view cleared.")
            st.rerun()  # Force the whole app to restart.

    with st.container(height=650, border=True):
        # Only load messages from DB if not hiding history and current session messages are empty
        if not st.session_state.hide_history and ("messages" not in st.session_state or not st.session_state.messages):
            st.session_state.messages = load_messages(st.session_state.user_id)

        # Display history conditionally
        if not st.session_state.hide_history:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat Input
        if prompt := st.chat_input(f"Ask your {context_label} mentor..."):
            # If new messages are being added, ensure full history (from DB) is in session_state
            if st.session_state.hide_history:
                st.session_state.hide_history = False # Reset hide_history when user sends a new message
                st.session_state.messages = load_messages(st.session_state.user_id) # Reload all messages from DB

            st.session_state.messages.append({"role": "user", "content": prompt})
            save_message(st.session_state.user_id, 'user', prompt)
            with st.chat_message("user"):
                st.markdown(prompt)

            # --- THE UNIFIED BRAIN ---
            # We combine the Page Context (Code or Lesson) with the User Question
            full_message = f"[{context_label} Context]\n{context_data}\n\nUser Question: {prompt}"
            
            # Include all past messages for context, including the new system message if present
            ai_messages = []
            if st.session_state.messages and st.session_state.messages[0]["role"] == "system":
                ai_messages.append(st.session_state.messages[0])
            ai_messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] != "system"])
            
            ai_messages.append({"role": "user", "content": full_message})

            with st.chat_message("assistant"):
                response = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are a Python Security & Education Mentor. "
                                "Your goal is to help users write secure code and understand cybersecurity concepts. "
                                "Be concise, encouraging, and always provide one brief \\\"Would you like to...\\\" "
                                "follow-up question at the end of every response."
                            )
                        },
                        *ai_messages # Pass all messages for context
                    ]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                save_message(st.session_state.user_id, "assistant", answer)

def workspace_page():

    st.markdown("""
        <style>
            .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }

            .stTextArea > label {
                color: #ffffff;
            }
            .stTextInput > label {
                color: #ffffff;
            }
            .stButton > button {
                width: 100%;
                border-radius: 15px;
                border: 1px solid #4CAF50;
                color: #ffffff;
                background-color: #4CAF50;
            }
            .stButton > button:hover {
                background-color: #45a049;
                border-color: #45a049;
            }
            h2, h3 {
                color: #4CAF50;
            }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.warning("Please login to access the workspace.")
        set_page("login")
        st.rerun()
        return

    # This creates the two-pane layout: 2 parts for code/graph, 1 part for chat
    left_col, right_col = st.columns([2, 1], gap="medium")

    with left_col:
        # --- TOP: Editor Box ---
        st.markdown("### 📝 Python Workspace")
        # Ensure the \'NoneType\' safety check we did earlier is still here
        editor_content = (st.session_state.get("code_editor") or "").strip()
        
        code_content = st_ace(value=st.session_state.code_input, language="python", theme="dracula", height=500, key="code_editor")

        if code_content:
            histogram_data = generate_entropy_histogram_data(code_content)
            max_entropy = max(histogram_data) if histogram_data else 0.0
            if max_entropy > DANGER_THRESHOLD:
                st.error(f"⚠️ CRITICAL RISK: High-entropy string detected above {DANGER_THRESHOLD:.2f} bits.")
        
        st.button("← Back to Dashboard", on_click=lambda: st.session_state.update({"page": "dashboard"}))

        # --- BOTTOM: Graph Box ---
        st.markdown("---")
        st.markdown("### 📊 Security Distribution")
        if code_content:
            if histogram_data:
                import pandas as pd
                import plotly.graph_objects as go

                df = pd.DataFrame({"Line Number": range(1, len(histogram_data) + 1), "Entropy": histogram_data})
                colors = ["#FF4B4B" if entropy > DANGER_THRESHOLD else "#636EFA" for entropy in df["Entropy"]]
                fig = go.Figure(data=[go.Bar(x=df["Line Number"], y=df["Entropy"], marker_color=colors)])

                # Add reference lines
                fig.add_hline(y=AVERAGE_BASELINE, line_dash="dash", line_color="green", annotation_text=f"Average Baseline Entropy ({AVERAGE_BASELINE:.2f})", annotation_position="top right")
                fig.add_hline(y=DANGER_THRESHOLD, line_dash="solid", line_color="red", annotation_text=f"Danger ({DANGER_THRESHOLD:.2f})", annotation_position="top left")

                fig.update_layout(
                    xaxis_title="Line Number",
                    yaxis_title="Entropy Score",
                    font=dict(color="white")
                )

                st.plotly_chart(fig, use_container_width=True, theme=None)
                st.metric(label="Max Line Entropy", value=f"{max_entropy:.2f}", delta=f"{max_entropy - DANGER_THRESHOLD:.2f}", delta_color="inverse")
            else:
                st.info("Enter code to see entropy distribution.")
        else:
            st.info("Enter code to see entropy distribution.")

    with right_col:
        # Pass the editor code as context
        render_unified_chatbot("Workspace", editor_content)

def learning_page():

    left_col, right_col = st.columns([2, 1], gap="medium")

    with left_col:
        st.title("📚 Learning Center")
        
        # Category Selector
        level = st.radio("Select Level:", ["Beginner", "Intermediate"], horizontal=True)
        
        if level == "Beginner":
            st.markdown("### 🟢 Beginner: Introduction to Entropy")
            st.write("In this lesson, we learn why random-looking code is actually safer...")
            # Add more text tutorials here
        else:
            st.markdown("### 🟡 Intermediate: Secure Password Hashing")
            st.write("Learn how to use bcrypt and why salting prevents rainbow table attacks...")

        if st.button("← Back to Dashboard"):
            st.session_state.update({"page": "dashboard"})

    with right_col:
        # Pass the current level as context
        render_unified_chatbot("Learning Center", f"Current Level: {level}")


if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "workspace":
    workspace_page()
elif st.session_state.page == "training":
    learning_page()

# Streamlit heartbeat fragment to keep the websocket connection alive
@st.fragment(run_every=60)
def heartbeat():
    with st.empty():
        # A small, invisible timer to keep the connection alive
        pass

heartbeat()
