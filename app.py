import streamlit as st
import math
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="NBFC Agentic AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- Synthetic Customers ----------------
CUSTOMERS = {
    "CUST001": {
        "name": "Rahul Sharma",
        "age": 30,
        "city": "Bengaluru",
        "credit_score": 780,
        "preapproved_limit": 300000,
        "salary": 60000
    },
    "CUST002": {
        "name": "Ananya Verma",
        "age": 28,
        "city": "Delhi",
        "credit_score": 720,
        "preapproved_limit": 200000,
        "salary": 50000
    },
    "CUST003": {
        "name": "Karan Mehta",
        "age": 35,
        "city": "Mumbai",
        "credit_score": 690,
        "preapproved_limit": 250000,
        "salary": 70000
    },
    "CUST004": {
        "name": "Sneha Iyer",
        "age": 32,
        "city": "Chennai",
        "credit_score": 810,
        "preapproved_limit": 400000,
        "salary": 90000
    },
    "CUST005": {
        "name": "Amit Singh",
        "age": 40,
        "city": "Pune",
        "credit_score": 750,
        "preapproved_limit": 350000,
        "salary": 80000
    }
}

# ---------------- Helper Functions ----------------
def calculate_emi(P, R, N):
    r = R / (12 * 100)
    return P * r * (1 + r)**N / ((1 + r)**N - 1)

def generate_sanction_letter(customer, loan, tenure, rate):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    y = 800

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "🏦 Personal Loan Sanction Letter")
    y -= 40

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Customer: {customer['name']}")
    y -= 20
    c.drawString(50, y, f"Age: {customer['age']}")
    y -= 20
    c.drawString(50, y, f"City: {customer['city']}")
    y -= 20
    c.drawString(50, y, f"Credit Score: {customer['credit_score']}")
    y -= 30

    c.drawString(50, y, f"Loan Amount: ₹{loan}")
    y -= 20
    c.drawString(50, y, f"Tenure: {tenure} months")
    y -= 20
    c.drawString(50, y, f"Interest Rate: {rate}%")

    y -= 40
    c.drawString(50, y, "This loan has been approved based on internal credit assessment.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def reset():
    st.session_state.clear()
    st.rerun()

# ---------------- Styling ----------------
st.markdown("""
<style>
.chat-bubble {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.user {background-color: #d1f0c4;}
.agent {background-color: #cce0ff;}
[data-theme="dark"] .user {background-color: #0b3d0b;}
[data-theme="dark"] .agent {background-color: #05294a;}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.title("🤖 NBFC Agentic AI Chatbot")
st.caption("Human-like conversational AI for personal loans")

if st.button("🏠 Return to Home"):
    reset()

st.divider()

# ---------------- Session Init ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "select_customer"
if "customer" not in st.session_state:
    st.session_state.customer = None
if "loan_amount" not in st.session_state:
    st.session_state.loan_amount = 0
if "tenure" not in st.session_state:
    st.session_state.tenure = 0
if "rate" not in st.session_state:
    st.session_state.rate = 0
if "approved" not in st.session_state:
    st.session_state.approved = False

# ---------------- Conversation Flow ----------------
# Step 1: Select Customer
if st.session_state.stage == "select_customer":
    customer_id = st.selectbox("Select Customer ID 🆔", list(CUSTOMERS.keys()))
    if st.button("Confirm"):
        st.session_state.customer = CUSTOMERS[customer_id]
        st.session_state.stage = "loan_amount"

# Step 2: Display Customer Info and Ask Loan Amount
if st.session_state.stage == "loan_amount" and st.session_state.customer:
    c = st.session_state.customer
    st.markdown(f"👤 Customer: **{c['name']}**, Age: **{c['age']}**, City: **{c['city']}**")
    st.markdown(f"💳 Credit Score: **{c['credit_score']}**, Pre-approved Limit: **₹{c['preapproved_limit']}**")
    st.session_state.loan_amount = st.number_input("💰 Enter Loan Amount", min_value=10000, max_value=5*10**6, step=5000)
    if st.button("Next ➡"):
        st.session_state.stage = "tenure"

# Step 3: Select Tenure
if st.session_state.stage == "tenure":
    st.session_state.tenure = st.selectbox("⏳ Select Tenure (Months)", [12, 24, 36, 48, 60])
    if st.button("Next ➡"):
        st.session_state.stage = "rate"

# Step 4: Select Interest Rate
if st.session_state.stage == "rate":
    st.session_state.rate = st.slider("📈 Select Interest Rate (%)", 8.0, 15.0, 10.0, 0.5)
    if st.button("Next ➡"):
        st.session_state.stage = "verification"

# Step 5: Verification Agent
if st.session_state.stage == "verification":
    st.success("✅ **Verification Agent:** KYC details verified successfully!")
    if st.button("Next ➡"):
        st.session_state.stage = "underwriting"

# Step 6: Underwriting Agent
if st.session_state.stage == "underwriting":
    c = st.session_state.customer
    loan = st.session_state.loan_amount
    tenure = st.session_state.tenure
    rate = st.session_state.rate
    emi = calculate_emi(loan, rate, tenure)

    if c["credit_score"] < 700:
        st.error("❌ Loan Rejected: Credit score below 700.")
        st.session_state.stage = "end"
    elif loan <= c["preapproved_limit"]:
        st.success(f"✅ Loan Approved instantly! EMI: ₹{int(emi)}")
        st.session_state.approved = True
        st.session_state.stage = "sanction"
    elif loan <= 2 * c["preapproved_limit"]:
        st.info("📄 Salary slip required for approval. Please upload below.")
        st.session_state.stage = "salary"
    else:
        st.error("❌ Loan amount exceeds eligibility limit.")
        st.session_state.stage = "end"

# Step 7: Salary Slip Upload
if st.session_state.stage == "salary":
    slip = st.file_uploader("📄 Upload Salary Slip (PDF/Image)", type=["pdf", "jpg", "jpeg", "png"])
    if slip:
        c = st.session_state.customer
        emi = calculate_emi(st.session_state.loan_amount, st.session_state.rate, st.session_state.tenure)
        if emi <= 0.5 * c["salary"]:
            st.success("✅ Salary verified. Loan Approved!")
            st.session_state.approved = True
            if st.button("Next ➡"):
                st.session_state.stage = "sanction"
        else:
            st.error("❌ EMI exceeds 50% of salary. Loan Rejected.")
            st.session_state.stage = "end"

# Step 8: Sanction Letter
if st.session_state.stage == "sanction":
    pdf = generate_sanction_letter(
        st.session_state.customer,
        st.session_state.loan_amount,
        st.session_state.tenure,
        st.session_state.rate
    )
    st.download_button(
        "⬇ Download Sanction Letter",
        pdf,
        "sanction_letter.pdf",
        "application/pdf"
    )
    st.success("🎉 Congratulations! Your loan journey is complete.")
    if st.button("🔁 Start Again"):
        reset()

# Step 9: End
if st.session_state.stage == "end":
    st.info("You can start a new loan journey anytime.")
    if st.button("🔁 Start Again"):
        reset()
