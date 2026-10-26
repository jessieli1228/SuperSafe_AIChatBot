COURSE_CONTENT = {
    "Module 0: Foundations": {
        "0.1 Variables & Data Types": {
            "reading": """
            ### 🧱 Understanding Variables & Data Types
            In computer science, a variable is a named container that stores data values in computer memory. Python handles multiple data types automatically, including strings (`str`), integers (`int`), floating-point numbers (`float`), and booleans (`bool`). 
            
            ### ⚠️ The Security Risk
            Unchecked data types can lead to critical bugs or security crashes. For example, if an application expects an integer user age but receives a string containing malicious script characters or massive numbers, it can cause type coercion vulnerabilities or unhandled runtime exceptions.
            
            ### 🛠️ Best Practices
            * Always validate and cast external inputs at the boundary of your program.
            * Use explicit type-checking functions or libraries like Pydantic to ensure data integrity before processing.
            """,
            "security": "Mindset: Never assume data is the type you expect. Always validate and cast incoming data explicitly at system boundaries.",
            "code": """# Safe type casting with robust exception handling
user_input = "25"

try:
    user_age = int(user_input)
    print(f"Successfully processed valid integer age: {user_age}")
except ValueError:
    print("Security Alert: Invalid type supplied. Expected integer.")
"""
        },
        "0.2 The input() Function": {
            "reading": """
            ### 📥 Accepting User Input Safely
            The `input()` function prompts the user to type text into the console or UI terminal. While useful for interactive programs, raw input is completely untrusted data. Accepting raw strings without sanitization exposes programs to command injection and control flow manipulation.
            
            ### 🔍 How Attackers Exploit Input
            If an application takes raw input and passes it directly into system execution functions (like `os.system()`), an attacker can append malicious terminal commands (e.g., `; rm -rf /`) to wipe system data.
            
            ### 🛠️ Best Practices
            * Strip whitespace and enforce strict character whitelist filtering (alphanumeric only).
            * Never pass raw user strings directly into system shells or database queries.
            """,
            "security": "Mindset: All external input is guilty until proven innocent. Filter and sanitize before use.",
            "code": """# Sanitizing and validating user string input
raw_username = input("Enter your username: ")

# Strip whitespace and limit length
clean_username = raw_username.strip()[:15]

# Enforce alphanumeric character whitelist
if not clean_username.isalnum():
    raise ValueError("Access Denied: Username contains illegal special characters!")
"""
        },
        "0.3 If/Else Logic Gates": {
            "reading": """
            ### 🔀 Controlling Program Flow Securely
            Conditional statements (`if`, `elif`, `else`) dictate how an application responds to different states. In security architecture, conditional blocks govern access control checks, user permissions, and authentication verification.
            
            ### 🛡️ Fail-Closed Design Principle
            A secure application must always **fail closed**. This means that if an unexpected state occurs or a user role is unrecognized, the `else` fallback block must deny access by default rather than granting elevated permissions.
            
            ### 🛠️ Best Practices
            * Always include an explicit `else` or fallback exception handler that blocks unauthorized actions.
            * Avoid complex, nested conditional logic that obscures permission checks.
            """,
            "security": "Mindset: Default to denial. Ensure your fallback 'else' blocks reject access securely.",
            "code": """# Secure fail-closed authorization check
user_role = "unverified_guest"

if user_role == "admin":
    grant_admin_privileges()
elif user_role == "developer":
    grant_developer_access()
else:
    # Fail-closed default fallback
    print("Access Denied: Standard security restrictions enforced.")
"""
        },
        "0.4 Lists & Dictionaries": {
            "reading": """
            ### 📚 Managing Complex Data Structures
            Lists and dictionaries are foundational data structures used to group collections of items or map keys to values. In web applications, dictionaries often represent JSON payloads, user profiles, or database records.
            
            ### ⚠️ Index & Key Errors
            Attempting to access a dictionary key that does not exist raises an unhandled `KeyError`, while out-of-bounds list indices raise an `IndexError`. Attackers can trigger these crashes intentionally to cause denial of service or glean server debugging details from stack traces.
            
            ### 🛠️ Best Practices
            * Always use the `.get()` method when looking up dictionary keys to provide safe default values.
            * Check list lengths before accessing specific indices.
            """,
            "security": "Mindset: Never assume a dictionary key or list index exists. Always implement safe lookup patterns.",
            "code": """# Safe dictionary key retrieval with fallback defaults
user_record = {"username": "cyber_student", "role": "coder"}

# Safe lookup prevents KeyError crashes
user_email = user_record.get("email", "default-no-email@vaultcode.secure")
print(f"Retrieved email address: {user_email}")
"""
        },
        "0.5 F-Strings Security": {
            "reading": """
            ### 📝 Formatted Strings and Injection Risks
            Python f-strings (`f"Hello {name}"`) provide an elegant way to inject variables into strings. However, using f-strings to construct SQL queries, system commands, or HTML templates introduces devastating injection vulnerabilities (SQLi and XSS).
            
            ### 🚨 The Danger of Dynamic Interpolation
            When you build a database query using an f-string with user input, an attacker can manipulate the input string to alter the query logic entirely, bypassing authentication screens or extracting sensitive database tables.
            
            ### 🛠️ Best Practices
            * Use f-strings strictly for UI logging, console output, and debugging.
            * Never use f-strings for SQL queries, file paths, or shell commands. Use parameterized queries instead.
            """,
            "security": "Mindset: Use f-strings for logging and display text only—never for constructing executable code or queries.",
            "code": """# ❌ INSECURE: Building SQL queries with f-strings
# query = f"SELECT * FROM users WHERE user = '{user_input}'"

# ✅ SECURE: Safe logging and display formatting
dev_name = "Alex"
print(f"[VAULTCODE AUDIT LOG] Developer '{dev_name}' initiated security scan.")
"""
        },
        "0.6 Loops & DoS Risks": {
            "reading": """
            ### 🔄 Iteration Safety and Resource Limits
            Loops (`for` and `while`) allow applications to process repetitive tasks efficiently. However, unbounded `while` loops or poorly structured recursive calls can easily result in infinite loops.
            
            ### 💥 Denial of Service (DoS) via CPU Exhaustion
            If an infinite loop is triggered on a server handling user requests, it spikes CPU utilization to 100%, freezing the application thread and blocking all other users from accessing the system (Denial of Service).
            
            ### 🛠️ Best Practices
            * Always implement explicit iteration counters or timeout thresholds inside `while` loops.
            * Validate that loop termination conditions are guaranteed to change.
            """,
            "security": "Mindset: Every loop must have a guaranteed exit condition and an upper execution limit.",
            "code": """# Bounded loop with strict iteration limits
max_attempts = 3
current_attempt = 0

while current_attempt < max_attempts:
    if verify_connection():
        print("Connection established successfully.")
        break
    current_attempt += 1
    print(f"Attempt {current_attempt} failed. Retrying...")
else:
    print("Maximum retry limit reached. Halting process.")
"""
        }
    },
    "Module 1: Secrets": {
        "1.1 Identifying Secrets": {
            "reading": """
            ### 🔑 Recognizing Hardcoded Credentials
            Secrets include API keys, database passwords, private encryption keys, and JSON Web Tokens (JWTs). Hardcoding these sensitive strings directly into your Python scripts or web apps is one of the most common and dangerous programming mistakes.
            
            ### 🤖 Automated Scrapers
            Public code repositories are continuously scraped by automated botnets searching for hardcoded keys (like OpenAI keys, AWS keys, or GitHub tokens). Once discovered, these keys are stolen and abused within seconds.
            
            ### 🛠️ Best Practices
            * Never place production or test secrets in plain text inside source code.
            * Externalize all secrets into secure environment variables.
            """,
            "security": "Mindset: Treat any plain-text secret inside a codebase as already compromised.",
            "code": """# ❌ INSECURE: Hardcoded API Secret
# OPENAI_API_KEY = "sk-proj-9f8d7c6b5a4e3d2c1b0a..."

# ✅ SECURE: Loading secret dynamically from runtime environment
import os

api_key = os.getenv("VAULT_SECRET_API_KEY")
if not api_key:
    raise ValueError("Critical Error: Missing required environment secret!")
"""
        },
        "1.2 Environment Variables": {
            "reading": """
            ### 🌐 Isolating Configuration with Environment Variables
            Environment variables are key-value pairs stored in the operating system environment, separate from your source code. They allow your application to adapt its configuration across different environments (Development, Staging, Production) without modifying code.
            
            ### 🔒 Separation of Concerns
            By pulling credentials via `os.getenv()`, your repository remains completely safe to share on GitHub because zero sensitive credentials exist inside the physical files.
            
            ### 🛠️ Best Practices
            * Check for the existence of critical environment variables at startup and fail fast if they are missing.
            """,
            "security": "Mindset: Code is public; configuration is environment-specific.",
            "code": """import os

# Fetching configuration safely at application startup
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")

if not DATABASE_URL or not JWT_SECRET:
    raise RuntimeError("Startup Failed: Missing essential environment variables.")
"""
        },
        "1.3 The .env File Pattern": {
            "reading": """
            ### 📄 Local Development with .env Files
            During local development, managing operating system environment variables can be tedious. The `.env` file standard allows developers to store local key-value pairs in a single file parsed automatically by libraries like `python-dotenv`.
            
            ### 🛡️ Protecting Your Local Vault
            Your `.env` file acts as your local secrets vault. It must **never** be committed to version control or pushed to GitHub.
            
            ### 🛠️ Best Practices
            * Include a `.env.example` file in your repository with blank placeholder keys so other developers know what variables are required.
            """,
            "security": "Mindset: A .env file is a local secrets vault. Treat it with extreme care.",
            "code": """from dotenv import load_dotenv
import os

# Load local environment variables from .env file into memory
load_dotenv()

secret_token = os.getenv("LOCAL_SECRET_TOKEN")
print("Environment loaded securely.")
"""
        },
        "1.4 Mastering .gitignore": {
            "reading": """
            ### 🚫 Preventing Accidental Git Commits
            The `.gitignore` file tells Git which files and folders to ignore and exclude from tracking. If you fail to include `.env`, database files (`*.db`), or virtual environments (`.venv/`) in your `.gitignore`, Git will track them and push them to GitHub.
            
            ### 🕵️‍♂️ The Cost of a Single Mistake
            Pushing a single `.env` file containing live API keys to a public GitHub repo can result in automated bots stealing your credentials before you can even refresh the page.
            
            ### 🛠️ Best Practices
            * Configure your `.gitignore` file before initializing your first git repository (`git init`).
            * Regularly run `git status` to verify no secret files are staged.
            """,
            "security": "Mindset: Set up your .gitignore file before writing your first line of code.",
            "code": """# Standard .gitignore template for Python & Security Apps
.env
*.db
__pycache__/
.venv/
vault_logs/
secrets.json
"""
        },
        "1.5 Secret Rotation": {
            "reading": """
            ### 🔄 Rotating Compromised Credentials
            Secret rotation is the practice of periodically or emergency-revoking old API keys and replacing them with newly generated ones. If a secret is ever exposed or suspected of leaking, rotation neutralizes the threat immediately.
            
            ### ⚡ Zero-Downtime Rotation
            Enterprise applications support dual-key configurations so new keys can be introduced before old keys are retired, preventing application downtime during updates.
            
            ### 🛠️ Best Practices
            * Build systems that can accept fallback or secondary keys during transition phases.
            * Automate secret rotation schedules in production cloud environments.
            """,
            "security": "Mindset: Assume every secret will eventually leak. Build systems that support fast key rotation.",
            "code": """# Supporting dual-key rotation during transition periods
ACTIVE_KEY = os.getenv("VAULT_PRIMARY_KEY")
FALLBACK_KEY = os.getenv("VAULT_SECONDARY_KEY")

def validate_token(token):
    return token in (ACTIVE_KEY, FALLBACK_KEY)
"""
        },
        "1.6 Emergency Response": {
            "reading": """
            ### 🚨 Incident Handling for Leaked Keys
            If an API key is accidentally pushed to GitHub, automated scanners will exploit it within seconds. Knowing your emergency response protocol is vital for survival.
            
            ### 📋 Incident Response Steps
            1. **Revoke Immediately:** Go to the provider dashboard (OpenAI, AWS, GitHub) and revoke/delete the compromised key instantly.
            2. **Check Logs:** Review provider usage logs to see what data or credits the attacker accessed.
            3. **Clean History:** Purge the secret from your git commit history using tools like BFG Repo-Cleaner.
            """,
            "security": "Mindset: Deleting a commit message does not erase git history. Revoke the key first, clean history second.",
            "code": """# Emergency remediation terminal workflow:
# 1. Revoke key in provider console.
# 2. Use BFG to strip file from git history:
# bfg --delete-files .env
# git push origin --force --all
"""
        }
    },
    "Module 2: GitHub Walls": {
        "2.1 Public vs Private Repos": {
            "reading": """
            ### 🌐 Repository Visibility and Access
            GitHub repositories can be set to Public (visible to everyone on the internet) or Private (restricted to authorized collaborators). While private repositories offer a layer of privacy, they should still never contain hardcoded secrets because team members' accounts can be compromised.
            
            ### 🛡️ Defense-in-Depth
            Relying solely on a repository being "private" is a weak security posture. Codebases should remain secure and secret-free regardless of their public or private visibility status.
            
            ### 🛠️ Best Practices
            * Treat all private repositories as if they will become public tomorrow.
            * Enforce strict team collaborator access controls and MFA.
            """,
            "security": "Mindset: Never rely on repository privacy settings as your primary security control.",
            "code": "# Best Practice: Keep secrets externalized even inside private enterprise repositories."
        },
        "2.2 Branching Strategies": {
            "reading": """
            ### 🌿 Protected Branches and Git Workflows
            Pushing code directly to the `main` or `production` branch is a major risk that can introduce bugs or security vulnerabilities directly to users. Branching strategies (like Git Flow) enforce isolated feature development.
            
            ### 🔒 Branch Protection Rules
            Configuring branch protection on GitHub requires all pull requests to pass automated security checks and receive human peer reviews before merging into `main`.
            
            ### 🛠️ Best Practices
            * Lock down the `main` branch so direct pushes are blocked.
            * Always create feature branches for new code development.
            """,
            "security": "Mindset: Never push directly to main. Require status checks and reviews on all pull requests.",
            "code": """# Recommended Git workflow commands:
# git checkout -b feature/secure-authentication-fix
# git add .
# git commit -m "Fix: Implemented secure environment validation"
# git push origin feature/secure-authentication-fix
"""
        },
        "2.3 The Git History 'Ghost'": {
            "reading": """
            ### 👻 The Git History Ghost
            Git does not just save your current file state; it records every single snapshot and commit across the entire history of the project. If you hardcode a secret in Commit A and delete it in Commit B, the secret remains permanently accessible in Git's internal commit history database.
            
            ### 🔍 Finding Hidden Leaks
            Attackers use specialized search tools to crawl git logs of public repositories looking for historical commits that contained passwords or keys long after they were supposedly deleted.
            
            ### 🛠️ Best Practices
            * Use history-rewriting tools like BFG Repo-Cleaner or `git filter-branch` to completely purge leaked files from historical commits.
            """,
            "security": "Mindset: Deleting code line-by-line does not clear Git history. Clean the entire commit graph.",
            "code": """# Inspecting git commit history for hidden string patterns:
# git log -p -S 'sk_live_'
"""
        },
        "2.4 Pull Requests & Review": {
            "reading": """
            ### 👀 Peer Code Reviews as Security Gates
            Pull Requests (PRs) provide a collaborative workspace for reviewing code changes before they merge into the main project. Code reviews serve as an essential human defense layer, catching logic flaws and security vulnerabilities that automated tools might miss.
            
            ### 📋 Security Checklists
            Teams should enforce a mandatory PR review checklist covering input sanitization, error handling, and secret exclusion.
            
            ### 🛠️ Best Practices
            * Require at least one peer approval before any pull request can be merged.
            * Review code changes line-by-line with a security-first mindset.
            """,
            "security": "Mindset: Two sets of eyes are better than one. Never bypass code review policies.",
            "code": """# Example Pull Request Security Checklist:
# [x] No hardcoded keys or passwords present
# [x] All user inputs properly validated and sanitized
# [x] Unit tests passing successfully
"""
        },
        "2.5 Commit Signing": {
            "reading": """
            ### 🔏 Verifying Identity with GPG Commit Signing
            By default, Git allows anyone to forge commit author names and email addresses easily. GPG (GNU Privacy Guard) commit signing uses cryptographic key pairs to cryptographically verify that a commit was genuinely authored by the verified account owner.
            
            ### 🛡️ Preventing Impersonation
            Commit signing ensures that malicious actors cannot spoof developer identities or inject unverified code into open-source repositories under false pretenses.
            
            ### 🛠️ Best Practices
            * Generate a GPG key pair, link it to your GitHub account, and enable mandatory commit signing.
            """,
            "security": "Mindset: Verify developer identity using cryptographic proof rather than trusting plain-text headers.",
            "code": """# Signing a git commit cryptographically:
# git commit -S -m "Feat: Implemented secure session token hashing"
"""
        },
        "2.6 Dependabot Alerts": {
            "reading": """
            ### 🤖 Automated Dependency Scanning with Dependabot
            Modern applications rely heavily on open-source third-party packages (e.g., in `requirements.txt` or `package.json`). When security flaws (CVEs) are discovered in these libraries, Dependabot automatically scans your project and alerts you.
            
            ### ⚡ Automated Remediation
            Dependabot doesn't just alert you—it generates automated pull requests to upgrade vulnerable packages to safe, patched versions instantly.
            
            ### 🛠️ Best Practices
            * Enable Dependabot alerts and security updates on all your GitHub repositories.
            * Promptly merge dependency security patches.
            """,
            "security": "Mindset: Outdated third-party packages are an open doorway. Patch dependencies as soon as alerts arise.",
            "code": """# Example Dependabot configuration file (.github/dependabot.yml)
# version: 2
# updates:
#   - package-ecosystem: "pip"
#     directory: "/"
#     schedule:
#       interval: "daily"
"""
        }
    },
    "Module 3: Safe Tools": {
        "3.1 Package Typosquatting": {
            "reading": """
            ### 📦 Understanding Package Typosquatting
            Typosquatting is a supply-chain attack where malicious actors publish fraudulent packages on package registries (like PyPI or npm) with names visually similar to popular libraries (e.g., `reqeusts` instead of `requests`).
            
            ### 🦠 Malicious Installation Payload
            When an unwary developer makes a typo during installation (`pip install reqeusts`), the malicious package installs successfully and executes hidden scripts that steal SSH keys or env variables.
            
            ### 🛠️ Best Practices
            * Double-check spelling when installing packages or updating `requirements.txt`.
            * Use lockfiles and verified package registries.
            """,
            "security": "Mindset: Double-check package spellings in installation commands and requirements files.",
            "code": """# ❌ Dangerous Typo Installation:
# pip install reqeusts

# ✅ Verified Official Package Installation:
# pip install requests
"""
        },
        "3.2 Virtual Environments": {
            "reading": """
            ### 🗂️ Isolating Dependencies with Virtual Environments
            Python virtual environments (`.venv`) create isolated, self-contained directory structures for individual projects. This ensures project dependencies don't conflict with global system packages or other projects.
            
            ### 🛡️ Clean Project Boundaries
            Developing inside a virtual environment prevents permission issues, namespace pollution, and unexpected system library overwrites.
            
            ### 🛠️ Best Practices
            * Always create and activate a virtual environment before starting any new Python project.
            * Add `.venv/` to your `.gitignore` file immediately.
            """,
            "security": "Mindset: Always develop inside an isolated virtual environment to prevent system-wide package pollution.",
            "code": """# Terminal commands to create and activate virtual environment (macOS/Linux):
# python3 -m venv .venv
# source .venv/bin/activate
"""
        },
        "3.3 Verified Extensions": {
            "reading": """
            ### 🔌 Securing IDE Extensions and Plugins
            Code editors like VS Code rely on extensions to add functionality. However, extensions run with the full permissions of your user account on your local machine. Installing unverified extensions from unknown publishers can expose your workspace files and terminal.
            
            ### 🕵️‍♂️ Spyware & Keyloggers
            Malicious extensions can silently harvest environment variables, code snippets, and API keys stored in open editor windows.
            
            ### 🛠️ Best Practices
            * Install extensions exclusively from verified publishers with established community trust ratings and blue checkmarks.
            """,
            "security": "Mindset: Install IDE extensions exclusively from verified publishers with high trust ratings.",
            "code": "# Verify publisher badges and download counts in the VS Code Extension Marketplace before installing."
        },
        "3.4 MFA/2FA Defense": {
            "reading": """
            ### 🛡️ Multi-Factor Authentication (MFA/2FA)
            Passwords alone are easily compromised through phishing, brute-force attacks, or data breaches. MFA/2FA requires developers to present two or more verification factors (e.g., password + authenticator app code or hardware security key).
            
            ### 🌐 Securing Developer Accounts
            Mandating MFA on GitHub, AWS, and cloud deployment dashboards protects your organization even if individual account passwords are stolen.
            
            ### 🛠️ Best Practices
            * Enable TOTP authenticator apps or hardware security keys (YubiKey) on all developer accounts.
            """,
            "security": "Mindset: Passwords alone are insufficient protection. Mandate hardware keys or TOTP authenticators.",
            "code": "# Enforce mandatory MFA policies across all GitHub organization members and contributors."
        },
        "3.5 SSH vs HTTPS": {
            "reading": """
            ### 🔐 Secure Git Authentication: SSH vs HTTPS
            HTTPS Git authentication requires typing tokens or passwords repeatedly, whereas SSH authenticates using cryptographic public/private key pairs (`~/.ssh/id_ed25519`).
            
            ### 🛡️ Tokenless Encryption
            SSH keys provide strong, encrypted authentication without exposing plain-text passwords or personal access tokens over network streams.
            
            ### 🛠️ Best Practices
            * Generate strong Ed25519 SSH keys for Git authentication.
            * Protect private SSH keys with strong passphrases.
            """,
            "security": "Mindset: Protect private SSH keys with strong passphrases and store public keys securely on remote servers.",
            "code": """# Generating a secure Ed25519 SSH key pair for GitHub:
# ssh-keygen -t ed25519 -C "developer@vaultcode.secure"
"""
        },
        "3.6 Supply Chain Integrity": {
            "reading": """
            ### ⛓️ Software Supply Chain Security
            Modern software is built like a puzzle from hundreds of third-party open-source libraries. Supply chain security focuses on verifying the integrity of every component, dependency, build runner, and plugin in your software pipeline.
            
            ### 🔒 Cryptographic Pinning
            Using exact version pinning and hash verification ensures that third-party packages cannot be silently tampered with by upstream attackers.
            
            ### 🛠️ Best Practices
            * Pin exact package versions in dependency files.
            * Regularly audit packages for known vulnerabilities.
            """,
            "security": "Mindset: Pin exact dependency versions using hash verification and lockfiles.",
            "code": """# Example pinned requirement with cryptographic hash verification:
# requests==2.31.0 --hash=sha256:5820a4570b7218386f...
"""
        }
    },
    "Module 4: Patterns": {
        "4.1 Input Sanitization": {
            "reading": """
            ### 🧹 Preventing Injection with Input Sanitization
            Input sanitization involves stripping, cleaning, or escaping dangerous characters (`<`, `>`, `'`, `"`, `;`) from user data before processing. This prevents attackers from injecting malicious script tags (Cross-Site Scripting / XSS) or database commands.
            
            ### 🛡️ Filter on Entry, Encode on Exit
            The golden rule of web application security is to filter data as it enters your system and encode it safely when rendering it back to users.
            
            ### 🛠️ Best Practices
            * Use built-in HTML escaping libraries to neutralize special characters.
            * Never trust raw user input in web templates.
            """,
            "security": "Mindset: Filter data on entry; encode data on exit.",
            "code": """import html

# Sanitizing user-provided text before rendering in HTML
raw_user_comment = "<script>alert('xss attack!')</script>"
safe_rendered_comment = html.escape(raw_user_comment)

print(safe_rendered_comment) 
# Outputs safely: &lt;script&gt;alert(&#x27;xss attack!&#x27;)&lt;&#x2F;script&gt;
"""
        },
        "4.2 Principle of Least Privilege": {
            "reading": """
            ### 👤 The Principle of Least Privilege (PoLP)
            The Principle of Least Privilege dictates that users, processes, database connections, and API keys should only be granted the absolute minimum permissions required to perform their specific task—nothing more.
            
            ### 💥 Limiting the Blast Radius
            If an application component is compromised, strict adherence to PoLP ensures that the attacker's access is heavily restricted, preventing a complete system takeover.
            
            ### 🛠️ Best Practices
            * Never connect to databases using `root` or `admin` user accounts for standard application queries.
            * Restrict cloud service role permissions strictly to necessary resources.
            """,
            "security": "Mindset: Grant access on a strict need-to-have basis. Avoid root or admin accounts for routine tasks.",
            "code": """# ✅ Connect database using restricted, read-only permissions for reporting queries:
# DB_USER = "analytics_readonly_user"
# DB_PASS = os.getenv("READONLY_DB_PASSWORD")
"""
        },
        "4.3 Encryption at Rest": {
            "reading": """
            ### 💽 Protecting Data at Rest
            Encryption at rest ensures that sensitive data stored in files, SQLite databases, or cloud storage buckets is encrypted using robust algorithms like AES-256. If raw storage media is stolen, the data remains unreadable ciphertext without the decryption key.
            
            ### 🛡️ Cryptographic Protection
            Storing sensitive records (like passwords, personal metadata, or tokens) in plain text on disk is a critical security failure.
            
            ### 🛠️ Best Practices
            * Encrypt all sensitive database fields and local files.
            * Keep encryption keys completely separate from encrypted storage volumes.
            """,
            "security": "Mindset: Plain-text data on disk is vulnerable data. Cryptographically protect stored records.",
            "code": """from cryptography.fernet import Fernet

# Generate encryption key & initialize cipher
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Encrypt sensitive user record before disk storage
encrypted_record = cipher_suite.encrypt(b"Confidential user metadata record")
print("Data encrypted successfully for storage at rest.")
"""
        },
        "4.4 Secure Error Messages": {
            "reading": """
            ### 🛑 Preventing Information Disclosure via Errors
            Displaying detailed stack traces, database schema details, or server directory paths in production error messages provides attackers with valuable reconnaissance information.
            
            ### 🛡️ Friendly UI, Secure Logs
            Applications should return sanitized, generic error messages to end-users while logging full technical stack traces privately to secure internal logging aggregators.
            
            ### 🛠️ Best Practices
            * Disable debug mode in production environments.
            * Catch broad exceptions gracefully and display friendly fallback messages.
            """,
            "security": "Mindset: Show users simple friendly error messages; log full stack traces internally to secure servers.",
            "code": """try:
    execute_database_query()
except Exception as internal_error:
    # Log detailed stack trace privately for developers
    print(f"[INTERNAL LOG] Database failure: {internal_error}")
    # Return sanitized generic error message to end user
    print("User Output: An unexpected error occurred. Please try again later.")
"""
        },
        "4.5 Rate Limiting": {
            "reading": """
            ### ⏱️ Throttling Request Volumes with Rate Limiting
            Rate limiting restricts the number of API or login requests a client can submit within a specific timeframe. It protects services from automated brute-force password guessing, credential stuffing, scraping bots, and Denial of Service outages.
            
            ### 💰 Cost and Resource Control
            Uncapped APIs allow malicious bots to spam endpoints, exhausting server CPU and running up massive cloud infrastructure bills.
            
            ### 🛠️ Best Practices
            * Enforce strict rate limits on authentication and AI generation endpoints.
            """,
            "security": "Mindset: Uncapped endpoints are vulnerable to automated abuse and unexpected server cost spikes.",
            "code": """# Conceptual rate-limiting check
REQUEST_COUNTS = {}

def check_rate_limit(client_ip):
    current_count = REQUEST_COUNTS.get(client_ip, 0)
    if current_count > 50:
        return False  # Rate limit exceeded
    REQUEST_COUNTS[client_ip] = current_count + 1
    return True
"""
        },
        "4.6 HTTPS & TLS": {
            "reading": """
            ### 🔒 Protecting Data in Transit with HTTPS & TLS
            Transport Layer Security (TLS/HTTPS) encrypts all data transmitted over networks between client browsers and server backends. Without HTTPS, data travels in plain text.
            
            ### 🛜 Defending Against Eavesdropping
            On public Wi-Fi networks, unencrypted HTTP traffic can be easily intercepted by Man-In-The-Middle (MITM) attackers sniffing network packets to steal session cookies and login credentials.
            
            ### 🛠️ Best Practices
            * Enforce HTTPS across all application endpoints.
            * Implement HSTS (HTTP Strict Transport Security) headers.
            """,
            "security": "Mindset: HTTP sends clear text across public networks. Enforce HTTPS across all application endpoints.",
            "code": "# Server Configuration: Enable HSTS headers to force browsers to connect exclusively via secure HTTPS."
        }
    },
    "Module 5: Robots": {
        "5.1 Secret Scanning Bots": {
            "reading": """
            ### 🛡️ Automated Credential Discovery with Secret Scanners
            Secret scanning bots are automated security tools integrated into code hosting platforms and CI/CD pipelines. They continuously scan source code, commit history, and pull requests for exposed API keys using regular expressions and entropy analysis.
            
            ### ⚡ Shifting Left
            Catching leaked keys locally before code is ever pushed to remote servers prevents exposure entirely.
            
            ### 🛠️ Best Practices
            * Integrate automated secret scanning tools into your pre-commit hooks and GitHub workflows.
            """,
            "security": "Mindset: Automate security scanning inside CI/CD pipelines to catch human oversights immediately.",
            "code": """# Example pre-commit hook configuration (.pre-commit-config.yaml)
# repos:
#   - repo: https://github.com/Yelp/detect-secrets
#     rev: v1.4.0
#     hooks:
#       - id: detect-secrets
"""
        },
        "5.2 Bandit Static Analysis": {
            "reading": """
            ### 🐍 Python Static Security Testing with Bandit
            Bandit is a static application security testing (SAST) tool designed specifically to scan Python source code for security flaws, such as dangerous function calls (`exec()`), hardcoded passwords, or weak cryptography.
            
            ### 🔍 Catching Flaws Early
            Static analyzers review code structure without executing it, allowing developers to identify and fix security vulnerabilities during development.
            
            ### 🛠️ Best Practices
            * Run Bandit scans automatically as part of your pull request testing pipeline.
            """,
            "security": "Mindset: Run static code analyzer audits automatically on every pull request.",
            "code": """# Command line execution for Python Bandit security analysis:
# bandit -r ./your_vaultcode_project
"""
        },
        "5.3 Automated Testing": {
            "reading": """
            ### 🧪 Security-Focused Unit Testing
            Automated test suites verify that application components operate securely under various edge cases. Security tests should explicitly verify that invalid inputs are rejected, authentication errors trigger 403 blocks, and rate limits function correctly.
            
            ### 🛡️ Regression Prevention
            Writing security tests ensures that future code changes do not accidentally reintroduce patched vulnerabilities.
            
            ### 🛠️ Best Practices
            * Write negative test cases that verify security controls block unauthorized behavior successfully.
            """,
            "security": "Mindset: Write tests that verify insecure behavior is blocked, not just that normal features work.",
            "code": """def test_unauthorized_admin_access():
    # Simulate guest user attempting to access admin route
    response_status = 403  # Expected Forbidden block
    assert response_status == 403, "Security violation: Unauthorized access granted!"
"""
        },
        "5.4 Dependency Scanning": {
            "reading": """
            ### 📦 Auditing Packages with Dependency Scanners
            Tools like `pip-audit` scan your installed Python libraries against global vulnerability databases (such as NVD and CVE records) to discover known security exploits in third-party dependencies.
            
            ### 🔄 Staying Up-to-Date
            Even if your custom code is perfectly secure, an outdated third-party library can provide an attacker with a backdoor into your application.
            
            ### 🛠️ Best Practices
            * Regularly run dependency audits and update packages immediately when vulnerabilities are patched.
            """,
            "security": "Mindset: Regularly audit and update project dependencies to eliminate known package CVE vulnerabilities.",
            "code": """# Running Python dependency vulnerability audits via terminal:
# pip-audit
"""
        },
        "5.5 Infrastructure as Code": {
            "reading": """
            ### ☁️ Securing Infrastructure as Code (IaC)
            Infrastructure as Code tools like Terraform, Dockerfiles, and Kubernetes manifests define cloud servers in code. Security scanners inspect IaC files for misconfigurations (like open SSH ports or public storage buckets) before provisioning cloud servers.
            
            ### 🛡️ Secure Defaults
            Containers and servers should always run with restricted non-root privileges by default.
            
            ### 🛠️ Best Practices
            * Scan IaC templates for security misconfigurations automatically.
            """,
            "security": "Mindset: Treat infrastructure code with the same security rigor as application logic.",
            "code": """# Dockerfile secure default non-root user definition:
# USER nonroot
"""
        },
        "5.6 AI Security Mentors": {
            "reading": """
            ### 🤖 Real-Time AI Code Auditing & Mentorship
            AI security mentors (like VaultCode's internal engine) combine static entropy scanning with Large Language Model context analysis to provide real-time code vulnerability feedback and remediation tips directly inside developer workspaces.
            
            ### 💡 Empowering Developers
            AI mentors act as continuous educational companions, teaching developers secure coding practices as they write code.
            
            ### 🛠️ Best Practices
            * Use AI code assistants to review code for security risks before pushing commits.
            """,
            "security": "Mindset: Leverage AI tools as real-time security companions to learn safer coding patterns continuously.",
            "code": """# VaultCode Real-Time AI Security Pipeline:
# 1. User inputs code snippet into workspace
# 2. Entropy & regex engine scans for hardcoded secrets
# 3. AI mentor analyzes context and generates secure remediation advice
"""
        }
    }
}