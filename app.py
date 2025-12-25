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
    st.experimental_rerun()

# ---------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## 🏦 ABC NBFC")
    st.caption("AI Loan Assistant")

    if st.button("🏠 Return to Home"):
        reset_application()

    st.markdown("---")
    st.caption("Demo MVP for Agentic AI Loan Processing")

# ---------------------------------------------------
# Detect Theme
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
            return "SALARY_SLIP", "Salary slip verification simulated ✅", emi
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
Monthly EMI: ₹{round(emi,2)}
City: {customer['city']}

Regards,
ABC NBFC Ltd.
"""

# ---------------------------------------------------
# Helper functions for state updates
# ---------------------------------------------------
def start_loan_journey(selected_customer):
    st.session_state.customer_id = selected_customer
    st.session_state.step = 2
    st.experimental_rerun()

def proceed_to_underwriting(loan_amount, tenure):
    st.session_state.loan_amount = loan_amount
    st.session_state.tenure = tenure
    st.session_state.step = 3
    st.experimental_rerun()

def continue_after_underwriting():
    st.experimental_rerun()

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
    st.button("🚀 Start Loan Journey", on_click=lambda: start_loan_journey(customer_id))

# ---------------------------------------------------
# STEP 2: Sales Agent
# ---------------------------------------------------
elif st.session_state.step == 2:
    customer = customers[st.session_state.customer_id]

    st.markdown(f"""
    <div class="chat-bubble assistant">
        Hi <b>{customer['name']}</b> from {customer['city']} 😊<br><br>
        Tell me how much loan you need and your preferred tenure.
    </div>
    """, unsafe_allow_html=True)

    loan_amount = st.number_input("💰 Loan Amount (₹)", min_value=50000, step=10000)
    tenure = st.selectbox("📆 Loan Tenure (months)", [12, 24, 36, 48])
    st.button("🔍 Check Eligibility", on_click=lambda: proceed_to_underwriting(loan_amount, tenure))

# ---------------------------------------------------
# STEP 3: Underwriting
# ---------------------------------------------------
elif st.session_state.step == 3:
    customer = customers[st.session_state.customer_id]

    st.markdown("""<div class="chat-bubble assistant">🔍 Verifying your profile and checking eligibility...</div>""", unsafe_allow_html=True)

    status, reason, emi = underwriting_agent(
        st.session_state.loan_amount,
        st.session_state.tenure,
        customer
    )

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metric-box'><b>Credit Score</b><br>{customer['credit_score']}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-box'><b>Pre-approved</b><br>₹{customer['preapproved_limit']}</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-box'><b>EMI</b><br>₹{round(emi,2)}</div>", unsafe_allow_html=True)

    if status == "APPROVED":
        st.markdown(f"<div class='success-box'>✅ Loan Approved Instantly!</div>", unsafe_allow_html=True)
        st.session_state.emi = emi
        st.session_state.step = 5
        st.button("Continue ➡️", on_click=continue_after_underwriting)

    elif status == "SALARY_SLIP":
        st.markdown(f"<div class='warning-box'>📄 {reason}</div>", unsafe_allow_html=True)
        st.markdown("Simulating salary slip verification automatically ✅")
        st.session_state.emi = emi
        st.session_state.step = 5
        st.button("Continue ➡️", on_click=continue_after_underwriting)

    else:
        st.markdown(f"<div class='reject-box'>❌ Loan Rejected: {reason}</div>", unsafe_allow_html=True)
        st.session_state.step = 4
        st.button("Continue ➡️", on_click=continue_after_underwriting)

# ---------------------------------------------------
# STEP 4: Rejection
# ---------------------------------------------------
elif st.session_state.step == 4:
    st.markdown("""<div class="chat-bubble assistant">Thank you for your interest. Unfortunately, we can’t proceed right now.</div>""", unsafe_allow_html=True)

# ---------------------------------------------------
# STEP 5: Sanction Letter
# ---------------------------------------------------
elif st.session_state.step == 5:
    customer = customers[st.session_state.customer_id]

    st.markdown("""<div class="chat-bubble assistant">🎉 Congratulations! Your loan has been approved. Please download your sanction letter below.</div>""", unsafe_allow_html=True)

    letter = generate_sanction_letter(
        customer,
        st.session_state.loan_amount,
        st.session_state.tenure,
        st.session_state.emi
    )

    st.download_button("📄 Download Sanction Letter", data=letter, file_name="sanction_letter.txt")
