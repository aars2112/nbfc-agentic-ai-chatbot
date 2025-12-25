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
    c.drawString(50, y, "Personal Loan Sanction Letter")
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
st.caption("Full conversational AI for personal loans")

if st.button("🏠 Return to Home"):
    reset()

st.divider()

# ---------------- Session Init ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.stage = "start"

# ---------------- Display Chat ----------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your response here...")

def bot(text):
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.chat_message("assistant").write(text)

def user(text):
    st.session_state.messages.append({"role": "user", "content": text})
    st.chat_message("user").write(text)

# ---------------- Conversation Flow ----------------
if st.session_state.stage == "start":
    bot("👋 Hello! I’m your digital loan assistant. Let's start your personal loan journey.")
    bot("Please select a customer ID from the drop-down to begin.")
    st.session_state.stage = "select_customer"

elif st.session_state.stage == "select_customer":
    customer_id = st.selectbox("Select Customer ID", list(CUSTOMERS.keys()))
    if st.button("Confirm"):
        st.session_state.customer = CUSTOMERS[customer_id]
        bot(f"Hi {CUSTOMERS[customer_id]['name']} from {CUSTOMERS[customer_id]['city']}!")
        bot(f"Your credit score is {CUSTOMERS[customer_id]['credit_score']} and pre-approved limit is ₹{CUSTOMERS[customer_id]['preapproved_limit']}.")
        bot("How much loan amount do you want?")
        st.session_state.stage = "loan_amount"

elif st.session_state.stage == "loan_amount" and user_input:
    user(user_input)
    st.session_state.loan_amount = int(user_input)
    bot("Great! What tenure in months do you prefer? (12, 24, 36, 48, 60)")
    st.session_state.stage = "tenure"

elif st.session_state.stage == "tenure" and user_input:
    user(user_input)
    st.session_state.tenure = int(user_input)
    bot("What interest rate (%) are you comfortable with?")
    st.session_state.stage = "rate"

elif st.session_state.stage == "rate" and user_input:
    user(user_input)
    st.session_state.rate = float(user_input)

    bot("🔍 **Verification Agent:** KYC verified successfully!")
    bot("📊 **Underwriting Agent:** Checking eligibility...")

    c = st.session_state.customer
    emi = calculate_emi(st.session_state.loan_amount, st.session_state.rate, st.session_state.tenure)

    if c["credit_score"] < 700:
        bot("❌ Loan Rejected: Credit score below 700.")
        st.session_state.stage = "end"
    elif st.session_state.loan_amount <= c["preapproved_limit"]:
        st.session_state.approved = True
        bot(f"✅ Loan Approved instantly! EMI will be approx ₹{int(emi)}")
        st.session_state.stage = "sanction"
    elif st.session_state.loan_amount <= 2 * c["preapproved_limit"]:
        bot("📄 Salary slip required. Please upload your salary slip (PDF or image).")
        st.session_state.stage = "salary"
    else:
        bot("❌ Loan amount exceeds eligibility limit.")
        st.session_state.stage = "end"

elif st.session_state.stage == "salary":
    slip = st.file_uploader("Upload your salary slip", type=["pdf", "png", "jpg", "jpeg"])
    if slip:
        bot("✅ Salary slip uploaded successfully. Evaluating EMI eligibility...")
        c = st.session_state.customer
        emi = calculate_emi(st.session_state.loan_amount, st.session_state.rate, st.session_state.tenure)
        # assume slip salary is same as customer salary
        if emi <= 0.5 * c["salary"]:
            bot("✅ Salary verified. Loan Approved!")
            st.session_state.approved = True
            st.session_state.stage = "sanction"
        else:
            bot("❌ EMI exceeds 50% of salary. Loan Rejected.")
            st.session_state.stage = "end"

elif st.session_state.stage == "sanction":
    bot("📄 **Sanction Letter Generator:** Preparing your document...")
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
    bot("🎉 Congratulations! Your loan journey is complete.")
    st.session_state.stage = "end"

elif st.session_state.stage == "end":
    bot("Do you want to start a new loan journey?")
    if st.button("🔁 Start Again"):
        reset()
