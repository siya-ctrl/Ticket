import streamlit as st
from fpdf import FPDF
import datetime
import tempfile
import base64
import urllib.parse
import os

# Streamlit page config must be first command after imports
st.set_page_config(page_title="Shahaji Tours - Ticket Generator", layout="centered")

# Initialize receipt no in session_state for auto-increment
if "receipt_no" not in st.session_state:
    st.session_state.receipt_no = 1000  # Starting receipt number

# PDF generation class
class ShahajiPDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.ln(10)

    def footer(self):
        pass

st.title("🚌 Shahaji Tours and Travels Karad - Ticket Generator")

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
        advance_amount = st.number_input("Advance Amount (Rs.)", min_value=0, max_value=total_amount if total_amount > 0 else None, step=1)

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
    balance_amount = total_amount - advance_amount

    pdf = ShahajiPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    margin_x = 10
    margin_y = 20
    box_width = 190
    box_height = 200
    pdf.rect(margin_x, margin_y, box_width, box_height)

    # Receipt No and Customer Name right aligned top-right inside box
    pdf.set_xy(margin_x + box_width - 70, margin_y + 5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(70, 10, f"Receipt No.: {st.session_state.receipt_no}", align='R', ln=True)

    # Title centered below top margin in bold
    pdf.set_xy(margin_x, margin_y)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(box_width - 10, 10, "Shahaji Tours and Travels Karad", ln=True, align='C')

    # Ticket Details title bold
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Ticket Details:", ln=True)

    # Ticket details with bold labels and normal values
    def write_bold_label_value(label, value):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 8, f"{label}:", ln=False)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, str(value), ln=True)

    write_bold_label_value("Customer Name", customer_name)
    write_bold_label_value("Bus Name", bus_name)
    write_bold_label_value("Bus Number", bus_number)
    write_bold_label_value("From", from_location)
    write_bold_label_value("To", to_location)
    write_bold_label_value("Seat Type", seat_type)
    write_bold_label_value("No. of Seats", no_of_seats)
    write_bold_label_value("Seat Numbers", seat_numbers)
    write_bold_label_value("Boarding Point", boarding_point)
    write_bold_label_value("Reporting Time", reporting_time)
    write_bold_label_value("Journey Date", journey_date.strftime('%d/%m/%Y'))
    write_bold_label_value("Issue Date", issue_date.strftime('%d/%m/%Y'))

    pdf.ln(5)

    # Payment Details title bold
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Payment Details:", ln=True)

    write_bold_label_value("Total Amount", f"Rs. {total_amount}")
    write_bold_label_value("Advance", f"Rs. {advance_amount}")
    write_bold_label_value("Balance", f"Rs. {balance_amount}")

    pdf.set_y(margin_y + box_height + 5)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, "Cancellation Rules as per bus operator's policy", ln=True)
    pdf.cell(0, 10, "Signature", ln=True)
    pdf.cell(0, 10, "For Shahaji Tours and Travels Karad", ln=True)
    pdf.cell(0, 10, "Booked By : Shahaji Tours and Travels Karad", ln=True)
    pdf.multi_cell(0, 10, "Address: Shop No 5, Jagdale Complex, Opp.Hotel Pankaj, P.B.Road, Karad. Mob:8055323258")

    # Save PDF to temp file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    tmp_file.close()  # Close the file handle to release it

    # Read PDF bytes
    with open(tmp_file.name, "rb") as file:
        pdf_bytes = file.read()

    # Delete temp file after reading
    os.unlink(tmp_file.name)

    # Prepare download link for PDF
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    download_filename = f"ticket_{st.session_state.receipt_no}.pdf"
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{download_filename}">📥 Download Ticket PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

    # WhatsApp share message (text only, no direct PDF attachment possible)
    message = (
        f"Hello {customer_name}, your ticket is ready.\n"
        f"From: {from_location} To: {to_location}\n"
        f"Date: {journey_date.strftime('%d/%m/%Y')} | Seats: {seat_numbers}\n"
        f"Balance to pay: Rs. {balance_amount}\n\n"
        f"Please download your ticket from the link sent."
    )
    wa_url = f"https://wa.me/?text={urllib.parse.quote(message)}"
    st.markdown(f"[📤 Share Ticket Info via WhatsApp]({wa_url})", unsafe_allow_html=True)

    st.success("✅ Ticket generated successfully!")

    # Increment receipt number only AFTER successful ticket generation
    st.session_state.receipt_no += 1


