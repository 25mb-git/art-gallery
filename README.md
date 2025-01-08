# 🎨 Streamlit Art Gallery

The application has been deployed on an 8GB Mac Mini. Access the live app here:
https://mac-mini.boga-vector.ts.net/

A sleek, side-by-side art gallery application built with [Streamlit](https://streamlit.io). This app allows you to display, manage, and explore stunning art pieces in a modern and interactive layout.

---

## ✨ Features

- **Side-by-Side Display**: Art pieces are displayed in a responsive grid layout with evenly spaced columns.
- **Admin Controls**: Admins can log in to:
  - Add new art pieces with titles and descriptions.
  - Edit the title and description of existing art pieces.
  - Delete art pieces from the gallery.
- **Customizable Styling**: Includes hover effects, shadows, and clean typography for a professional gallery look.
- **Secure Admin Access**: Protected by an admin password, ensuring only authorized users can manage the gallery.

---

## 📦 Installation

### Prerequisites

- Python 3.8 or later
- [Streamlit](https://streamlit.io)
- SQLite (default database, no additional setup required)

### Clone the Repository

1. **Clone this repository**:  
   ```bash
   git clone https://github.com/25mb-git/art-gallery.git
    ```
2. **Install dependencies**:
   ```bash
    pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
    streamlit run gallery.py
    ```

## Test Code
### Test case

1. test_save_to_db:
  Tests adding an art piece to the database.
  Verifies that the image, title, and description are saved correctly.

2. test_fetch_art_pieces:
  Inserts an art piece and fetches it using fetch_art_pieces().
  Verifies the fetched data matches the inserted data.

3. test_update_art_piece:
  Inserts an art piece and updates its title and description.
  Verifies that the update operation was successful.

4. test_delete_art_piece:
  Inserts an art piece and deletes it.
  Verifies that the art piece is no longer in the database.

### Test execution
1. **Run test code:**:
   ```bash
   pip install pytest
    ```

Make sure pytest is installed:

2. **Run test code:**:
   ```bash
    pytest test/test_app.py
    ```
