"""
File: staff_directory.py
Function: Streamlit page for JCPAO directory (INTERNAL view for JCPAO employees)
Author: Joseph Cho, ujcho@jacksongov.org
Date: April 12, 2025
Updated: November 10, 2025
"""

import streamlit as st
from pathlib import Path 
import pandas as pd
import re


from read_data import MEMBERS # Load data
from photo import load_photo


MEMBERS['City'] = MEMBERS['agency_address'].str.split(',').str[1].str.strip()
MEMBERS['State'] = MEMBERS['agency_address'].str.split(',').str[2].str.strip()

# st.title("Staff Directory")
# TODO - directory pagination?

# # --- Configure Streamlit page settings --- 
# jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")

# # --- JCPAO Streamlit page logo --- 
# st.logo(jcpao_logo, size="large", link="https://www.jacksoncountyprosecutor.com")


# --- Initialize session state --- 

if "city" not in st.session_state:
    st.session_state["city"] = "All"

if "state" not in st.session_state:
    st.session_state["state"] = "All"

if "exec_board" not in st.session_state: # exec board ONLY? 
    st.session_state["exec_board"] = False

if "member_name" not in st.session_state:
    st.session_state["member_name"] = ""


# --- Define callback functions --- 

# Define update_df() function
def update_df():

    filtered_df = MEMBERS.copy()

    if st.session_state["city"] != 'All':
        filtered_df = filtered_df[filtered_df['agency_address'].str.contains(st.session_state["city"], case=False, na=False)].reset_index(drop=True)
    if st.session_state["state"] != 'All':
        filtered_df = filtered_df[filtered_df['State']==st.session_state["state"]].reset_index(drop=True)
    if st.session_state["exec_board"]:
        filtered_df = filtered_df[filtered_df['exec_board']].reset_index(drop=True)
    if st.session_state["member_name"]:
        # Update search function to split entered text into unique words, and check if any words appear in specified cols

        searched_text = st.session_state["member_name"].strip().lower()
        words = list({w for w in searched_text.split() if w}) # split search text into unique words
        search_cols = ["full_name", "agency_name", "job_title", "tools"]
        combined = filtered_df[search_cols].astype(str).agg(" ".join, axis=1).str.lower() # combine searchable columns into a single lowercase string per row
        mask = combined.apply(lambda text: any(word in text for word in words)) # match if ANY word appears in the combined text

        filtered_df = filtered_df[mask].reset_index(drop=True)

    st.session_state["df"] = filtered_df.reset_index(drop=True)

# Reset filters button
def reset_filters():
    st.session_state["city"] = "All"
    st.session_state["state"] = "All"
    st.session_state["exec_board"] = False
    st.session_state["member_name"] = ""
    # filtered_df = STAFF_DIRECTORY.copy()
    # st.session_state["staffview_filtered_df"] = filtered_df
    st.session_state["df"] = MEMBERS.copy()


# --- Sidebar Filter functions ---

with st.sidebar:
    # Select options: position / unit / location / birthday month 
    st.title("Mid-America Regional Crime Analysis Network (MARCAN)")
    st.write("***Member Directory***")
    st.divider()
    st.write("Please use the directory to view information on active MARCAN members!")
    st.divider()

    # Filter by Exec Board
    st.toggle(
        ":blue-badge[⭐️ **Executive Board:**]",
        key="exec_board",
        help="Filter directory to only members of the Executive Board",
        on_change=update_df,
    )
    
    # Filter by City
    cities_dict = {"All": "All"} | {
        f"{row['City']}, {row['State']}": f"{row['City']}, {row['State']}"
        for _, row in MEMBERS[['City', 'State']].dropna().drop_duplicates().iterrows()
    }
    cities_options = st.selectbox(
        label= ":blue-badge[**Filter by City:**]",
        options=cities_dict.keys(),
        index=0, # All
        format_func=lambda x: cities_dict[x],
        key='city',
        placeholder="Select city",
        on_change=update_df,
    )

    # Filter by State
    states_dict = {"All": "All"} | {k: k for k in MEMBERS['State'].dropna().unique()}
    states_options = st.selectbox(
        label= ":blue-badge[**Filter by State:**]",
        options=states_dict.keys(),
        index=0, # All
        format_func=lambda x: states_dict[x],
        key='state',
        placeholder="Select state",
        on_change=update_df,
    )

    # Reset filters 
    refresh = st.button(
        label="Reset Filters",
        key="reset",
        on_click=reset_filters,
        type="secondary",
        icon="🔄",
    )

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

# --- Internal Directory HELPER funcs --- 

def reformat_phone_num(phone_num):
    # Handle NaN values or non-string types 
    if not isinstance(phone_num, str) or pd.isna(phone_num):
        return phone_num
    
    # Check length is 10-digits, then reformat 
    if len(phone_num) == 10:
        return f"{phone_num[:3]}-{phone_num[3:6]}-{phone_num[6:]}"
    else:
        return phone_num

def to_bullet_list(text): # Separate by , ; \n \t (but not /)
    if not text:
        return ""
    items = re.split(r'[,;\n\t]+', str(text))
    items = [item.strip() for item in items if item.strip()]
    return "\n" + "\n".join(f"- {item}" for item in items)

def display_employee(row):

    with st.container():

        col1, col2 = st.columns([1,1.25], gap="small", vertical_alignment="center")

        with col1:
            
            # Headshot Photo (if None, JCPAO logo)
            marcan_logo = Path("assets/logo/marcan_logo.png")
            if not row['photo']:
                st.image(marcan_logo, width=400)
            else:
                # headshot_path = "headshots/"+row['work_email'].strip() # work_email to replace PhotoID
                headshot_path = row['work_email'].strip() # work_email to replace PhotoID
                staff_headshot = load_photo(headshot_path)
                st.image(staff_headshot, width=400)
                # st.write(headshot_path)
            
        with col2:
            exec_badge = f":blue-badge[⭐️ ***{row['exec_position']}***]" if row['exec_board'] else ""
            
            st.markdown(f"""
                # {row['full_name']}     
                {exec_badge}    

                **Agency:** {row['agency_name']}    
                **Job Title:** {row['job_title']}   
                **Work Email:** {row['work_email']}    
                **Work Phone:** {reformat_phone_num(row['work_phone'])}    
            """)

            bio = row['bio']
            add_exp_cleaned = row['add_exp'].replace('\n', ', ') if pd.notna(row['add_exp']) else None
            additional_experience = f"**Additional Experience:**\n{to_bullet_list(add_exp_cleaned)}" if add_exp_cleaned else ""
            tools = row['tools']

            with st.expander(f"**More about {row['full_name'].split()[0]}:**", expanded=False, width="stretch", icon=":material/person_book:"):
                st.markdown(f"""
                    **Biography:**      
                    {bio}      
                """)

                st.markdown(f"""
                    {additional_experience}
                """)

            with st.expander(f"**Software Tools:**", expanded=False, width="stretch", icon=":material/build:"):
                st.markdown(f"""
                    **Tools:**       
                    {to_bullet_list(tools)}      
                """)


        st.divider()

# --- Display INTERNAL Directory ---

# filtered_df = emp_view.copy()
# filtered_df.reset_index(drop=True, inplace=True)

df = st.session_state.get("df", MEMBERS.copy())

# Internal Directory title 
st.markdown("<h1 style='text-align: center; color: black;'>MARCAN Member Directory</h1>", unsafe_allow_html=True)
st.divider()

# Text Search feature 
searched_text = st.text_input(
    "Search employee name:",
    key="member_name"
)

text_search = st.button(
    "Search",
    icon="🔎",
    on_click=update_df,
    key="search_button",
)

st.divider()

if df.empty:
    st.info("No active MARCAN members found given the selected category filters.", icon="⚠️")
else:
    for i, row in df.iterrows():
        display_employee(row)





