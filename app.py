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
    "Rahul Sharma": {
        "name": "Rahul Sharma",
        "city": "Bengaluru",
        "credit_score": 780,
        "preapproved_limit": 300000,
        "salary": 60000
    },
    "Ananya Verma": {
        "name": "Ananya Verma",
        "city": "Delhi",
        "credit_score": 720,
        "preapproved_limit": 200000,
        "salary": 50000
    },
    "Karan Mehta": {
        "name": "Karan Mehta",
        "city": "Mumbai",
        "credit_score": 690,
        "preapproved_limit": 250000,
        "salary": 70000
    },
    "Sneha Iyer": {
        "name": "Sneha Iyer",
        "city": "Chennai",
        "credit_score": 810,
        "preapproved_limit": 400000,
        "salary": 90000
    },
    "Amit Singh": {
        "name": "Amit Singh",
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

# ---------------- UI Header ----------------
st.title("🤖 NBFC Agentic AI Loan Assistant")
st.caption("Conversational AI-powered personal loan sales")

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

# ---------------- Conversation Engine ----------------
user_input = st.chat_input("Type your response...")

def bot(text):
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.chat_message("assistant").write(text)

def user(text):
    st.session_state.messages.append({"role": "user", "content": text})
    st.chat_message("user").write(text)

# ---------------- Chat Flow ----------------
if st.session_state.stage == "start":
    bot("👋 Hello! I’m your digital loan assistant. Let’s get you a personal loan.")
    bot("Please select a customer profile to continue.")
    st.session_state.stage = "select_customer"

elif st.session_state.stage == "select_customer":
    name = st.selectbox("Select customer", list(CUSTOMERS.keys()))
    if st.button("Confirm"):
        st.session_state.customer = CUSTOMERS[name]
        bot(f"Great! Hi {name} 👋")
        bot("How much loan amount are you looking for?")
        st.session_state.stage = "loan_amount"

elif st.session_state.stage == "loan_amount" and user_input:
    user(user_input)
    st.session_state.loan_amount = int(user_input)
    bot("Got it. What tenure do you prefer? (in months)")
    st.session_state.stage = "tenure"

elif st.session_state.stage == "tenure" and user_input:
    user(user_input)
    st.session_state.tenure = int(user_input)
    bot("What interest rate are you comfortable with?")
    st.session_state.stage = "rate"

elif st.session_state.stage == "rate" and user_input:
    user(user_input)
    st.session_state.rate = float(user_input)

    bot("🔍 **Verification Agent:** KYC verified successfully.")
    bot("📊 **Underwriting Agent:** Evaluating eligibility...")

    c = st.session_state.customer
    emi = calculate_emi(st.session_state.loan_amount, st.session_state.rate, st.session_state.tenure)

    if c["credit_score"] < 700:
        bot("❌ Loan rejected due to low credit score.")
        st.session_state.stage = "end"

    elif st.session_state.loan_amount <= c["preapproved_limit"]:
        st.session_state.approved = True
        bot("✅ Loan approved instantly!")
        st.session_state.stage = "sanction"

    elif st.session_state.loan_amount <= 2 * c["preapproved_limit"]:
        bot("📄 Salary slip required. Please select one.")
        st.session_state.stage = "salary"

    else:
        bot("❌ Loan amount exceeds eligibility.")
        st.session_state.stage = "end"

elif st.session_state.stage == "salary":
    slip = st.selectbox(
        "Select dummy salary slip",
        ["₹40,000", "₹60,000", "₹90,000"]
    )
    if st.button("Submit Salary Slip"):
        slip_salary = int(slip.replace("₹", "").replace(",", ""))
        emi = calculate_emi(st.session_state.loan_amount, st.session_state.rate, st.session_state.tenure)

        if emi <= 0.5 * slip_salary:
            bot("✅ Salary verified. Loan approved!")
            st.session_state.approved = True
            st.session_state.stage = "sanction"
        else:
            bot("❌ EMI exceeds 50% of salary. Loan rejected.")
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
    bot("Would you like to start a new loan journey?")
    if st.button("🔁 Start Again"):
        reset()



