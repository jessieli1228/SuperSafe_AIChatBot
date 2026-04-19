import streamlit as st
import google.generativeai as genai
import sqlite3

from database_utils import initialize_db, hash_password, verify_password, get_user_id, save_message, load_messages, clear_chat_history

initialize_db()

MODEL_MAPPING = {
    'gemma-3-27b-it (in-depth response)': 'models/gemma-3-27b-it',
    'gemini-flash-2.5 (standard response)': 'models/gemini-2.5-flash',
    'gemma-3-4b-it (fast response)': 'models/gemma-3-4b-it'
}
model_id = "models/gemini-2.5-flash"

if st.session_state.get('logged_in', False):
    with st.sidebar:
        st.title("Settings")
       
        selected_model_display = st.selectbox("Select Model", list(MODEL_MAPPING.keys()))
        
        model_id = MODEL_MAPPING[selected_model_display]



genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

from security_utils import generate_entropy_histogram_data

from streamlit_ace import st_ace

AVERAGE_BASELINE = 3.01
DANGER_THRESHOLD = 4.50
st.set_page_config(page_title="SuperSafe AI", layout="wide", initial_sidebar_state="collapsed")

def set_page(page):
    st.session_state.page = page

if "page" not in st.session_state:
    st.session_state.page = "home"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "files" not in st.session_state:
    st.session_state.files = {"main.py": ""}
if "active_file" not in st.session_state:
    st.session_state.active_file = "main.py"

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

if 'files' not in st.session_state:
    st.session_state.files = {"main.py": ""}
if 'active_file' not in st.session_state:
    st.session_state.active_file = 'main.py'
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
                conn = sqlite3.connect("users.db")
                c = conn.cursor()

                if st.session_state.auth_mode == "Login":
                    c.execute("SELECT * FROM users WHERE username = ?", (st.session_state.username,))
                    user = c.fetchone()
                    if user:
                        stored_hash, stored_salt = user[1], user[2]
                        if verify_password(st.session_state.password, stored_hash, stored_salt):
                            st.session_state.logged_in = True
                            st.session_state.user_id = get_user_id(st.session_state.username)
                            set_page("dashboard")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    else:
                        st.error("Invalid credentials")
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
    col1, col2 = st.columns([1, 1.2])
    with col1:
        if st.button('Clear Chat Memory', key='permanent_wipe', help='Deletes all chat messages and clears the current chat view.', use_container_width=True):
            st.session_state.messages = []
            st.session_state.hide_history = False
            st.success('Chat history wiped.')
            st.rerun()
    with col2:
        if st.button('Hide History (Memory Saved)', key='soft_clear', help='Clears view but keeps background memory.', use_container_width=True):
            st.session_state.messages = []
            st.session_state.hide_history = True
            st.success('Chat view cleared.')
            st.rerun()

    st.markdown("### 🤖 Security & Study Mentor")
    
    with st.container(height=650, border=True):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat Input
        if prompt := st.chat_input(f"Ask your {context_label} mentor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            save_message(st.session_state.user_id, 'user', prompt)
            with st.chat_message("user"):
                st.markdown(prompt)

            # --- THE UNIFIED BRAIN ---
            # We combine the Page Context (Code or Lesson) with the User Question
            full_message = f"[{context_label} Context]\n{context_data}\n\nUser Question: {prompt}"
            
            with st.chat_message("assistant"):
                # Define the system prompt text
                SYSTEM_PROMPT = (
                    "You are a Python Security & Education Mentor. "
                    "Your goal is to help users write secure code and understand cybersecurity concepts. "
                    "Be concise, encouraging, and always provide one brief follow-up question."
                )

                # Initialize the model using the ID selected in your sidebar
                if "gemini" in model_id.lower():
                    model = genai.GenerativeModel(
                        model_name=model_id,
                        system_instruction=SYSTEM_PROMPT
                    )
                    # Generate the response using the Google SDK syntax
                    response = model.generate_content(full_message)
                else: # For models that don't support system_instruction, like Gemma
                    model = genai.GenerativeModel(
                        model_name=model_id
                    )
                    # Prepend the system prompt to the message
                    full_message_with_system_prompt = f"{SYSTEM_PROMPT}\n\n{full_message}"
                    response = model.generate_content(full_message_with_system_prompt)
                answer = response.text
                
                st.markdown(answer)
                
                # Store the assistant's response
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

    with st.sidebar:
        st.markdown('### 📁 Project Files')
        for filename in st.session_state.files.keys():
            label = f'📄 {filename}' if filename == st.session_state.active_file else filename
            if st.button(label, key=f'file_button_{filename}', use_container_width=True):
                st.session_state.active_file = filename
                st.rerun()

        with st.expander('➕ New File', expanded=False):
            new_filename = st.text_input('New filename', key='new_filename_input')
            if st.button('Create File'):
                if new_filename and new_filename not in st.session_state.files:
                    st.session_state.files[new_filename] = ''
                    st.session_state.active_file = new_filename
                    st.rerun()
                elif new_filename:
                    st.error('File already exists.')
                else:
                    st.error('Filename cannot be empty.')

    with left_col:
        # --- TOP: Editor Box ---
        st.markdown(f"### 📝 {st.session_state.active_file}")
        
        # Create a temporary key that Streamlit uses to store the editor's live state
        editor_state_key = f"editor_state_{st.session_state.active_file}"

        code_content = st_ace(
            value=st.session_state.files.get(st.session_state.active_file, ""), 
            language="python", 
            theme="dracula", 
            height=500, 
            key=editor_state_key, # Use the state key
            auto_update=True  
        )

        # SINGLE Entropy Check Block
        if code_content:
            histogram_data = generate_entropy_histogram_data(code_content)
            if histogram_data: # Ensure we have data before calculating max
                max_entropy = max(histogram_data)
                if max_entropy > DANGER_THRESHOLD:
                    st.error(f"⚠️ CRITICAL RISK: High-entropy string detected ({max_entropy:.2f} bits).")

        # SYNC: Update the master dictionary quietly
        if code_content != st.session_state.files.get(st.session_state.active_file, ""):
            st.session_state.files[st.session_state.active_file] = code_content
            st.caption("✅ Syncing...")
        
        
        st.button("← Back to Dashboard", on_click=lambda: st.session_state.update({"page": "dashboard"}))

        # --- BOTTOM: Graph Box ---
        st.markdown("---")
        st.markdown("### 📊 Security Distribution")

        if st.button("🔍 Run Security Audit", use_container_width=True):
            if code_content:
                st.session_state.histogram_data = generate_entropy_histogram_data(code_content)
                st.session_state.max_entropy = max(st.session_state.histogram_data) if st.session_state.histogram_data else 0.0
            else:
                st.session_state.histogram_data = None
                st.session_state.max_entropy = 0.0
            st.rerun()

        st.caption("(or press CMD+ENTER)")

        if st.session_state.get("histogram_data"):
            import pandas as pd
            import plotly.graph_objects as go

            df = pd.DataFrame({"Line Number": range(1, len(st.session_state.histogram_data) + 1), "Entropy": st.session_state.histogram_data})
            colors = ["#FF4B4B" if entropy > DANGER_THRESHOLD else "#636EFA" for entropy in df["Entropy"]]
            fig = go.Figure(data=[go.Bar(x=df["Line Number"], y=df["Entropy"], marker_color=colors)])

            # Add reference lines
            fig.add_hline(y=AVERAGE_BASELINE, line_dash="dash", line_color="green", annotation_text=f"Average Baseline Entropy ({AVERAGE_BASELINE:.2f})", annotation_position="top right")
            fig.add_hline(y=DANGER_THRESHOLD, line_dash="solid", line_color="red", annotation_text=f"Danger ({DANGER_THRESHOLD:.2f})", annotation_position="top left")

            fig.update_layout(
                xaxis=dict(
                    tickmode='linear', 
                    tick0=1, 
                    dtick=1,
                    title="Line Number"
                ),
                yaxis_title="Entropy Score",
                font=dict(color="white"),
                margin=dict(l=20, r=20, t=20, b=20)
            )

            st.plotly_chart(fig, use_container_width=True, theme=None)
            st.metric(label="Max Line Entropy", value=f"{st.session_state.max_entropy:.2f}", delta=f"{st.session_state.max_entropy - DANGER_THRESHOLD:.2f}", delta_color="inverse")
        else:
            st.info("Click \"Run Security Audit\" to see entropy distribution.")

    with right_col:
        # Pass all files content as context
        all_files_content = """
"""
        for filename, content in st.session_state.files.items():
            all_files_content += f"File: {filename}\n```python\n{content}\n```\n\n"
        render_unified_chatbot("Workspace", all_files_content)

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

# Streamlit heartbeat fragment to keep the websocket connection alive
@st.fragment(run_every=60)
def heartbeat():
    with st.empty():
        # A small, invisible timer to keep the connection alive
        pass

heartbeat()