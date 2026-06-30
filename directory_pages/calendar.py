import streamlit as st

# --- Links ---
calendar_link = r"https://www.marcan.org/metro-intel"

# --- Sidebar Filter functions --- 
with st.sidebar:

    st.title("Mid-America Regional Crime Analysis Network (MARCAN)")
    st.write("***MARCAN Calendar***")
    st.divider()
    st.write("MARCAN Meeting Calendar information is also available on the MARCAN website [here](https://www.marcan.org/metro-intel).")
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

st.markdown("<h1 style='text-align: center; color: black;'>MARCAN Calendar</h1>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2, gap="medium", vertical_alignment="top", border=False, width="stretch")

with col1:
    # Monthly Meetings
    st.header("Monthly Meetings", divider="blue")
    st.markdown("""
        MARCAN meetings are held at 10AM every third Thursday of the month, with locations rotating between MARCAN agencies in the Kansas City KS-MO Metro area. 
        Metro Intel meetings are held at 11AM, following MARCAN meetings. Metro Intel meetings are attended by analysts, detectives, probation/parole officers, and other law enforcement personnel. 
        The aim of Metro Intel meetings is to allow agency representatives to share crime intelligence, notable subjects of interest, and other information relevant to effective police operations.
    """)

    st.markdown("""
        **2026 MARCAN Calendar:**
        - January 15th @ Lee's Summit PD
        - February 19th @ Lenexa Justice Center
        - March 19th @ Lee's Summit PD
        - :red[NO MEETING in April] (MARCAN Conference April 15-16, 2026)
        - May 21st @ Independence PD
        - June 18th @ Lenexa Justice Center
        - July 16th @ Independence PD
        - August 20th @ Lenexa Justice Center
        - September 17th @ Independence PD
        - October 15th @ Lenexa Justice Center
        - November 19th @ Independence PD
        - :red[NO MEETING in December] (Holiday Party TBD)
    """)

with col2: 
    # Meeting locations
    st.header("Meeting Locations", divider="blue")

    st.info("MARCAN meetings start at 10AM, followed by Metro Intel meetings at 11AM, on the third Thursday of every month at one of the following locations:", icon=":material/info:")

    with st.expander("**Independence Police Department**", expanded=False):
        st.markdown("""
            > Independence Police Department        
            > [17221 E 23rd St S](https://maps.app.goo.gl/EqDBce8JdshsdjvKA)        
            > [Independence, MO 64057](https://maps.app.goo.gl/EqDBce8JdshsdjvKA)        
            > Enter through the main doors and the meeting room is to the *right*        
        """)

        st.iframe("""
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3097.2911727294604!2d-94.37754038794091!3d39.077064935964!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x87c102ca31d70fd3%3A0xd0637b6d2916269f!2s17221%20East%2023rd%20St%20S%2C%20Independence%2C%20MO%2064057!5e0!3m2!1sen!2sus!4v1782858744282!5m2!1sen!2sus" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>
        """)

    with st.expander("**Lenexa Justice Center**", expanded=False):        
        st.markdown("""
            > Lenexa Justice Center        
            > [17371 Prairie Star Pkwy](https://maps.app.goo.gl/zM2x6MwcbXWU4ZEB6)        
            > [Lenexa, KS 66219](https://maps.app.goo.gl/zM2x6MwcbXWU4ZEB6)        
            > Enter through the main doors and the meeting room is to the *left*        
        """)

        st.iframe("""
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3102.637210999598!2d-94.7892045879452!3d38.95511564317769!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x87c0946bb2708803%3A0x4724beb500fd847!2s17371%20Prairie%20Star%20Pkwy%2C%20Lenexa%2C%20KS%2066219!5e0!3m2!1sen!2sus!4v1782858811620!5m2!1sen!2sus" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>
        """)
