import streamlit as st
import math
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="NBFC Agentic AI Loan Assistant",
    page_icon="💰",
    layout="centered"
)

# -------------------------------
# Synthetic Customer Data (5)
# -------------------------------
CUSTOMERS = {
    "Rahul Sharma": {
        "name": "Rahul Sharma",
        "age": 30,
        "city": "Bengaluru",
        "credit_score": 780,
        "preapproved_limit": 300000,
        "salary": 60000
    },
    "Ananya Verma": {
        "name": "Ananya Verma",
        "age": 28,
        "city": "Delhi",
        "credit_score": 720,
        "preapproved_limit": 200000,
        "salary": 50000
    },
    "Karan Mehta": {
        "name": "Karan Mehta",
        "age": 35,
        "city": "Mumbai",
        "credit_score": 690,
        "preapproved_limit": 250000,
        "salary": 70000
    },
    "Sneha Iyer": {
        "name": "Sneha Iyer",
        "age": 32,
        "city": "Chennai",
        "credit_score": 810,
        "preapproved_limit": 400000,
        "salary": 90000
    },
    "Amit Singh": {
        "name": "Amit Singh",
        "age": 40,
        "city": "Pune",
        "credit_score": 750,
        "preapproved_limit": 350000,
        "salary": 80000
    }
}

# -------------------------------
# Helper Functions
# -------------------------------
def calculate_emi(P, R, N):
    r = R / (12 * 100)
    emi = P * r * (1 + r)**N / ((1 + r)**N - 1)
    return emi

def generate_sanction_letter(customer, loan_amount, tenure, interest):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Personal Loan Sanction Letter")

    y -= 40
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Customer Name: {customer['name']}")
    y -= 20
    c.drawString(50, y, f"City: {customer['city']}")
    y -= 20
    c.drawString(50, y, f"Credit Score: {customer['credit_score']}")
    y -= 30

    c.drawString(50, y, f"Sanctioned Amount: ₹{loan_amount}")
    y -= 20
    c.drawString(50, y, f"Tenure: {tenure} months")
    y -= 20
    c.drawString(50, y, f"Interest Rate: {interest}%")
    y -= 30

    c.drawString(50, y, "This loan is sanctioned based on internal credit evaluation.")
    y -= 20
    c.drawString(50, y, "NBFC reserves the right to verify documents post disbursement.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# -------------------------------
# UI Styling (Light & Dark Safe)
# -------------------------------
st.markdown("""
<style>
.chat-bubble {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    background-color: rgba(0, 123, 255, 0.1);
    color: inherit;
}
.agent {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.title("🤖 NBFC Agentic AI Loan Assistant")
st.caption("Human-like conversational loan sales powered by Agentic AI")

if st.button("🏠 Return to Home"):
    reset_app()

st.divider()

# -------------------------------
# Step 1: Customer Selection
# -------------------------------
st.subheader("👤 Select Customer Profile (Synthetic Data)")
customer_name = st.selectbox("Choose a customer", list(CUSTOMERS.keys()))
customer = CUSTOMERS[customer_name]

st.info(
    f"**{customer['name']}**, Age {customer['age']} | "
    f"{customer['city']} | Credit Score: {customer['credit_score']}"
)

# -------------------------------
# Step 2: Sales Agent
# -------------------------------
st.subheader("💬 Sales Agent Conversation")

loan_amount = st.number_input(
    "Desired Loan Amount (₹)",
    min_value=50000,
    step=10000
)

tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48, 60])
interest = st.slider("Interest Rate (%)", 10.0, 20.0, 13.5)

if st.button("➡ Proceed to Verification"):
    st.session_state["verified"] = True

# -------------------------------
# Step 3: Verification Agent
# -------------------------------
if st.session_state.get("verified"):
    st.subheader("✅ Verification Agent")
    st.success("KYC verified successfully from CRM database")

# -------------------------------
# Step 4: Underwriting Agent
# -------------------------------
if st.session_state.get("verified"):
    st.subheader("📊 Underwriting Agent")

    st.write(f"**Pre-approved Limit:** ₹{customer['preapproved_limit']}")
    emi = calculate_emi(loan_amount, interest, tenure)
    st.write(f"**Calculated EMI:** ₹{int(emi)}")
    st.write(f"**Customer Salary:** ₹{customer['salary']}")

    decision = None

    if customer["credit_score"] < 700:
        decision = "reject"
        st.error("❌ Loan Rejected: Credit score below 700")

    elif loan_amount <= customer["preapproved_limit"]:
        decision = "approve"
        st.success("✅ Loan Approved Instantly")

    elif loan_amount <= 2 * customer["preapproved_limit"]:
        st.warning("📄 Salary Slip Required")
        slip_option = st.selectbox(
            "Select Salary Slip (Dummy)",
            ["Salary Slip – ₹40,000", "Salary Slip – ₹60,000", "Salary Slip – ₹90,000"]
        )

        slip_salary = int(slip_option.split("₹")[1].replace(",", ""))
        if emi <= 0.5 * slip_salary:
            decision = "approve"
            st.success("✅ Loan Approved after salary validation")
        else:
            decision = "reject"
            st.error("❌ EMI exceeds 50% of salary")

    else:
        decision = "reject"
        st.error("❌ Loan amount exceeds eligibility limit")

# -------------------------------
# Step 5: Sanction Letter
# -------------------------------
if st.session_state.get("verified") and decision == "approve":
    st.subheader("📄 Sanction Letter Generator")

    pdf = generate_sanction_letter(customer, loan_amount, tenure, interest)

    st.download_button(
        "⬇ Download Sanction Letter",
        pdf,
        file_name="loan_sanction_letter.pdf",
        mime="application/pdf"
    )

    st.success("🎉 Loan process completed successfully")

    st.button("🔁 Start New Customer Journey", on_click=reset_app)





