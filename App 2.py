import streamlit as st
import os

TICKET_FOLDER = "tickets"
os.makedirs(TICKET_FOLDER, exist_ok=True)

# Streamlit page config
st.set_page_config(page_title="Shahaji Tours - Ticket Download", layout="centered")

# Base URL of your deployed Streamlit app
BASE_URL = "https://ticket-abkrvbzmpjwqva7jhqgdcw.streamlit.app/"  # Replace with your actual deployed URL

# --- Function to serve download button ---
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
    else:
        st.error("❌ Ticket not found.")

# --- Main ---
def main():
    st.title("📤 Shahaji Tours - Download Your Ticket")

    query_params = st.query_params

    if "ticket" in query_params:
        receipt_number = query_params["ticket"][0]
        st.markdown(f"### 🧾 Receipt No: **{receipt_number}**")
        st.markdown("👇 Click below to download your ticket:")
        show_download(receipt_number)

        share_url = f"{BASE_URL}?ticket={receipt_number}"
        st.markdown("📎 Share this link with your customer:")
        st.code(share_url)
    else:
        st.info("ℹ️ This page lets users download their tickets using a link.")
        st.write("To test manually, enter a receipt number below:")

        receipt_number = st.text_input("Receipt Number (e.g., 1001)")
        if st.button("Download Ticket"):
            show_download(receipt_number)

if __name__ == "__main__":
    main()
