import streamlit as st
from fpdf import FPDF
import datetime
import urllib.parse
import os

# Config
st.set_page_config(page_title="Shahaji Tours - Ticket System", layout="centered")
TICKET_FOLDER = "tickets_data"
os.makedirs(TICKET_FOLDER, exist_ok=True)
BASE_URL = "https://ticket-ncdd5jogjjgcpbwxuoctuf.streamlit.app/"  # Replace this!

# Receipt number file handling
def get_next_receipt_no():
    file_path = "receipt_number.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            current = int(f.read())
    else:
        current = 1000
    next_receipt = current + 1
    with open(file_path, "w") as f:
        f.write(str(next_receipt))
    return current

# PDF Generator
class ShahajiPDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.ln(10)
    def footer(self):
        pass

# Serve PDF Download
def show_download(receipt_number):
    file_path = os.path.join(TICKET_FOLDER, f"ticket_{receipt_number}.pdf")
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        st.download_button(
            label=f"📥 Download Ticket #{receipt_number}",
            data=data,
            file_name=f"ticket_{receipt_number}.pdf",
            mime="application/pdf",
        )
        st.success("✅ Ticket ready to download.")
    else:
        st.error("❌ Ticket not found.")

# Main logic
query_params = st.query_params
if "ticket" in query_params:
    receipt_number = query_params["ticket"][0]
    st.title("📤 Shahaji Tours - Download Your Ticket")
    st.markdown(f"### 🧾 Receipt No: **{receipt_number}**")
    show_download(receipt_number)
    st.stop()  # Skip form if downloading

# --- Ticket Generation Form ---
st.title("🚌 Shahaji Tours and Travels Karad - Ticket Generator")

if "receipt_no" not in st.session_state:
    st.session_state.receipt_no = get_next_receipt_no()

with st.form("ticket_form"):
    st.subheader("Enter Ticket Details")
    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Customer Name")
        from_location = st.text_input("From")
        seat_type = st.selectbox("Seat Type", ["SEATER", "SLEEPER"])
        no_of_seats = st.number_input("No. of Seats", min_value=1, max_value=10, step=1)
        seat_numbers = st.text_input("Seat Numbers (comma-separated)")
        reporting_time = st.text_input("Reporting Time")
        total_amount = st.number_input("Total Amount (Rs.)", min_value=0, step=1)
        advance_amount = st.number_input("Advance Amount (Rs.)", min_value=0, max_value=total_amount, step=1)

    with col2:
        to_location = st.text_input("To")
        boarding_point = st.text_input("Boarding Point", value="Shahaji Tours and Travels Karad")
        journey_date = st.date_input("Date of Journey", datetime.date.today())
        issue_date = st.date_input("Date of Issue", datetime.date.today())
        bus_name = st.text_input("Bus Name")
        bus_number = st.text_input("Bus Number")

    st.write(f"Receipt No.: **{st.session_state.receipt_no}**")
    submitted = st.form_submit_button("Generate Ticket")

if submitted:
    receipt_no = st.session_state.receipt_no
    balance_amount = total_amount - advance_amount

    pdf = ShahajiPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    margin_x, margin_y = 10, 20
    box_width, box_height = 190, 200
    pdf.rect(margin_x, margin_y, box_width, box_height)

    pdf.set_xy(margin_x + box_width - 70, margin_y + 5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(70, 10, f"Receipt No.: {receipt_no}", align='R', ln=True)
    pdf.set_xy(margin_x, margin_y)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(box_width - 10, 10, "Shahaji Tours and Travels Karad", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Ticket Details:", ln=True)

    def write_bold(label, value):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 8, f"{label}:", ln=False)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, str(value), ln=True)

    write_bold("Customer Name", customer_name)
    write_bold("Bus Name", bus_name)
    write_bold("Bus Number", bus_number)
    write_bold("From", from_location)
    write_bold("To", to_location)
    write_bold("Seat Type", seat_type)
    write_bold("No. of Seats", no_of_seats)
    write_bold("Seat Numbers", seat_numbers)
    write_bold("Boarding Point", boarding_point)
    write_bold("Reporting Time", reporting_time)
    write_bold("Journey Date", journey_date.strftime('%d/%m/%Y'))
    write_bold("Issue Date", issue_date.strftime('%d/%m/%Y'))
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Payment Details:", ln=True)
    write_bold("Total Amount", f"Rs. {total_amount}")
    write_bold("Advance", f"Rs. {advance_amount}")
    write_bold("Balance", f"Rs. {balance_amount}")

    pdf.set_y(margin_y + box_height + 5)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 10,
        "Cancellation Rules as per bus operator's policy\n"
        "Signature\n"
        "For Shahaji Tours and Travels Karad\n"
        "Booked By : Shahaji Tours and Travels Karad\n"
        "Address: Shop No 5, Jagdale Complex, Opp.Hotel Pankaj, P.B.Road, Karad. Mob:8055323258"
    )

    filepath = os.path.join(TICKET_FOLDER, f"ticket_{receipt_no}.pdf")
    pdf.output(filepath)

    with open(filepath, "rb") as f:
        st.download_button("📥 Download Ticket PDF", data=f.read(), file_name=f"ticket_{receipt_no}.pdf", mime="application/pdf")

    # WhatsApp link
    ticket_url = f"{BASE_URL}?ticket={receipt_no}"
    message = (
        f"Hello {customer_name}, your ticket is ready.\n"
        f"From: {from_location} To: {to_location}\n"
        f"Date: {journey_date.strftime('%d/%m/%Y')} | Seats: {seat_numbers}\n"
        f"Balance to pay: Rs. {balance_amount}\n\n"
        f"Download your ticket: {ticket_url}"
    )
    wa_url = f"https://wa.me/?text={urllib.parse.quote(message)}"
    st.markdown(f"[📤 Share Ticket Info via WhatsApp]({wa_url})", unsafe_allow_html=True)
    st.success("✅ Ticket generated successfully!")

    st.session_state.receipt_no = get_next_receipt_no()
