import streamlit as st
from datetime import date

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="ABC NBFC | AI Loan Assistant",
    page_icon="💳",
    layout="centered"
)

# ---------------------------------------------------
# Utility: Reset App
# ---------------------------------------------------
def reset_application():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.step = 1

# ---------------------------------------------------
# Sidebar Global Navigation
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## 🏦 ABC NBFC")
    st.caption("AI Loan Assistant")

    if st.button("🏠 Return to Home"):
        reset_application()
        st.rerun()

    st.markdown("---")
    st.caption("Demo MVP for Agentic AI Loan Processing")

# ---------------------------------------------------
# Detect Theme (Light / Dark)
# ---------------------------------------------------
theme = st.get_option("theme.base")

if theme == "dark":
    bg_main = "#0e1117"
    bubble_bg = "#1f2937"
    bubble_border = "#3b82f6"
    text_color = "#f9fafb"
    success_bg = "#064e3b"
    warning_bg = "#78350f"
    reject_bg = "#7f1d1d"
else:
    bg_main = "#f7f9fc"
    bubble_bg = "#e8f0fe"
    bubble_border = "#1a73e8"
    text_color = "#111827"
    success_bg = "#e6f4ea"
    warning_bg = "#fff4e5"
    reject_bg = "#fdecea"

# ---------------------------------------------------
# Dynamic CSS
# ---------------------------------------------------
st.markdown(f"""
<style>
.main {{
    background-color: {bg_main};
}}
.chat-bubble {{
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: {text_color};
}}
.assistant {{
    background-color: {bubble_bg};
    border-left: 4px solid {bubble_border};
}}
.success-box {{
    background-color: {success_bg};
    padding: 15px;
    border-radius: 10px;
}}
.warning-box {{
    background-color: {warning_bg};
    padding: 15px;
    border-radius: 10px;
}}
.reject-box {{
    background-color: {reject_bg};
    padding: 15px;
    border-radius: 10px;
}}
.metric-box {{
    background-color: rgba(255,255,255,0.08);
    padding: 12px;
    border-radius: 10px;
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Synthetic Customer Data
# ---------------------------------------------------
customers = {
    "C001": {"name": "Rahul Verma", "city": "Bengaluru", "salary": 65000, "credit_score": 760, "preapproved_limit": 300000},
    "C002": {"name": "Ananya Sharma", "city": "Delhi", "salary": 85000, "credit_score": 810, "preapproved_limit": 500000},
    "C003": {"name": "Mohit Gupta", "city": "Jaipur", "salary": 45000, "credit_score": 690, "preapproved_limit": 200000},
    "C004": {"name": "Sneha Iyer", "city": "Chennai", "salary": 72000, "credit_score": 735, "preapproved_limit": 250000},
    "C005": {"name": "Arjun Mehta", "city": "Mumbai", "salary": 120000, "credit_score": 840, "preapproved_limit": 700000}
}

# ---------------------------------------------------
# Underwriting Agent
# ---------------------------------------------------
def underwriting_agent(loan_amount, tenure, customer):
    emi = loan_amount / tenure

    if customer["credit_score"] < 700:
        return "REJECTED", "Credit score below 700", emi

    if loan_amount <= customer["preapproved_limit"]:
        return "APPROVED", "Approved within pre-approved limit", emi

    if loan_amount <= 2 * customer["preapproved_limit"]:
        if emi <= 0.5 * customer["salary"]:
            return "SALARY_SLIP", "Salary slip required for verification (simulated)", emi
        else:
            return "REJECTED", "EMI exceeds 50% of salary", emi

    return "REJECTED", "Requested amount too high", emi

# ---------------------------------------------------
# Sanction Letter Generator
# ---------------------------------------------------
def generate_sanction_letter(customer, loan_amount, tenure, emi):
    return f"""
PERSONAL LOAN SANCTION LETTER

Date: {date.today()}

Dear {customer['name']},

We are pleased to inform you that your Personal Loan has been approved.

Loan Amount: ₹{loan_amount}
Tenure: {tenure} months
Monthly EMI: ₹{round(emi, 2)}
City: {customer['city']}

Regards,
ABC NBFC Ltd.
"""

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.title("🤖 ABC NBFC AI Loan Assistant")
st.caption("Fast • Paperless • Human-like Loan Experience")

if "step" not in st.session_state:
    st.session_state.step = 1

# ---------------------------------------------------
# STEP 1: Welcome
# ---------------------------------------------------
if st.session_state.step == 1:
    st.markdown(f"""
    <div class="chat-bubble assistant">
        👋 Hi! I’m your digital loan assistant.<br><br>
        I’ll help you check eligibility and get a personal loan in minutes.
    </div>
    """, unsafe_allow_html=True)

    customer_id = st.selectbox("Select Customer Profile", customers.keys())

    if st.button("🚀 Start Loan Journey"):
        st.session_state.customer_id = customer_id
        st.session_state.step = 2
        st.reru
