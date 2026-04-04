
import streamlit as st
from streamlit_ace import st_ace
from security_utils import generate_entropy_histogram_data, AVERAGE_BASELINE_ENTROPY
import sqlite3
from database_utils import initialize_db, hash_password, verify_password

def set_page(page):
    st.session_state.page = page

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if 'code_input' not in st.session_state:
    st.session_state.code_input = ''

def login_page():
    st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
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
            if st.form_submit_button("Login"):
                # Placeholder for actual database verification
                # For now, let's initialize the database and add a test user if it doesn't exist
                initialize_db()

                # Example: Add a test user if not exists
                # This part would typically be in a registration flow, not login
                # For demonstration, we'll keep it simple.
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username = ?", (st.session_state.username,))
                user = c.fetchone()

                if not user:
                    # Register new user (for demonstration purposes, in a real app this would be a separate registration flow)
                    hashed_password, salt = hash_password(st.session_state.password)
                    c.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                              (st.session_state.username, hashed_password, salt))
                    conn.commit()
                    conn.close()
                    st.success("User registered and logged in!")
                    st.session_state.logged_in = True
                    set_page("dashboard")
                    st.rerun()
                else:
                    # Verify password for existing user
                    stored_hash, stored_salt = user[1], user[2]
                    if verify_password(st.session_state.password, stored_hash, stored_salt):
                        st.session_state.logged_in = True
                        set_page("dashboard")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                conn.close()


def dashboard_page():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
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

    col1, col2, col3 = st.columns([2, 1, 1])

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
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
        <style>
            .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }
            .stSidebar {
                background-color: #1e1e1e;
                color: #ffffff;
                padding: 20px;
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

    with st.sidebar:
        st.markdown("<h2>Security Entropy Meter</h2>", unsafe_allow_html=True)
        st.progress(85) # Example progress
        st.write("Current code security level.")
        st.chat_input("Ask your AI Mentor:")

        st.markdown("<h3>Security Distribution</h3>", unsafe_allow_html=True)
        if st.session_state.code_input:
            histogram_data = generate_entropy_histogram_data(st.session_state.code_input)
            if histogram_data:
                import pandas as pd
                df = pd.DataFrame({"Line Number": range(1, len(histogram_data) + 1), "Entropy": histogram_data})
                st.bar_chart(df, x="Line Number", y="Entropy")
                st.info(f"Average Baseline Entropy: {AVERAGE_BASELINE_ENTROPY:.2f}")

                # High entropy alert logic
                for i, entropy_value in enumerate(histogram_data):
                    if entropy_value > AVERAGE_BASELINE_ENTROPY + 1.5:
                        st.warning(f"High Entropy Detected on Line {i+1}: This looks like a hardcoded secret (API Key or Password). Please move this to an environment variable.")
            else:
                st.info("Enter code to see entropy distribution.")
        else:
            st.info("Enter code to see entropy distribution.")

        st.button("Back to Dashboard", on_click=set_page, args=("dashboard",))

    st.markdown("<h1 style=\'color: #4CAF50;\'>Active Workspace</h1>", unsafe_allow_html=True)
    st_ace(value=st.session_state.code_input, language="python", theme="dracula", height=500, key="code_input")

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "workspace":
    workspace_page()
