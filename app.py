
import streamlit as st
import qrcode
from PIL import Image
import io
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

# Configure the Streamlit app
st.set_page_config(page_title="QR Code Tool by samad", page_icon="🔳", layout="wide")

# Initialize session state for QR scanning
if "qr_code_data" not in st.session_state:
    st.session_state.qr_code_data = None  # Store last detected QR code

# Class for real-time QR code scanning using webcam with OpenCV
class QRCodeScanner(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")  # Convert frame to NumPy array
        detector = cv2.QRCodeDetector()         # Initialize OpenCV's QR code detector
        data, points, _ = detector.detectAndDecode(img)

        if data:
            st.session_state.qr_code_data = data  # Store result in session state
        
        return img  # Return the frame for display

# Function to generate a QR code from given text or URL
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')  # Create QR code image
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)  # Reset file pointer
    
    return img_bytes  # Return the byte stream

# Function to decode QR codes from an uploaded image using OpenCV
def decode_qr_code(uploaded_image):
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(image)
    return [data] if data else []

# App title
st.title("🔳 QR Code Encoder & Decoder")
st.markdown("### A simple tool to generate, decode, and scan QR codes in real-time.")

# Layout for Generate & Decode
col1, col2 = st.columns(2)

with col1:
    st.subheader("Generate QR Code")
    input_text = st.text_input("Enter text or URL to generate QR Code")
    if st.button("Generate QR Code", use_container_width=True):
        if input_text:
            qr_image = generate_qr_code(input_text)
            st.image(qr_image, caption="Generated QR Code")  # Display QR Code
            st.download_button("Download QR Code", qr_image.getvalue(), "qrcode.png", "image/png")
        else:
            st.error("Please enter text or a URL")

with col2:
    st.subheader("Decode QR Code")
    uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"], help="Upload an image containing a QR code")
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded QR Code", use_column_width=True)
        decoded_texts = decode_qr_code(uploaded_file)
        if decoded_texts:
            st.success("Decoded Text:")
            for text in decoded_texts:
                st.code(text, language='plaintext')
        else:
            st.error("No QR code detected or could not decode.")

# Section for real-time QR code scanning
st.subheader("📷 Scan QR Code using Camera")
st.write("Use your webcam to scan QR codes in real-time.")

# Run the real-time QR scanner
webrtc_streamer(key="qr_scanner", video_transformer_factory=QRCodeScanner)

# Display scanned QR code result
if st.session_state.qr_code_data:
    st.success(f"**Decoded QR Code:** {st.session_state.qr_code_data}")



# import streamlit as st
# import qrcode
# from PIL import Image
# import io
# import cv2
# import numpy as np
# from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
# import av

# # Configure the Streamlit app
# st.set_page_config(page_title="QR Code Tool", page_icon="🔳", layout="wide")

# # Global variable to store detected QR code result
# scanned_qr_result = st.empty()

# # Class for real-time QR code scanning using webcam with OpenCV
# class QRCodeScanner(VideoTransformerBase):
#     def __init__(self):
#         self.qr_code_data = None  # Store the last detected QR code

#     def transform(self, frame):
#         img = frame.to_ndarray(format="bgr24")  # Convert frame to NumPy array
#         detector = cv2.QRCodeDetector()         # Initialize OpenCV's QR code detector
#         data, points, _ = detector.detectAndDecode(img)

#         if data:
#             self.qr_code_data = data  # Store detected QR code data
        
#         return img  # Return the frame for display

# # Function to generate a QR code from given text or URL
# def generate_qr_code(data):
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)
#     img = qr.make_image(fill='black', back_color='white')  # Create QR code image
    
#     img_bytes = io.BytesIO()
#     img.save(img_bytes, format="PNG")
#     img_bytes.seek(0)  # Reset file pointer
    
#     return img_bytes  # Return the byte stream

# # Function to decode QR codes from an uploaded image using OpenCV
# def decode_qr_code(uploaded_image):
#     file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
#     image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
#     detector = cv2.QRCodeDetector()
#     data, points, _ = detector.detectAndDecode(image)
#     return [data] if data else []

# # App title
# st.title("🔳 QR Code Encoder & Decoder")
# st.markdown("### A simple tool to generate, decode, and scan QR codes in real-time.")

# # Layout for Generate & Decode
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("Generate QR Code")
#     input_text = st.text_input("Enter text or URL to generate QR Code")
#     if st.button("Generate QR Code", use_container_width=True):
#         if input_text:
#             qr_image = generate_qr_code(input_text)
#             st.image(qr_image, caption="Generated QR Code")  # Display QR Code
#             st.download_button("Download QR Code", qr_image.getvalue(), "qrcode.png", "image/png")
#         else:
#             st.error("Please enter text or a URL")

# with col2:
#     st.subheader("Decode QR Code")
#     uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"], help="Upload an image containing a QR code")
#     if uploaded_file:
#         st.image(uploaded_file, caption="Uploaded QR Code", use_column_width=True)
#         decoded_texts = decode_qr_code(uploaded_file)
#         if decoded_texts:
#             st.success("Decoded Text:")
#             for text in decoded_texts:
#                 st.code(text, language='plaintext')
#         else:
#             st.error("No QR code detected or could not decode.")

# # Section for real-time QR code scanning
# st.subheader("📷 Scan QR Code using Camera")
# st.write("Use your webcam to scan QR codes in real-time.")

# # Run the real-time QR scanner
# qr_scanner = webrtc_streamer(
#     key="qr_scanner",
#     video_transformer_factory=QRCodeScanner,
#     async_transform=True,
# )

# # Display scanned QR code result
# if qr_scanner and qr_scanner.video_transformer:
#     detected_qr = qr_scanner.video_transformer.qr_code_data
#     if detected_qr:
#         scanned_qr_result.success(f"**Decoded QR Code:** {detected_qr}")

# # Display features
# st.markdown("---")
# st.markdown("### Features:")
# st.markdown("✅ Generate QR codes from text or URLs")
# st.markdown("✅ Decode QR codes from uploaded images")
# st.markdown("✅ Scan QR codes in real-time using your webcam")
# st.markdown("✅ Download generated QR codes")



# # import streamlit as st
# # import qrcode
# # from PIL import Image
# # import io
# # import cv2
# # import numpy as np
# # from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# # # Configure the Streamlit app with title, icon, and wide layout
# # st.set_page_config(page_title="QR Code Tool", page_icon="🔳", layout="wide")

# # # Class for real-time QR code scanning using webcam with OpenCV
# # class QRCodeScanner(VideoTransformerBase):
# #     def transform(self, frame):
# #         img = frame.to_ndarray(format="bgr24")  # Convert frame to NumPy array
# #         detector = cv2.QRCodeDetector()         # Initialize OpenCV's QR code detector
# #         data, points, _ = detector.detectAndDecode(img)
# #         if data:
# #             st.success(f"Decoded Text: {data}")  # Display decoded text if found
# #         return img  # Return the frame for display

# # # Function to generate a QR code from given text or URL
# # def generate_qr_code(data):
# #     qr = qrcode.QRCode(
# #         version=1,
# #         error_correction=qrcode.constants.ERROR_CORRECT_L,
# #         box_size=10,
# #         border=4,
# #     )
# #     qr.add_data(data)
# #     qr.make(fit=True)
# #     img = qr.make_image(fill='black', back_color='white')  # Create QR code image
    
# #     # Convert PIL image to bytes
# #     img_bytes = io.BytesIO()
# #     img.save(img_bytes, format="PNG")
# #     img_bytes.seek(0)  # Reset file pointer
    
# #     return img_bytes  # Return the byte stream

# # # Function to decode QR codes from an uploaded image using OpenCV
# # def decode_qr_code(uploaded_image):
# #     # Convert uploaded file to an OpenCV image
# #     file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
# #     image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
# #     detector = cv2.QRCodeDetector()  # Initialize detector
# #     data, points, _ = detector.detectAndDecode(image)
# #     return [data] if data else []  # Return result as a list for consistency

# # # App title and description
# # st.title("🔳 QR Code Encoder & Decoder")
# # st.markdown("### A simple tool to generate, decode, and scan QR codes in real-time.")

# # # Layout with two columns for generating and decoding QR codes
# # col1, col2 = st.columns(2)

# # with col1:
# #     st.subheader("Generate QR Code")
# #     input_text = st.text_input("Enter text or URL to generate QR Code")
# #     if st.button("Generate QR Code", use_container_width=True):
# #         if input_text:
# #             qr_image = generate_qr_code(input_text)
# #             st.image(qr_image, caption="Generated QR Code")  # Display QR Code
# #             st.download_button("Download QR Code", qr_image.getvalue(), "qrcode.png", "image/png")
# #         else:
# #             st.error("Please enter text or a URL")

# # with col2:
# #     st.subheader("Decode QR Code")
# #     uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"], help="Upload an image containing a QR code")
# #     if uploaded_file:
# #         st.image(uploaded_file, caption="Uploaded QR Code", use_column_width=True)
# #         decoded_texts = decode_qr_code(uploaded_file)
# #         if decoded_texts:
# #             st.success("Decoded Text:")
# #             for text in decoded_texts:
# #                 st.code(text, language='plaintext')
# #         else:
# #             st.error("No QR code detected or could not decode.")

# # # Section for real-time QR code scanning using webcam
# # st.subheader("📷 Scan QR Code using Camera")
# # st.write("Use your webcam to scan QR codes in real-time.")
# # webrtc_streamer(key="qr_scanner", video_transformer_factory=QRCodeScanner)

# # # Display features of the tool
# # st.markdown("---")
# # st.markdown("### Features:")
# # st.markdown("✅ Generate QR codes from text or URLs")
# # st.markdown("✅ Decode QR codes from uploaded images")
# # st.markdown("✅ Scan QR codes in real-time using your webcam")
# # st.markdown("✅ Download generated QR codes")
