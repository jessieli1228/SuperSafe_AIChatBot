# content.py

COURSE_CONTENT = {
    "Module 0: Foundations": {
        "0.1 Variables & Data Types": {
            "reading": """
            Variables are the fundamental storage units in Python. When you create a variable like `user_id = 101`, Python allocates space in the system's RAM. Understanding the difference between **Mutable** (changeable) and **Immutable** (unchangeable) types is a core security skill.
            
            For instance, Strings and Integers are immutable. If you try to change them, Python creates a new object. However, Lists are mutable. In a secure application, if you pass a list of 'Allowed Permissions' to a function, a malicious function could alter that list in place, granting unauthorized access.
            """,
            "security": "Use type-hinting in Python (e.g., `user_id: int`) to prevent unexpected data types from causing logic crashes."
        },
        "0.2 The input() Function": {
            "reading": """
            The `input()` function is the bridge between the user's keyboard and your CPU. By default, Python treats all input as a string. This is the 'Entry Point' for almost every classic cyberattack. 
            
            Because you cannot control what a user types, you must assume every character is an attempt to break the system. If you execute raw input, your app is compromised. Secure coding starts with the assumption that all input is 'Dirty' until it has been scrubbed.
            """,
            "security": "The 'Golden Rule': Filter at the entrance, encode at the exit. Never let raw input touch internal logic."
        },
        "0.3 If/Else Logic Gates": {
            "reading": """
            Conditional logic creates the 'Decision Trees' of your software. In security, these are your gates. A common mistake is using 'Loose Equality.' For example, checking `if user == 'admin'` without verifying a session token. 
            
            Professional secure coding uses 'Strict Validation'—checking for multiple factors before granting access. If the logic is flawed, the entire fortress is useless.
            """,
            "security": "Always use 'Default Deny.' Your `else` statement should always be the most restrictive option."
        },
        "0.4 Lists & Dictionaries": {
            "reading": """
            Data structures like Lists and Dictionaries manage complex info, such as user profiles. The risk here is 'Insecure Direct Object Reference' (IDOR). 
            
            If your app uses a list index to fetch a profile (e.g., `profiles[10]`), a hacker might change the number to `11` to see someone else's data. Always cross-reference the current session ID with the specific data key being requested.
            """,
            "security": "Never assume a user has access to an item just because they know its index or ID."
        },
        "0.5 F-Strings Security": {
            "reading": """
            F-Strings (`f"Hello {name}"`) are fast, but they are not a security feature. They evaluate variables within them. When building sensitive strings—like SQL queries—you must use 'Parameterized' methods. 
            
            Concatenation is even worse because it treats user input as a literal part of the string structure, which allows 'Injection' attacks.
            """,
            "security": "F-strings are for the UI; Parameterized queries are for the Database."
        },
        "0.6 Loops & DoS Risks": {
            "reading": """
            Loops allow for automation but are targets for 'Denial of Service' (DoS). If a hacker provides input that causes a loop to run indefinitely, they can 'peg' your CPU at 100%, crashing the app. 
            
            In secure coding, you must implement 'Time-to-Live' (TTL) or maximum iteration counts to ensure a process can be killed if it cycles too many times.
            """,
            "security": "Always set a maximum limit for loop iterations when processing user-submitted data."
        }
    },
    "Module 1: Secrets": {
        "1.1 Identifying Secrets": {
            "reading": "A 'Secret' is data that proves identity, like API keys. 'Hardcoding' these is a critical failure. If you can see a password in your source code, any person or bot with access to that file now owns your account.",
            "security": "If it grants access, it's a secret. Never type it directly into a .py file."
        },
        "1.2 Environment Variables": {
            "reading": "Environment Variables live 'outside' your program. Instead of writing the key in code, you fetch it from the OS. This separates your logic (the code) from your identity (the key).",
            "security": "Use `os.getenv()` to keep sensitive data out of your source control."
        },
        "1.3 The .env File Pattern": {
            "reading": "The .env file is a local text file for secrets. Python reads it into memory during runtime. It allows you to use different keys for 'Testing' vs 'Production' without changing code.",
            "security": "Treat .env like your physical keys—keep it on your machine, never in the cloud."
        },
        "1.4 Mastering .gitignore": {
            "reading": ".gitignore is a 'Blindfold' for Git. By listing `.env` inside it, you ensure that secrets aren't accidentally uploaded to GitHub. It's the most basic defense for every developer.",
            "security": "Create your .gitignore BEFORE your first commit to ensure clean history."
        },
        "1.5 Secret Rotation": {
            "reading": "Security is a cycle, not a one-time setup. 'Secret Rotation' means changing keys regularly. This limits the 'Blast Radius' if a key is ever stolen.",
            "security": "If you suspect a leak, change the key immediately. Don't wait for proof of a hack."
        },
        "1.6 Emergency Response": {
            "reading": "If you push a secret to GitHub, deleting the file won't help because Git stores the entire history. You must 'Invalidate' the key at the source (like Google Cloud) so it stops working.",
            "security": "1. Kill the key. 2. Notify the team. 3. Scrub the Git history."
        }
    },
    "Module 2: GitHub Walls": {
        "2.1 Public vs Private Repos": { "reading": "Private repos are not vaults. If your account is compromised, every secret in every private repo is stolen. Always code as if your repository is public.", "security": "Private repos protect intellectual property, but 'Secrets' should still be handled via environment variables." },
        "2.2 Branching Strategies": { "reading": "Never write code directly on the 'Main' branch. Create 'Feature Branches' to test code. If you make a security mistake, you can delete the branch before it ever hits the live version.", "security": "Protect the Main branch in GitHub settings to prevent unreviewed code pushes." },
        "2.3 The Git History 'Ghost'": { "reading": "Git is a 'Time Machine.' A password deleted today still exists in the hidden `.git` folder. Hackers use automated tools to 'dig' through history for forgotten keys.", "security": "Use `git status` and `git diff` to audit exactly what you are about to save." },
        "2.4 Pull Requests & Review": { "reading": "A Pull Request (PR) is a formal checkpoint. It allows a teammate to spot security flaws—like hardcoded keys—before they are merged into the final project.", "security": "The 'Four-Eyes' principle caught 90% of simple errors in professional software." },
        "2.5 Commit Signing": { "reading": "Identity spoofing is common on GitHub. 'Commit Signing' uses cryptographic keys to prove a commit actually came from you and hasn't been tampered with.", "security": "A 'Verified' badge on GitHub is your digital signature of authenticity." },
        "2.6 Dependabot Alerts": { "reading": "Your app relies on external libraries. If one has a security hole, so do you. Dependabot scans your libraries and automatically creates PRs to fix them.", "security": "Merge security-related Dependabot PRs immediately to stay protected." }
    },
    "Module 3: Safe Tools": {
        "3.1 Package Typosquatting": { "reading": "Hackers create fake packages like `requesst` instead of `requests`. One typo during installation can install a virus on your machine.", "security": "Always copy-paste install commands from official documentation like PyPI." },
        "3.2 Virtual Environments": { "reading": "A `venv` keeps your project isolated. If you accidentally install a bad package, it's trapped in that folder and can't see your other project files.", "security": "Always work inside a virtual environment to limit the impact of malicious packages." },
        "3.3 Verified Extensions": { "reading": "VS Code extensions have full access to your files. Only install tools from verified publishers with high ratings to prevent 'Extension-based' data theft.", "security": "Audit your extensions list and remove tools you don't recognize or use." },
        "3.4 MFA/2FA Defense": { "reading": "Multi-Factor Authentication is the ultimate shield. Even if a hacker steals your password, they cannot access your account without your phone's code.", "security": "Enable 2FA on GitHub, your Email, and your Cloud providers immediately." },
        "3.5 SSH vs HTTPS": { "reading": "SSH keys are more secure for pushing code. They prove your identity using public-key cryptography without ever sending a password over the wire.", "security": "Switch your Git remote to use SSH for a more secure and convenient workflow." },
        "3.6 Supply Chain Integrity": { "reading": "The 'Supply Chain' is every tool you use. Only download installers from official sites. 'Cracked' software often contains hidden backdoors.", "security": "The security of your app is only as strong as the security of the tools you used to build it." }
    },
    "Module 4: Patterns": {
        "4.1 Input Sanitization": { "reading": "Sanitization is the process of removing 'illegal' characters. If you expect a number, reject anything with a semicolon or bracket to prevent code injection.", "security": "Use 'Whitelisting'—explicitly define what is allowed and reject everything else." },
        "4.2 Principle of Least Privilege": { "reading": "Give your code only the power it needs. A script that only reads a file should not have permission to delete it or access the internet.", "security": "Run your local apps as a standard user, never as an 'Administrator' or 'Root'." },
        "4.3 Encryption at Rest": { "reading": "If you store user data in a local file, it must be encrypted. If the hardware is stolen, the data remains unreadable without the key.", "security": "Use the `cryptography` library in Python to secure sensitive local data files." },
        "4.4 Secure Error Messages": { "reading": "Generic errors leak folder paths and database names. This 'Information Leakage' helps hackers map your system for an attack.", "security": "Use `try/except` to show users a safe message while logging the 'Real' error privately." },
        "4.5 Rate Limiting": { "reading": "Rate limiting stops automated bots from trying thousands of passwords a second. It forces them to slow down, making attacks impractical.", "security": "Implement a 'Cool Down' period after three failed login or access attempts." },
        "4.6 HTTPS & TLS": { "reading": "HTTPS creates an encrypted tunnel so that no one on your Wi-Fi can 'eavesdrop' on your data. It is mandatory for any modern web application.", "security": "Always ensure your hosting environment (like Streamlit Cloud) provides an SSL certificate." }
    },
    "Module 5: Robots": {
        "5.1 Secret Scanning Bots": { "reading": "GitHub robots scan every commit. If they see an API key, they alert you and the key provider in seconds to prevent unauthorized use.", "security": "Never ignore a 'Secret Scanning' alert—hackers use the same bots to find your keys." },
        "5.2 Bandit Static Analysis": { "reading": "Bandit is a 'Robot' for Python that finds security holes—like weak encryption or hardcoded keys—automatically as you write code.", "security": "Run `pip install bandit` and audit your script before every major update." },
        "5.3 Automated Testing": { "reading": "You can write 'Security Tests' that check if your gates are working. These run every time you save, ensuring you don't accidentally break a security feature.", "security": "Automated security tests ensure that security is a 'Repeatable' process." },
        "5.4 Dependency Scanning": { "reading": "Tools like Snyk check if your `requirements.txt` includes libraries with known vulnerabilities. They provide one-click fixes for these bugs.", "security": "Update your packages weekly to stay ahead of known security vulnerabilities." },
        "5.5 Infrastructure as Code": { "reading": "By writing code to build your servers, you ensure that security settings (like firewalls) are identical and never 'forgotten' by a human.", "security": "Manual configuration is the leading cause of security misconfigurations in the cloud." },
        "5.6 AI Security Mentors": { "reading": "AI tools like this one can help you audit your logic. However, never paste a real production secret into an AI chat for debugging.", "security": "Use AI to understand 'How' to secure your code, but keep the actual 'Keys' to yourself." }
    }
}