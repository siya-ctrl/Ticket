import streamlit as st
import os
from fpdf import FPDF

TICKET_FOLDER = "tickets"
os.makedirs(TICKET_FOLDER, exist_ok=True)

def generate_ticket(receipt_number):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Ticket Receipt Number: {receipt_number}", ln=True)
    file_path = os.path.join(TICKET_FOLDER, f"ticket_{receipt_number}.pdf")
    pdf.output(file_path)
    return file_path

def show_download(receipt_number):
    file_path = os.path.join(TICKET_FOLDER, f"ticket_{receipt_number}.pdf")
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        st.download_button(
            label=f"Download Ticket #{receipt_number}",
            data=data,
            file_name=f"ticket_{receipt_number}.pdf",
            mime="application/pdf",
        )
    else:
        st.error("Ticket not found.")

def main():
    st.title("Ticket Generator")

    # Check if ticket receipt_number is in query params
    query_params = st.experimental_get_query_params()
    if "ticket" in query_params:
        receipt_number = query_params["ticket"][0]
        st.write(f"Download your ticket: #{receipt_number}")
        show_download(receipt_number)
        st.write("Share this link with your customer:")
        url = st.get_url() + f"?ticket={receipt_number}"
        st.text(url)
        return

    # Normal ticket generation page
    receipt_number = st.text_input("Enter Receipt Number", value="1001")
    if st.button("Generate Ticket PDF"):
        file_path = generate_ticket(receipt_number)
        st.success(f"Ticket #{receipt_number} generated!")
        st.write("You can download the ticket here:")
        show_download(receipt_number)
        url = st.get_url() + f"?ticket={receipt_number}"
        st.write("Or share this link with your customer to download the ticket:")
        st.text(url)

if __name__ == "__main__":
    main()
