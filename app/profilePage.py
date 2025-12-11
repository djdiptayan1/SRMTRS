import streamlit as st


def profilePage(faculty):
    # Back to search button
    if st.button("Back to Search Results"):
        st.session_state["view"] = "search"
        st.set_query_params(view="search")  # Update query params to reflect the change

    # Faculty information
    st.markdown(
        f"<h1 style='text-align: center;'>{faculty['FacultyName']}</h1>",
        unsafe_allow_html=True,
    )

    try:
        st.markdown(
            f"<div style='text-align: center;'><img src='{faculty['ImageURL']}' width='400' style='border-radius: 15px;'></div>",
            unsafe_allow_html=True,
        )
    except:
        st.markdown(
            "<div style='text-align: center;'><img src='../avater.png' width='400' style='border-radius: 15px;'></div>",
            unsafe_allow_html=True,
        )

    st.header(f"**Name:** {faculty['FacultyName']}")
    st.write(f"**Department:** {faculty['DepartmentName']}")
    st.write(f"**Designation:** {faculty['Designation']}")
    st.write(f"**Specialization:** {faculty['Specialization']}")
    # st.write(f"**Email:** {faculty.get('Email', 'N/A')}")
    # st.write(f"**Phone:** {faculty.get('Phone', 'N/A')}")
    # st.write(f"**Address:** {faculty.get('Address', 'N/A')}")
    st.write(f"[Profile Link]({faculty['ProfileLink']})")
    st.write("---")

    # Comments Section
    st.markdown("### Comments and Reviews")

    if "comments" not in st.session_state:
        st.session_state["comments"] = {}

    faculty_comments_key = f"comments_{faculty['FacultyName']}"

    if faculty_comments_key not in st.session_state["comments"]:
        st.session_state["comments"][faculty_comments_key] = []

    # Text input for new comment
    new_comment = st.text_input("Add a comment:")

    # Button to submit the comment
    if st.button("Submit Comment"):
        if new_comment:
            st.session_state["comments"][faculty_comments_key].append(new_comment)
            st.experimental_rerun()  # Rerun to update the comments display

    # Display comments
    for comment in st.session_state["comments"][faculty_comments_key]:
        st.write(f"- {comment}")
