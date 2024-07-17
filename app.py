import streamlit as st
import json
from urllib.error import URLError


def load_faculty_data():
    with open("faculties_data.json", "r") as file:
        data = json.load(file)
    return data


def search_faculty(name, data):
    results = []
    name = name.lower()
    for faculty in data:
        full_name = faculty["FacultyName"].lower()
        if name in full_name:
            results.append(faculty)
    return results


def faculty_card(faculty, col):
    with col:
        container = st.container()
        with container:
            try:
                st.image(faculty["ImageURL"], use_column_width=True)
            except:
                st.image("./avater.png", use_column_width=True)
            st.header(f"**Name:** {faculty['FacultyName']}")
            st.write(f"**Department:** {faculty['DepartmentName']}")
            st.write(f"**Designation:** {faculty['Designation']}")
            st.write(f"**Specialization:** {faculty['Specialization']}")
            st.write(f"[Profile Link]({faculty['ProfileLink']})")
        st.write("---")


st.set_page_config(page_title="Know Your Enemy", layout="wide")
st.markdown(
    "<h1 style='text-align: center;'>Know your Enemy 🔍</h1>", unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center;'>Search for any SRM Faculty</h2>",
    unsafe_allow_html=True,
)


name = st.text_input("Enter the name of the faculty", placeholder="e.g., John Doe")

faculty_data = load_faculty_data()

if name:
    results = search_faculty(name, faculty_data)
    if results:
        cols = st.columns(2)
        for index, result in enumerate(results):
            col = cols[index % 2]
            faculty_card(result, col)
    else:
        st.write("Faculty not found.")
else:
    st.write("Please enter a faculty name to search.")
