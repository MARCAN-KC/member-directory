import streamlit as st
from pathlib import Path


# --- Initialize links ---

# Online links 
marcan_home = r"https://www.marcan.org/home"
iaca_home = r"https://www.iaca.net/"
member_form = r"https://form.jotform.com/260976583293067"

# Office social media
jcpao_twitter = r"https://x.com/MARCANBoard"
jcpao_facebook = r"https://www.facebook.com/MidAmericaCrimeAnalysts"
jcpao_instagram = r"https://www.instagram.com/marcanboard"
jcpao_youtube = r""
jcpao_linkedin = r""


# --- Sidebar Filter functions --- 
with st.sidebar:

    st.title("Mid-America Regional Crime Analysis Network (MARCAN)")
    st.write("***MARCAN Resources***")
    st.divider()
    st.write("Cick on any of the resources below to open in a new tab. If you would like to add other resources, please reach out to *VP of Administration* [Joseph Cho](mailto:ujcho@jacksongov.org).")
    st.divider()
    st.write("To securely exit portal, logout or just exit page:")

    # Logout 
    logout = st.button(
        label="Logout",
        key="logout",
        on_click=lambda: st.session_state.clear(), # Clear session state
        type="secondary",
        icon=":material/logout:"
    )


# --- Run page ---

st.markdown("<h1 style='text-align: center; color: black;'>Directory Resources</h1>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2, gap="medium", vertical_alignment="top", border=False, width="stretch")

with col1:

    # Online links
    st.header("Online Links", divider="blue")

    st.page_link(marcan_home, label="MARCAN Home Page", icon="⚖️")
    st.page_link(iaca_home, label="IACA Home Page", icon="⚖️")

    # Additional resources
    st.page_link(member_form, label="MARCAN Member Directory Form", icon="📝")

with col2:

    # Office social media
    st.header("Office Social Media", divider="blue")

    st.page_link(jcpao_twitter, label="Twitter", icon="🐦")
    st.page_link(jcpao_facebook, label="Facebook", icon="📘")
    st.page_link(jcpao_instagram, label="Instagram", icon="📸")
    # st.page_link(jcpao_youtube, label="YouTube", icon="📺")
    # st.page_link(jcpao_linkedin, label="LinkedIn", icon="🔗")

