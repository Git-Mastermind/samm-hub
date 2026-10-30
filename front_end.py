import streamlit as st
import requests

st.set_page_config(page_title="Spotlight API Tester", page_icon="⚡")

st.title("⚡ Spotlight Signup API Tester")
st.write("Use this interface to test your Flask `/signup` endpoint.")

api_url = st.text_input("Flask API Base URL", value="http://127.0.0.1:5000")

st.divider()

st.subheader("Add New User")

with st.form("signup_form"):
    name = st.text_input("Name", value="Alex Smith")
    email = st.text_input("Email", value="alex@example.com")
    
    # Password input field
    password = st.text_input("Password", type="password", value="securePass123")
    
    # Role Selection
    role_choice = st.selectbox(
        "Role Selection", 
        ["resident", "student", "teacher", "admin", "Custom..."]
    )
    
    custom_role = st.text_input("Enter Custom Role", value="") if role_choice == "Custom..." else ""
    
    community_id = st.number_input("Community ID", min_value=1, value=1, step=1)
    
    submitted = st.form_submit_button("Sign Up User")

if submitted:
    selected_role = custom_role.strip() if role_choice == "Custom..." else role_choice

    if not name or not email or not password:
        st.warning("Please fill in Name, Email, and Password.")
    elif "@" not in email:
        st.warning("Please enter a valid email address containing '@'.")
    elif role_choice == "Custom..." and not selected_role:
        st.warning("Please specify your custom role.")
    else:
        # Extract username (everything before the @)
        username = email.split("@")[0]

        # Calling /signup endpoint with query parameters
        endpoint = f"{api_url}/signup"
        params = {
            "name": name,
            "username": username,
            "email": email,
            "password": password,
            "role": selected_role,
            "community_id": community_id
        }
        
        try:
            response = requests.post(endpoint, params=params)
            
            if response.status_code == 201:
                st.success(f"✅ Success! Created user '{name}' (Username: **{username}**) with role '{selected_role}'.")
                st.json(response.json())
            else:
                st.error(f"❌ Failed with status code: {response.status_code}")
                st.text(response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to Flask API. Make sure your Flask server (`app.py`) is running on port 5000!")