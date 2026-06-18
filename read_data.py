import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Engine, text
from dotenv import load_dotenv
import os

load_dotenv("../marcan.env", override=True)  # points up to parent directory


# --- Initialize database connection pool ---

# SQLALCHEMY - Define get_engine()
@st.cache_resource
def get_engine(database_url):
    return create_engine(
        database_url, # st.secrets["sqlalchemy"]["database_url"]
        pool_size=10,
        max_overflow=5,
        pool_pre_ping=True,
        pool_timeout=60,
    )

# Establish NEON database connection (via sqlalchemy)
try:
    database_url = st.secrets["sqlalchemy"]["database_url"]
except Exception:
    database_url = os.getenv("SQLALCHEMY_DATABASE_URL")

# Attempt connection
try:
    engine = get_engine(database_url)
except Exception as e:
    print(f"{e}")
    st.stop()

# SQLALCHEMY: Read tables from NeonDB
@st.cache_data(show_spinner="Loading directory, please wait...") # ttl=3600*24*7, 
def query_table(sql_query: str, _engine: Engine = engine) -> pd.DataFrame:
    if _engine is None:
        return pd.DataFrame()

    try:
        with _engine.connect() as conn:
            return pd.read_sql(text(sql_query), conn)
    except Exception as e:
        st.error(f"Database query failed: {e}")
        return pd.DataFrame()
    
# Define function that returns ACTIVE members' work email addresses
@st.cache_data
def get_member_emails(df: pd.DataFrame) -> list:
    """Return list of active members' work email addresses"""
    
    if df.empty:
        return []
    
    return df["work_email"].str.lower().dropna().tolist()
 
# Query tables 
MEMBERS = query_table("SELECT * FROM member_directory WHERE active = TRUE")
MEMBER_EMAILS = get_member_emails(MEMBERS)


# --- Log activity --- 

def log_user(
    email_address: str,
    _engine: Engine = engine
):
    try:
        with _engine.connect() as conn:
            conn.execute(
                text("INSERT INTO member_log (login_email) VALUES (:email)"),
                {"email": email_address},
            )
            conn.commit()

    except Exception as e:
        st.error(f"Error logging activity: {e}")

