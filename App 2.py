import streamlit as st
import os

# Configuration
st.set_page_config(page_title="Shahaji Tours - Ticket Download", layout="centered")
TICKET_FOLDER = "tickets_data"
os.makedirs(TICKET_FOLDER, exist_ok=True)
BASE_URL = "https://ticket-nymczx8uq5mejpxxfu9rnn.streamlit.app/"  # Replace with actual deployed app URL

# Download function
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

# Main app
def main():
    st.title("📤 Shahaji Tours - Download Your Ticket")
    query_params = st.query_params

    if "ticket" in query_params:
        receipt_number = query_params["ticket"][0]
        st.markdown(f"### 🧾 Receipt No: **{receipt_number}**")
        show_download(receipt_number)

        share_url = f"{BASE_URL}?ticket={receipt_number}"
        st.markdown("📎 Share this link with your customer:")
        st.code(share_url)
    else:
        st.info("ℹ️ Use a receipt number to download the ticket below.")
        receipt_number = st.text_input("Enter Receipt Number")
        if st.button("Download Ticket"):
            show_download(receipt_number)

if __name__ == "__main__":
    main()
