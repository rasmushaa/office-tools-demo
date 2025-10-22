import io
import streamlit as st
from PIL import Image

PAGE_PRESETS = {
    "A4 (210 x 297 mm)": (210, 297),
    "Letter (8.5 x 11 in ≈ 216 x 279 mm)": (216, 279),
}

st.markdown("# Image to PDF")

preset = st.sidebar.selectbox("Page size", list(PAGE_PRESETS.keys()))
start_dpi = st.sidebar.number_input("Start DPI (resolution)", value=150, min_value=72, max_value=600, step=1)
target_kb = st.sidebar.number_input("Target file size (KB, 0 = no target)", value=0, min_value=0)

uploaded_files = st.file_uploader("Upload image files", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)


def page_pixels(mm_size, dpi):
    mm_per_inch = 25.4
    w_px = int(round(mm_size[0] / mm_per_inch * dpi))
    h_px = int(round(mm_size[1] / mm_per_inch * dpi))
    return (w_px, h_px)

def prepare_images(dpi):
    max_w, max_h = page_pixels(PAGE_PRESETS[preset], dpi)
    pil_images = []
    for f in uploaded_files:
        img = Image.open(f).convert("RGB")
        # Resize to fit page while keeping aspect ratio
        img.thumbnail((max_w, max_h), Image.LANCZOS)
        # Optional: center on white background of page size (uncomment if you want consistent page size)
        bg = Image.new("RGB", (max_w, max_h), (255, 255, 255))
        x = (max_w - img.width) // 2
        y = (max_h - img.height) // 2
        bg.paste(img, (x, y))
        pil_images.append(bg)
    return pil_images

def build_pdf_bytes(images, dpi):
    if not images:
        return b""
    buf = io.BytesIO()
    first, rest = images[0], images[1:]
    # Save as single PDF with all images
    first.save(buf, format="PDF", save_all=True, append_images=rest, dpi=(dpi, dpi))
    return buf.getvalue()

if uploaded_files:
    with st.status("Converting images to PDF...", expanded=True):
            
        current_dpi = int(start_dpi)
        min_dpi = 72
        pdf_bytes = None

        # Iteratively reduce DPI until under target_kb (if set) or until min_dpi reached
        while True:
            imgs = prepare_images(current_dpi)
            pdf_bytes = build_pdf_bytes(imgs, current_dpi)
            size_kb = len(pdf_bytes) / 1024
            if target_kb <= 0:
                break
            if size_kb <= target_kb or current_dpi <= min_dpi:
                break
            # reduce DPI (20% step)
            current_dpi = max(min_dpi, int(current_dpi * 0.8))
            st.write(f"Reduced DPI to {current_dpi} for target size {target_kb} KB (current size {size_kb:.1f} KB)")

        st.write(f"Result: {len(pdf_bytes)/1024:.1f} KB at {current_dpi} DPI.")

        # Provide download
        st.download_button(
            label="Download combined_images.pdf",
            data=pdf_bytes,
            file_name="combined_images.pdf",
            mime="application/pdf"
        )