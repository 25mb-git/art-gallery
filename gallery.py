import streamlit as st
import sqlite3
from PIL import Image, UnidentifiedImageError
import io

# Page Configuration
st.set_page_config(page_title="Art and Video Gallery", layout="wide")

# Database Setup
DATABASE = "art_gallery.db"
ADMIN_PASSWORD = "___your_password___"  # Replace with a secure password

def init_db():
    """Initialize the database with the necessary tables and columns."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create gallery table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS gallery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        media BLOB,
        media_type TEXT
    )
    ''')

    # Create counter table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS view_counter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        count INTEGER
    )
    ''')

    # Initialize counter if empty
    c.execute("SELECT COUNT(*) FROM view_counter")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO view_counter (count) VALUES (0)")
    conn.commit()
    conn.close()

def increment_counter():
    """Increment the web page view counter."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE view_counter SET count = count + 1 WHERE id = 1")
    conn.commit()
    conn.close()

def get_page_views():
    """Get the current web page view count."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT count FROM view_counter WHERE id = 1")
    views = c.fetchone()[0]
    conn.close()
    return views

def save_to_db(title, description, media, media_type):
    """Save an art piece or video to the database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO gallery (title, description, media, media_type) VALUES (?, ?, ?, ?)', 
              (title, description, media, media_type))
    conn.commit()
    conn.close()

def fetch_gallery_items():
    """Fetch all gallery items (art pieces and videos) from the database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT id, title, description, media, media_type FROM gallery ORDER BY id DESC')
    items = c.fetchall()
    conn.close()
    return items

def update_gallery_item(item_id, title, description, new_media=None, new_media_type=None):
    """Update the title, description, and optionally the media of a gallery item."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    if new_media and new_media_type:
        c.execute('UPDATE gallery SET title = ?, description = ?, media = ?, media_type = ? WHERE id = ?', 
                  (title, description, new_media, new_media_type, item_id))
    else:
        c.execute('UPDATE gallery SET title = ?, description = ? WHERE id = ?', 
                  (title, description, item_id))
    
    conn.commit()
    conn.close()

def delete_gallery_item(item_id):
    """Delete a gallery item from the database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM gallery WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Initialize Database and Increment Counter
init_db()
increment_counter()

# Add custom CSS for styling
st.markdown("""
<style>
    .card {
        padding: 5px;
        margin: 5px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .card img, .card video {
        border-radius: 10px;
        margin: 0;
        display: block;
        width: 100%;
    }
    .card-title {
        font-size: 16px;
        font-weight: bold;
        margin-top: 5px;
    }
    .card-description {
        font-size: 12px;
        color: gray;
        margin: 2px 0;
    }
    .github-link {
        font-size: 10px;  /* Smaller font for GitHub link */
        text-align: left;
        margin-top: 10px;
        color: #666;  /* Gray color */
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        font-size: 12px;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit App Setup
st.title("❤️ Art and Video Gallery")
st.write("Millie Bay @ British School in Tokyo")
st.markdown(
    '<div class="github-link">'
    'Source code for this blog: <a href="https://github.com/25mb-git/art-gallery" target="_blank">visit my GitHub</a>'
    '</div>',
    unsafe_allow_html=True,
)

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
        uploaded_file = st.file_uploader("Upload an image or video", type=["png", "jpg", "jpeg", "mp4", "mov", "avi"])

        if uploaded_file:
            # Determine media type
            if uploaded_file.type.startswith("image"):
                media_type = "image"
                preview_media = Image.open(uploaded_file)
                st.image(preview_media, caption="Preview Image", use_column_width=True)
                media_bytes = io.BytesIO()
                preview_media.save(media_bytes, format=uploaded_file.type.split("/")[-1].upper())
                media_data = media_bytes.getvalue()  # Convert image to bytes
            elif uploaded_file.type.startswith("video"):
                media_type = "video"
                media_data = uploaded_file.getvalue()  # Directly use bytes for videos
                st.video(media_data)

            # Get Title and Description
            title = st.text_input("Media Title", "")
            description = st.text_area("Media Description", "")

            # Save to Database
            if st.button("Add to Gallery", key="add_to_gallery"):
                save_to_db(title, description, media_data, media_type)
                st.success("Media added to the gallery!")

# Display Art Pieces and Videos Side by Side
st.header("Gallery")
gallery_items = fetch_gallery_items()
if gallery_items:
    cols = st.columns(3)  # Divide the page into 3 columns
    for i, item in enumerate(gallery_items):
        item_id, title, description, media_data, media_type = item
        col = cols[i % 3]  # Distribute items across columns
        with col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            if media_type == "image":
                try:
                    image = Image.open(io.BytesIO(media_data))
                    st.image(image, use_column_width=True)
                except UnidentifiedImageError:
                    st.error(f"Unable to display {title}. The file might be corrupted or not an image.")
            elif media_type == "video":
                st.video(media_data)

            st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-description">{description}</div>', unsafe_allow_html=True)

            # Admin Controls
            if is_admin:
                with st.expander(f"Admin Controls for {title}"):
                    new_title = st.text_input(f"Edit Title for {title}", value=title, key=f"title_{item_id}")
                    new_description = st.text_area(f"Edit Description for {title}", value=description, key=f"description_{item_id}")

                    # Upload new media for replacement
                    new_media_file = st.file_uploader(f"Upload new media for {title}", type=["png", "jpg", "jpeg", "mp4", "mov", "avi"], key=f"update_media_{item_id}")
                    new_media_data = None
                    new_media_type = None

                    if new_media_file:
                        if new_media_file.type.startswith("image"):
                            new_media_type = "image"
                            new_preview_media = Image.open(new_media_file)
                            st.image(new_preview_media, caption="New Image Preview", use_column_width=True)
                            new_media_bytes = io.BytesIO()
                            new_preview_media.save(new_media_bytes, format=new_media_file.type.split("/")[-1].upper())
                            new_media_data = new_media_bytes.getvalue()
                        elif new_media_file.type.startswith("video"):
                            new_media_type = "video"
                            new_media_data = new_media_file.getvalue()
                            st.video(new_media_data)

                    if st.button(f"Update {title}", key=f"update_{item_id}"):
                        update_gallery_item(item_id, new_title, new_description, new_media_data, new_media_type)
                        st.success(f"{title} updated!")
                        st.experimental_rerun()

                    if st.button(f"Delete {title}", key=f"delete_{item_id}"):
                        delete_gallery_item(item_id)
                        st.warning(f"{title} deleted!")
                        st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No art pieces or videos in the gallery yet. Admins can upload content to get started!")

# Footer Section
page_views = get_page_views()
st.markdown(f"""
<div class="footer">
    <p>© 2025 Millie Bay. All rights reserved.</p>
    <p>Page Views: {page_views}</p>
</div>
""", unsafe_allow_html=True)
