import pytest
import sqlite3
from PIL import Image
import io
import os
from app import init_db, save_to_db, fetch_art_pieces, update_art_piece, delete_art_piece

# Create a temporary test database
TEST_DB = "test_gallery.db"

@pytest.fixture
def setup_db():
    """Fixture to set up and tear down the test database."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    conn = sqlite3.connect(TEST_DB)
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

    yield  # Test functions run here

    # Clean up after test
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_save_to_db(setup_db):
    """Test saving an art piece to the database."""
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()

    # Create a dummy image
    img = Image.new("RGB", (100, 100), color="red")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")

    # Save the image to the test database
    save_to_db("Test Art", "A test description", img_bytes.getvalue())

    # Fetch from database and verify
    c.execute("SELECT * FROM gallery")
    result = c.fetchone()
    assert result is not None, "No data found in the database."
    assert result[1] == "Test Art", "Title does not match."
    assert result[2] == "A test description", "Description does not match."

    conn.close()


def test_fetch_art_pieces(setup_db):
    """Test fetching art pieces from the database."""
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()

    # Insert a dummy art piece
    img = Image.new("RGB", (100, 100), color="blue")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    c.execute(
        "INSERT INTO gallery (title, description, image) VALUES (?, ?, ?)",
        ("Fetched Art", "This is a fetched art piece", img_bytes.getvalue()),
    )
    conn.commit()

    # Fetch art pieces
    art_pieces = fetch_art_pieces()
    assert len(art_pieces) == 1, "The number of art pieces does not match."
    assert art_pieces[0][1] == "Fetched Art", "The fetched art title does not match."

    conn.close()


def test_update_art_piece(setup_db):
    """Test updating an art piece in the database."""
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()

    # Insert a dummy art piece
    img = Image.new("RGB", (100, 100), color="green")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    c.execute(
        "INSERT INTO gallery (title, description, image) VALUES (?, ?, ?)",
        ("Original Art", "Original description", img_bytes.getvalue()),
    )
    conn.commit()

    # Get the piece ID
    c.execute("SELECT id FROM gallery WHERE title = 'Original Art'")
    piece_id = c.fetchone()[0]

    # Update the art piece
    update_art_piece(piece_id, "Updated Art", "Updated description")

    # Verify the update
    c.execute("SELECT title, description FROM gallery WHERE id = ?", (piece_id,))
    updated_piece = c.fetchone()
    assert updated_piece[0] == "Updated Art", "The title was not updated."
    assert updated_piece[1] == "Updated description", "The description was not updated."

    conn.close()


def test_delete_art_piece(setup_db):
    """Test deleting an art piece from the database."""
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()

    # Insert a dummy art piece
    img = Image.new("RGB", (100, 100), color="purple")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    c.execute(
        "INSERT INTO gallery (title, description, image) VALUES (?, ?, ?)",
        ("Delete Art", "This will be deleted", img_bytes.getvalue()),
    )
    conn.commit()

    # Get the piece ID
    c.execute("SELECT id FROM gallery WHERE title = 'Delete Art'")
    piece_id = c.fetchone()[0]

    # Delete the art piece
    delete_art_piece(piece_id)

    # Verify the deletion
    c.execute("SELECT * FROM gallery WHERE id = ?", (piece_id,))
    deleted_piece = c.fetchone()
    assert deleted_piece is None, "The art piece was not deleted."

    conn.close()
