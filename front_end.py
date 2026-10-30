import streamlit as st
import requests

st.set_page_config(page_title="Spotlight Auth Tester", page_icon="🔑", layout="centered")

st.title("🔑 Sammamish Spotlights Auth Tester")
st.write("Test your Flask `/signup` and `/login` API endpoints.")

# Flask API URL setup
api_url = st.text_input("Flask API Base URL", value="http://127.0.0.1:5000")

st.divider()

# Navigation tabs for testing both routes
tab_signup, tab_login = st.tabs(["📝 Sign Up", "🔐 Log In"])

# ==========================================
# TAB 1: SIGNUP TESTER
# ==========================================
with tab_signup:
    st.subheader("Create a New Account")
    
    # Placed outside the form so Streamlit re-renders immediately when "Custom..." is selected
    role_choice = st.selectbox(
        "Role", 
        ["resident", "student", "teacher", "admin", "Custom..."]
    )
    
    custom_role = ""
    if role_choice == "Custom...":
        custom_role = st.text_input("Enter Custom Role", value="", placeholder="e.g. volunteer")

    with st.form("signup_form"):
        name = st.text_input("Full Name", value="", placeholder="First Last")
        email = st.text_input("Email", value="", placeholder="user@example.com")
        password = st.text_input("Password", type="password", value="")
        community_id = st.number_input("Community ID", min_value=1, value=1, step=1)
        
        submitted_signup = st.form_submit_button("Sign Up")

    if submitted_signup:
        selected_role = custom_role.strip() if role_choice == "Custom..." else role_choice

        if not name or not email or not password:
            st.warning("Please fill out all required fields (Name, Email, Password).")
        elif "@" not in email:
            st.warning("Please enter a valid email containing '@'.")
        elif role_choice == "Custom..." and not selected_role:
            st.warning("Please enter a custom role.")
        else:
            # Extract username (everything before '@')
            username = email.split("@")[0]
            
            endpoint = f"{api_url}/signup"
            params = {
                "name": name,
                "email": email,
                "role": selected_role,
                "password": password,
                "community_id": community_id
            }
            
            try:
                response = requests.post(endpoint, params=params)
                
                if response.status_code == 201:
                    st.success(f"✅ Success! Created user **{name}** with username: `{username}`")
                    st.json(response.json())
                else:
                    st.error(f"❌ Failed ({response.status_code})")
                    st.json(response.json() if response.text else response.text)
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to Flask API. Is `app.py` running on port 5000?")

# ==========================================
# TAB 2: LOGIN TESTER
# ==========================================
with tab_login:
    st.subheader("Log Into Account")
    
    with st.form("login_form"):
        username = st.text_input("Username (e.g. alex from alex@example.com)", value="", placeholder="username")
        login_password = st.text_input("Password", type="password", value="")
        
        submitted_login = st.form_submit_button("Log In")

    if submitted_login:
        if not username or not login_password:
            st.warning("Please enter both Username and Password.")
        else:
            endpoint = f"{api_url}/login"
            params = {
                "username": username,
                "password": login_password
            }
            
            try:
                response = requests.post(endpoint, params=params)
                
                if response.status_code == 200:
                    st.balloons()
                    st.success(f"🎉 Login successful for username **{username}**!")
                    st.json(response.json())
                elif response.status_code == 400:
                    st.error("❌ Username not found in database.")
                    st.json(response.json())
                elif response.status_code == 401:
                    st.error("❌ Incorrect password.")
                    st.json(response.json())
                else:
                    st.error(f"❌ Unexpected status code: {response.status_code}")
                    st.text(response.text)
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to Flask API. Is `app.py` running on port 5000?")