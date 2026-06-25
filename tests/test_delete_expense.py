import pytest
from app import app
from database.db import get_db, init_db, seed_db

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch, tmp_path):
    """Sets up a temporary SQLite database for testing and overrides the path."""
    db_file = tmp_path / "test_expense_tracker.db"
    
    monkeypatch.setattr("database.db.DB_PATH", str(db_file))
    
    init_db()
    seed_db()
    
    yield

def test_delete_expense_route_unauthenticated():
    """Unauthenticated GET /expenses/<id>/delete should redirect to /login."""
    with app.test_client() as client:
        response = client.get("/expenses/1/delete")
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

def test_delete_expense_nonexistent():
    """Accessing non-existent expense for deletion should return 404."""
    with app.test_client() as client:
        # Log in (user_id = 1)
        client.post("/login", data={
            "email": "demo@spendly.com",
            "password": "demo123"
        })
        
        response = client.get("/expenses/9999/delete")
        assert response.status_code == 404

def test_delete_expense_unauthorized():
    """Accessing another user's expense for deletion should return 403."""
    # First, let's create a second user and add an expense for them
    conn = get_db()
    # Insert User 2
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("User Two", "two@spendly.com", "dummy_hash")
    )
    # Insert Expense for User 2 (user_id = 2)
    cur = conn.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        (2, 100.0, "Food", "2026-06-25", "Secret Lunch")
    )
    secret_expense_id = cur.lastrowid
    conn.commit()
    conn.close()

    with app.test_client() as client:
        # Log in as Demo User (user_id = 1)
        client.post("/login", data={
            "email": "demo@spendly.com",
            "password": "demo123"
        })
        
        # Try to delete User 2's expense
        response = client.get(f"/expenses/{secret_expense_id}/delete")
        assert response.status_code == 403

def test_delete_expense_success():
    """Successful GET /expenses/<id>/delete deletes the expense, redirects to /profile with flash."""
    with app.test_client() as client:
        # Log in
        client.post("/login", data={
            "email": "demo@spendly.com",
            "password": "demo123"
        })
        
        # Check initial count and sum of expenses for user_id = 1
        conn = get_db()
        initial_expenses = conn.execute("SELECT COUNT(*) as count, SUM(amount) as total FROM expenses WHERE user_id = 1").fetchone()
        conn.close()
        
        # Delete one of the seeded expenses (id = 1)
        response = client.get("/expenses/1/delete", follow_redirects=True)
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        
        # Should redirect to profile page and show success flash
        assert "Expense deleted successfully!" in html
        
        # Verify expense is deleted in DB
        conn = get_db()
        deleted_expense = conn.execute("SELECT * FROM expenses WHERE id = 1").fetchone()
        updated_expenses = conn.execute("SELECT COUNT(*) as count, SUM(amount) as total FROM expenses WHERE user_id = 1").fetchone()
        conn.close()
        
        assert deleted_expense is None
        assert updated_expenses["count"] == initial_expenses["count"] - 1
        assert updated_expenses["total"] == initial_expenses["total"] - 150.50  # Seeded expense 1 is 150.50
