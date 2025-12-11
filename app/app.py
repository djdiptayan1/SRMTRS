import streamlit as st
import json
from profilePage import profilePage  # Importing the profile function


# Load faculty data from JSON file
def load_faculty_data():
    with open("../data/faculties_data_new.json", "r") as file:
        data = json.load(file)
    return data


# Search faculty by name
def search_faculty(name, data):
    results = []
    name = name.lower()
    for faculty in data:
        full_name = faculty["FacultyName"].lower()
        if name in full_name:
            results.append(faculty)
    return results


# Display faculty card with link to profile page
def faculty_card(faculty):
    # Unique key based on faculty name
    key = faculty["FacultyName"]
    # Use a Streamlit form to handle the click event
    with st.form(key=key):
        st.image(faculty["ImageURL"], use_column_width=True)
        st.markdown(f"**{faculty['FacultyName']}**")
        st.markdown(f"**Department:** {faculty['DepartmentName']}")
        st.markdown(f"**Designation:** {faculty['Designation']}")
        st.markdown(f"**Specialization:** {faculty['Specialization']}")
        # Submit button inside the form
        submit_button = st.form_submit_button(label="View Profile")
        if submit_button:
            st.session_state["selected_faculty"] = faculty
            st.session_state["view"] = "profile"
            st.set_query_params(
                view="profile"
            )  # Update query params to reflect the change


# Set page configuration
st.set_page_config(page_title="Know Your Enemy", layout="wide")

# Initialize session state
if "view" not in st.session_state:
    st.session_state["view"] = "search"
if "selected_faculty" not in st.session_state:
    st.session_state["selected_faculty"] = None

# Load faculty data
faculty_data = load_faculty_data()

# Check the current view and render accordingly
if st.session_state["view"] == "search":
    st.markdown(
        "<h1 style='text-align: center;'>Know your Enemy 🔍</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h2 style='text-align: center;'>Search for any SRM Faculty</h2>",
        unsafe_allow_html=True,
    )

    name = st.text_input("Enter the name of the faculty", placeholder="e.g., John Doe")
    if name:
        results = search_faculty(name, faculty_data)
        if results:
            cols = st.columns(2)  # Use columns to display the results
            for index, result in enumerate(results):
                with cols[index % 2]:
                    faculty_card(result)  # Display each faculty card
        else:
            st.write("Faculty not found.")
    else:
        st.write("Please enter a faculty name to search.")
elif st.session_state["view"] == "profile" and st.session_state["selected_faculty"]:
    profilePage(st.session_state["selected_faculty"])
