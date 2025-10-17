import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Cartoonify Your Image", layout="centered")
st.title("🖼️ Cartoonify Your Image")

st.markdown("### 🎨 Convert your photo into a cartoon in one click! Upload any image and watch the magic happen ✨")

uploaded_file = st.file_uploader("📸 Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    cartoon_final = Image.fromarray(cartoon_rgb)

    st.subheader("📷 Original Image")
    st.image(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), use_container_width=True)

    st.subheader("🎭 Cartoonified Image")
    st.image(cartoon_final, caption="Cartoonified Result", use_container_width=True)

    buf = BytesIO()
    cartoon_final.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="⬇️ Download Cartoon Image",
        data=byte_im,
        file_name="cartoon.png",
        mime="image/png"
    )
else:
    st.info("👆 Upload an image above to start cartoonifying!")

st.markdown("---")
st.caption("✨ Built with Streamlit & OpenCV — by Priya")
