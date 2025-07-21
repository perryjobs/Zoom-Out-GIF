import streamlit as st
from PIL import Image
import io

st.title("Zoom-Out Transition GIF Generator")

# Upload image
uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    orig_width, orig_height = image.size

    # Display image and show its size
    st.image(image, caption="Uploaded Image", use_container_width=True)
    st.write(f"Image dimensions: {orig_width}x{orig_height}")

    # Set default output resolution to image size
    default_width = orig_width
    default_height = orig_height

    # Allow user to adjust output resolution
    output_width = st.number_input("Output resolution width", value=default_width, step=50)
    output_height = st.number_input("Output resolution height", value=default_height, step=50)

    total_zoom_frames = st.number_input("Number of zoom-out frames", value=30, step=1)
    initial_zoom = st.number_input("Initial zoom level", value=1.5, step=0.1)
    final_zoom = st.number_input("Final zoom level", value=1.0, step=0.1)

    generate_button = st.button("Generate GIF")

    if generate_button:
        # Generate frames
        frames = []

        def generate_zoom_frame(frame_idx):
            progress = frame_idx / (total_zoom_frames - 1)
            zoom = initial_zoom + (final_zoom - initial_zoom) * progress
            new_width = int(orig_width * zoom)
            new_height = int(orig_height * zoom)
            resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            left = (new_width - output_width) // 2
            top = (new_height - output_height) // 2
            right = left + output_width
            bottom = top + output_height
            frame_img = resized_img.crop((left, top, right, bottom))
            return frame_img

        with st.spinner("Generating frames..."):
            for i in range(total_zoom_frames):
                frame = generate_zoom_frame(i)
                frames.append(frame)

        # Save GIF in memory
        gif_bytes = io.BytesIO()
        frames[0].save(
            gif_bytes,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0
        )
        gif_bytes.seek(0)

        # Display the GIF
        st.image(gif_bytes, caption="Zoom-Out GIF", use_container_width=True)

        # Download button
        st.download_button(
            label="Download GIF",
            data=gif_bytes,
            file_name="zoom_out.gif",
            mime="image/gif"
        )
else:
    st.info("Please upload an image to begin.")
