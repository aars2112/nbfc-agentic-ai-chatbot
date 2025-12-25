import streamlit as st
from fpdf import FPDF
import math

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="NBFC Agentic AI Loan Assistant",
    page_icon="💳",
    layout="centered"
)

# -------------------------------
# Styling (Light & Dark Mode Safe)
# -------------------------------
st.markdown("""
<style>
.user-msg {
    background-color: rgba(0, 123, 255, 0.15);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}
.bot-msg {
    background-color: rgba(40, 167, 69, 0.15);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}
.card {
    padding: 15px;
    border-radius: 12px;
    background-color: rgba(0,0,0,0.05);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Synthetic Customer Data (5)
# -------------------------------
CUSTOMERS = {
    "Aarav Sharma": {
        "age": 29,
        "city": "Bengaluru",
        "credit_score": 780,
        "preapproved_limit": 500000
    },
    "Neha Gupta": {
        "age": 34,
        "city": "Delhi",
        "credit_score": 720,
        "preapproved_limit": 300000
    },
    "Rohit Mehta": {
        "age": 41,
        "city": "Mumbai",
        "credit_score": 680,
        "preapproved_limit": 400000
    },
    "Pooja Verma": {
        "age": 27,
        "city": "Pune",
        "credit_score": 750,
        "preapproved_limit": 250000
    },
    "Ankit Jain": {
        "age": 38,
        "city": "Jaipur",
        "credit_score": 705,
        "preapproved_limit": 350000
    }
}

# -------------------------------
# Helper Functions
# -------------------------------
def calculate_emi(principal, annual_rate, tenure_months):
    monthly_rate = annual_rate / (12 * 100)
    emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)

def generate_sanction_letter(name, amount, tenure, emi):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "NBFC Personal Loan Sanction Letter", ln=True)
    pdf.ln(10)

    pdf.multi_cell(0, 8, f"""
Dear {name},

We are pleased to inform you that your personal loan has been approved.

Loan Amount: ₹{amount}
Tenure: {tenure} months
Monthly EMI: ₹{emi}

This sanction is subject to standard NBFC terms and conditions.

Regards,
NBFC Digital Lending Team
""")

    file_name = f"{name.replace(' ', '_')}_Sanction_Letter.pdf"
    pdf.output(file_name)
    return file_name

# -------------------------------
# Session State Initialization
# -------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "home"

# -------------------------------
# Header
# -------------------------------
st.title("💳 NBFC Agentic AI Loan Assistant")
st.caption("Human-like conversational personal loan journey")

# -------------------------------
# Global Home Button
# -------------------------------
if st.button("🏠 Return to Home"):
    st.session_state.clear()
    st.session_state.stage = "home"
    st.experimental_rerun()

# -------------------------------
# HOME
# -------------------------------
if st.session_state.stage == "home":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Start a New Loan Journey")

    customer = st.selectbox("Select Customer (Synthetic Data)", list(CUSTOMERS.keys()))

    if st.button("Start Chat"):
        st.session_state.customer = customer
        st.session_state.stage = "sales"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# SALES AGENT
# -------------------------------
elif st.session_state.stage == "sales":
    st.markdown('<div class="bot-msg">Hello! I’m your digital loan assistant. Let’s get you the best personal loan.</div>', unsafe_allow_html=True)

    loan_amount = st.number_input("Desired Loan Amount (₹)", min_value=50000, step=50000)
    tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48, 60])
    interest_rate = 14.0

    if st.button("Proceed to Verification"):
        st.session_state.loan_amount = loan_amount
        st.session_state.tenure = tenure
        st.session_state.emi = calculate_emi(loan_amount, interest_rate, tenure)
        st.session_state.stage = "verification"

# -------------------------------
# VERIFICATION AGENT
# -------------------------------
elif st.session_state.stage == "verification":
    customer = CUSTOMERS[st.session_state.customer]

    st.markdown('<div class="bot-msg">Verifying your KYC details from our CRM system...</div>', unsafe_allow_html=True)

    st.success(f"""
KYC Verified ✅  
Name: {st.session_state.customer}  
Age: {customer['age']}  
City: {customer['city']}
""")

    if st.button("Proceed to Underwriting"):
        st.session_state.stage = "underwriting"

# -------------------------------
# UNDERWRITING AGENT
# -------------------------------
elif st.session_state.stage == "underwriting":
    customer = CUSTOMERS[st.session_state.customer]

    loan_amount = st.session_state.loan_amount
    emi = st.session_state.emi
    credit_score = customer["credit_score"]
    limit = customer["preapproved_limit"]

    st.markdown('<div class="bot-msg">Evaluating credit profile and eligibility...</div>', unsafe_allow_html=True)

    st.info(f"Credit Score: {credit_score}")
    st.info(f"Pre-approved Limit: ₹{limit}")
    st.info(f"Calculated EMI: ₹{emi}")

    # Rejection conditions
    if credit_score < 700 or loan_amount > 2 * limit:
        st.error("❌ Loan Rejected due to credit score or eligibility limits.")
        st.session_state.stage = "end"

    # Salary verification required
    elif loan_amount > limit:
        st.warning("Income verification required to proceed.")

        salary = st.selectbox(
            "Select your monthly salary (simulated income verification)",
            [30000, 50000, 80000, 120000],
            help="For demo purposes, income is verified digitally"
        )

        if st.button("Verify Income"):
            if emi <= 0.5 * salary:
                st.success("Income verified successfully ✅")
                st.session_state.salary = salary
                st.session_state.stage = "sanction"
            else:
                st.error("❌ Loan Rejected: EMI exceeds 50% of monthly salary.")
                st.session_state.stage = "end"

    # Instant approval
    else:
        st.success("Eligible for instant approval 🎉")
        st.session_state.stage = "sanction"

# -------------------------------
# SANCTION LETTER
# -------------------------------
elif st.session_state.stage == "sanction":
    file_path = generate_sanction_letter(
        st.session_state.customer,
        st.session_state.loan_amount,
        st.session_state.tenure,
        st.session_state.emi
    )

    st.success("🎉 Loan Approved!")
    st.download_button(
        "📄 Download Sanction Letter",
        open(file_path, "rb"),
        file_name=file_path
    )

    st.session_state.stage = "end"

# -------------------------------
# END
# -------------------------------
elif st.session_state.stage == "end":
    st.info("Thank you for using NBFC Agentic AI Loan Assistant.")
    st.caption("You may return to Home to start a new journey.")
