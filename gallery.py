import streamlit as st
import sqlite3
from PIL import Image
import io

# Page Configuration
st.set_page_config(page_title="Art Gallery", layout="wide")

# Database Setup
DATABASE = "art_gallery.db"
ADMIN_PASSWORD = "___your_password___"  # Replace with a secure password

def init_db():
    """Initialize the database with the necessary tables."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            image BLOB
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(title, description, image):
    """Save an art piece to the database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO gallery (title, description, image) VALUES (?, ?, ?)', 
              (title, description, image))
    conn.commit()
    conn.close()

def fetch_art_pieces():
    """Fetch all art pieces from the database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT id, title, description, image FROM gallery ORDER BY id DESC')
    pieces = c.fetchall()
    conn.close()
    return pieces

def update_art_piece(piece_id, title, description):
    """Update an art piece's title and description."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('UPDATE gallery SET title = ?, description = ? WHERE id = ?', 
              (title, description, piece_id))
    conn.commit()
    conn.close()

def delete_art_piece(piece_id):
    """Delete an art piece from the database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM gallery WHERE id = ?', (piece_id,))
    conn.commit()
    conn.close()

# Initialize Database
init_db()

# Add custom CSS for styling
st.markdown("""
<style>
    .card {
        padding: 5px; /* Reduce padding inside the card */
        margin: 5px; /* Minimal margin between cards */
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .card img {
        border-radius: 10px;
        margin: 0; /* No extra margins around the image */
        display: block;
        width: 100%; /* Ensure the image fills the card */
    }
    .card-title {
        font-size: 16px; /* Reduce font size of the title */
        font-weight: bold;
        margin-top: 5px; /* Minimal spacing for the title */
    }
    .card-description {
        font-size: 12px; /* Reduce font size of the description */
        color: gray;
        margin: 2px 0; /* Minimal spacing for the description */
    }
</style>
""", unsafe_allow_html=True)

# Streamlit App Setup
st.title("🎨 Side-by-Side Art Gallery")
st.write("Explore stunning art pieces displayed in a horizontal layout.")

# Admin Authentication
is_admin = False
with st.sidebar.expander("Admin Login", expanded=False):
    admin_password = st.text_input("Enter Admin Password", type="password")
    if admin_password == ADMIN_PASSWORD:
        st.success("Admin Access Granted")
        is_admin = True
    elif admin_password:
        st.error("Incorrect Password")

# Admin Panel
if is_admin:
    with st.sidebar.expander("Admin Panel", expanded=False):
        st.markdown('<div class="admin-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload an image of the art piece", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Preview", use_column_width=True)

            # Get Title and Description
            title = st.text_input("Art Piece Title", "")
            description = st.text_area("Art Piece Description", "")

            # Save to Database
            if st.button("Add to Gallery", key="add_to_gallery"):
                # Convert the image to binary
                image_bytes = io.BytesIO()
                image.save(image_bytes, format=image.format)
                save_to_db(title, description, image_bytes.getvalue())
                st.success("Art piece added to the gallery!")
        st.markdown('</div>', unsafe_allow_html=True)

# Display Art Pieces Side by Side
st.header("🖼️ Art Pieces")
art_pieces = fetch_art_pieces()
if art_pieces:
    cols = st.columns(3)  # Divide the page into 3 columns
    for i, piece in enumerate(art_pieces):
        piece_id, title, description, image_data = piece
        col = cols[i % 3]  # Distribute pieces across columns
        with col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            image = Image.open(io.BytesIO(image_data))
            st.image(image, use_column_width=True)
            st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-description">{description}</div>', unsafe_allow_html=True)

            # Admin Controls
            if is_admin:
                with st.expander(f"Admin Controls for {title}"):
                    # Edit Title and Description
                    new_title = st.text_input(f"Edit Title for {title}", value=title, key=f"title_{piece_id}")
                    new_description = st.text_area(f"Edit Description for {title}", value=description, key=f"description_{piece_id}")
                    if st.button(f"Update {title}", key=f"update_{piece_id}"):
                        update_art_piece(piece_id, new_title, new_description)
                        st.success(f"{title} updated!")
                        st.experimental_rerun()

                    # Delete Art Piece
                    if st.button(f"Delete {title}", key=f"delete_{piece_id}"):
                        delete_art_piece(piece_id)
                        st.warning(f"{title} deleted!")
                        st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No art pieces in the gallery yet. Admins can upload art to get started!")
