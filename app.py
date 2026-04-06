
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
from database_utils import initialize_db, hash_password, verify_password

st.set_page_config(page_title='SuperSafe AI', layout='wide', initial_sidebar_state='collapsed')

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



    st.markdown("<h1 style='text-align: center;'>SuperSafe AI Mentor Login</h1>", unsafe_allow_html=True)

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

    st.markdown("<h1 style='color: #4CAF50;'>Dashboard</h1>", unsafe_allow_html=True)

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

    left_col, right_col = st.columns([0.75, 0.25])

    with left_col:
        st.title('Active Workspace')
        code_content = st_ace(value=st.session_state.code_input, language="python", theme="dracula", height=500, key="code_editor")

        if code_content:
            histogram_data = generate_entropy_histogram_data(code_content)
            max_entropy = max(histogram_data) if histogram_data else 0.0
            if max_entropy > DANGER_THRESHOLD:
                st.error(f'⚠️ CRITICAL RISK: High-entropy string detected above {DANGER_THRESHOLD:.2f} bits.')

            st.markdown("<h3>Security Distribution</h3>", unsafe_allow_html=True)
            if histogram_data:
                import pandas as pd
                import plotly.graph_objects as go

                df = pd.DataFrame({"Line Number": range(1, len(histogram_data) + 1), "Entropy": histogram_data})
                colors = ["#FF4B4B" if entropy > DANGER_THRESHOLD else "#636EFA" for entropy in df["Entropy"]]
                fig = go.Figure(data=[go.Bar(x=df["Line Number"], y=df["Entropy"], marker_color=colors)])

                # Add vertical reference lines
                fig.add_hline(y=AVERAGE_BASELINE, line_dash="dash", line_color="green", annotation_text="Average Baseline Entropy", annotation_position="top right")
                fig.add_hline(y=DANGER_THRESHOLD, line_dash="solid", line_color="red", annotation_text="Danger", annotation_position="top left")

                fig.update_layout(
                    xaxis_title="Line Number",
                    yaxis_title="Entropy Score",
                    font=dict(color="white")
                )

                st.plotly_chart(fig, use_container_width=True, theme=None)
                st.metric(label="Max Line Entropy", value=f"{max_entropy:.2f}", delta=f"{max_entropy - DANGER_THRESHOLD:.2f}", delta_color="inverse")
            else:
                st.info("Enter code to see entropy distribution.")
            st.button("Back to Dashboard", on_click=set_page, args=("dashboard",))

        else:
            st.info("Enter code to see entropy distribution.")
        


    with right_col:
        st.markdown("<h3>AI Mentor</h3>", unsafe_allow_html=True)
        if "messages" not in st.session_state:
            st.session_state.messages = [{ "role": "model", "text": "Hello! I\"m your AI Security Mentor. How can I help you code securely today?"}]

        with st.container(height=500):
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["text"])
        
        if prompt := st.chat_input("Ask your mentor..."):
            st.session_state.messages.append({"role": "user", "text": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            full_prompt = f"""You are a Security Mentor. Explain if the code is safe based on the entropy scores. Here is the code: {code_content}\nHere is the user\'s question: {prompt}"""

            messages = [
                {"role": "system", "content": "You are a professional secure coding mentor."},
                {"role": "user", "content": f"Please analyze the security of the following code:\n\n{code_content}"}
            ]

            completion = client.chat.completions.create(
                model="gemini-2.5-flash", 
                messages=messages
            )


            ai_response = completion.choices[0].message.content
            st.write(ai_response)


if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "workspace":
    workspace_page()
