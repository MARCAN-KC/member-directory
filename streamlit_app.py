import streamlit as st
from pathlib import Path
import time
import base64

# from connect_data import log_user
from read_data import MEMBER_EMAILS, log_user
# st.write(MEMBER_EMAILS)

# --- Configure Streamlit page settings --- 

marcan_logo = Path("assets/logo/marcan_logo.png")

st.set_page_config(
    page_title="MARCAN Directory", # court-view only
    page_icon=marcan_logo, # cloudinary.CloudinaryImage('marcan_logo_200x200').build_url()
    layout="wide", # "centered" or "wide"
    initial_sidebar_state="auto", # "expanded" / "auto" / "collapsed"
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "mailto:ujcho@jacksongov.org", # To report a bug, please email
        'About': "The MARCAN Directory was built by Joseph Cho, MARCAN Vice President of Administration"
    }
)

# --- JCPAO Streamlit page logo ---
st.logo(marcan_logo, size="large", link="https://www.marcan.org/")

@st.cache_data
def get_logo_base64(path: Path) -> str:
    """Base64-encode the logo so it can be centered via custom HTML."""
    return base64.b64encode(path.read_bytes()).decode()

# --- Connect to database --- 

# --- Initialize st.session_state --- 
if "verified" not in st.session_state:
    st.session_state["verified"] = False

# st.write(st.session_state)

# --- Initialize callback functions --- 

def verify_attempt():
    """Verify form submission"""

    # Variables
    email = st.session_state["verified_email"]
    code = st.session_state["security_code"]
    security_code = st.secrets["security_codes"]["marcan"]

    # Check verification
    # TODO - add security of checking if the @jacksongov.org email actually exists/is active in the database prior to verification
    # if (email.endswith("@courts.mo.gov") or email.endswith("@jacksongov.org")) and code == security_code:
    if email in MEMBER_EMAILS and code == security_code:
        log_user(email) # also track ip address? [st.context.ip_address]
        success_message = st.success(f"Verification successful: *{st.session_state['verified_email']}*")
        time.sleep(2)
        success_message.empty()
        st.session_state["verified"] = True # Unlocks directory
    else:
        fail_message = st.error("Failed to verify user. Please try again with an authorized email and security code.")
        time.sleep(2)
        fail_message.empty()

# --- New user dialog ---

@st.dialog("New to the MARCAN Directory?", width="small")
def new_user_dialog():
    st.markdown(
        """
        The **MARCAN Member Directory** is *only* available to active MARCAN members who have completed the MARCAN Directory Form.

        To be added to the directory and gain access, please complete the
        [**New Member Registration Form**](https://form.jotform.com/260976583293067) below. Once submitted, your information
        will be reviewed and you will receive an email confirming your information and directory access.
        """
    )
    # st.divider()
    st.write(" ")
    st.page_link(
        "https://form.jotform.com/260976583293067",
        label="New Member Registration Form",
        icon=":material/open_in_new:",
    )


# --- Enter security code ---

def display_portal():
    """Display access portal"""

    # Custom vertical space (CSS)
    st.markdown(
        """
        <style>
        .space { margin-top: 100px; }
        </style>
        <div class="space"></div>
        """,
        unsafe_allow_html=True
    )

    # Display form
    cols = st.columns(
        3, 
        gap=None,
        vertical_alignment="top", # center / bottom
        border=False,
        width="stretch"
    )

    with cols[1]:

        # Centered MARCAN logo
        st.markdown(
            f"""
            <div style='text-align: center; margin-bottom: 36px;'>
                <img src='data:image/png;base64,{get_logo_base64(marcan_logo)}' width='200'>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Form to verify user
        with st.form(
            "verify_user",
            clear_on_submit=False,
            enter_to_submit=False,
            border=True,
            width="stretch",
            height="content"
        ):
            # st.markdown("<h1 style='text-align: center; color: black;'>Court-View Directory</h1>", unsafe_allow_html=True)
            # st.markdown(":small[*Please verify the following information to access the directory*]", unsafe_allow_html=True) # :material/gavel:
            st.markdown("<div style='text-align: center; font-size: 1.75rem; font-weight: bold; color: #000000;'>MARCAN Member Directory</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: small; color: #000000; margin-bottom: 20px;'>Please verify the following information to access the directory</div>", unsafe_allow_html=True)
            # st.divider()

            # Email
            verified_email = st.text_input(
                label="Enter email",
                placeholder=None,
                help=None,
                key="verified_email",
                disabled=st.session_state["verified"],
            )

            # Security code
            security_code = st.text_input(
                label="Enter authorized security code",
                placeholder=None,
                help=None,
                key="security_code",
                disabled=st.session_state["verified"],
                type="password",
            )

            # Submit
            verify_button = st.form_submit_button(
                label="Verify", # :material/keyboard_return:
                icon=":material/keyboard_return:",
                disabled=st.session_state["verified"],
                on_click=verify_attempt,
                type="primary",
                width="stretch"
            )

        # New user dialog trigger
        if st.button(
            "New user? Click here",
            key="new_user_btn",
            icon=":material/person_add:",
            type="tertiary",
            use_container_width=True,
        ):
            new_user_dialog()

# --- Run STREAMLIT APP via st.navigation --- 


# --- RUN STREAMLIT APP --- 

if not st.session_state["verified"]:
    display_portal() # Display verification portal

else: # st.session_state["verified"] == TRUE

    # Preserve st.session_state?
    # st.session_state["verified_email"] = st.session_state["verified_email"]

    # Display APA Directory 
    directory_pages = {
        "Home": [
            st.Page("directory_pages/welcome_page.py", title="MARCAN Portal", icon=":material/home:"), # 🏡 
        ],
        "Directory Information": [
            st.Page("directory_pages/staff_directory.py", title="Member Directory", icon=":material/contacts:"), # ☎️
            # st.Page("directory_pages/staff_birthdays.py", title="Staff Birthdays", icon=":material/cake:"), # 🎂
            # st.Page("directory_pages/court_directory.py", title="Court-view Directory", icon=":material/account_balance:"), # 🏛️
        ],
        "Resources": [
            # st.Page("court_view.py", title="JCPAO Attorney Directory", icon=":material/contact_page:"),
            # st.Page("directory_pages/staff_dashboard.py", title="Staff Dashboard", icon=":material/monitoring:"),
            # st.Page("directory_pages/faq.py", title="Frequently Asked Questions", icon=":material/question_mark:"),
            st.Page("directory_pages/resources.py", title="MARCAN Resources", icon=":material/support_agent:"),
            st.Page("directory_pages/calendar.py", title="MARCAN Calendar", icon=":material/calendar_month:"),
        ], 
    }

    court_pg = st.navigation(directory_pages, position="top")
    court_pg.run() 