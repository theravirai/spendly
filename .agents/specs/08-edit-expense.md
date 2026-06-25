# Spec: Edit Expense

## Overview
Step 8 implements the edit expense flow. Logged-in users will be able to update their existing expenses from the dashboard. This ensures that users can correct mistakes in their logged expenses (e.g., editing amount, category, date, or description) without having to delete and re-create them. It completes the update part of the CRUD operations for expenses, providing standard data editing features.

## Depends on
- **Step 3 — Login / Logout** (session management and login state verification)
- **Step 7 — Add Expense** (expense validation schema and creation, reusing form layout structure)

## Routes
| Method | Path                        | Description                                                                  | Access    |
|--------|-----------------------------|------------------------------------------------------------------------------|-----------|
| `GET`  | `/expenses/<int:id>/edit`   | Renders the "Edit Expense" form pre-populated with current expense details.  | Logged-in |
| `POST` | `/expenses/<int:id>/edit`   | Validates and updates the expense in the database.                           | Logged-in |

## Database changes
No database changes. The `expenses` table already contains all necessary columns.

We will add database helper functions to `database/db.py`:
- **`get_expense_by_id(expense_id)`** — retrieves an expense row matching the given `expense_id` as a dictionary/Row object. Returns `None` if not found.
- **`update_expense(expense_id, amount, category, date, description)`** — updates the details of the specified expense.

## Templates
- **Create:**
  - `templates/edit_expense.html` — The new standalone template that extends `base.html` and renders the pre-populated expense editing form.
- **Modify:**
  - `templates/profile.html` — Update the transactions table to include an "Actions" header and render an edit link/button (e.g. with a pencil icon) in each expense row.

## Files to change
| File                     | What changes                                                                                                               |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------|
| `app.py`                 | Import `get_expense_by_id` and `update_expense` from `database.db`; implement GET and POST for `/expenses/<int:id>/edit` with validation, login authentication, and user ownership validation. |
| `database/db.py`         | Add `get_expense_by_id(expense_id)` and `update_expense(expense_id, amount, category, date, description)` database helper functions. |
| `database/queries.py`    | Update `get_recent_transactions` query to fetch the expense `id` and include `"id": row["id"]` in the returned transaction dictionaries. |
| `templates/profile.html` | Add an Actions column to the table header and an Edit link (using a Lucide icon) to each transaction row.                  |
| `static/css/profile.css` | Style the actions column, edit button, and icons to align with the design theme.                                            |

## Files to create
| File                          | Description                                                                                       |
|-------------------------------|---------------------------------------------------------------------------------------------------|
| `templates/edit_expense.html` | Jinja2 template for the Edit Expense form page.                                                    |
| `tests/test_edit_expense.py`  | Pytest tests validating login authentication, ownership validation, input validation, and successful updates. |

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No JS frameworks — vanilla JS only
- No DB logic in route functions — all database queries must live in `database/db.py`
- User ownership validation:
  - If the expense does not exist, abort with `404` (Not Found).
  - If the expense exists but does not belong to the logged-in user, abort with `403` (Forbidden).
- Server-side validation:
  - `amount` must be present and a positive number (greater than 0).
  - `category` must be one of the predefined categories: `Food`, `Transport`, `Bills`, `Health`, `Entertainment`, `Shopping`, `Other`.
  - `date` must be present and in a valid date format (`YYYY-MM-DD`).
  - `description` is optional, but must not exceed 200 characters if provided, and should be stripped of leading/trailing whitespace.
  - If validation fails, the page must re-render showing the error message and preserving the user's inputs.

## Definition of done
- [ ] Profile page transactions table has a new column for Actions.
- [ ] An edit button (with a pencil icon) is shown next to each expense in the table.
- [ ] Clicking the edit button redirects the user to `/expenses/<id>/edit` (or requests login if not authenticated).
- [ ] The Edit Expense page renders a pre-populated form with the current expense values: Amount, Category, Date, and Description.
- [ ] Accessing a non-existent expense ID returns a `404` error.
- [ ] Accessing another user's expense ID returns a `403` Forbidden error.
- [ ] Submitting the edit form with valid modifications updates the database and redirects the user back to `/profile` with a success flash message ("Expense updated successfully!").
- [ ] The updated expense is correctly reflected on the dashboard/profile statistics (Total Spent, Category Breakdown, etc.).
- [ ] Submitting invalid inputs (e.g. negative/zero amount, invalid date format, invalid category, or long description) prevents DB update, displays a clean error banner, and preserves entered values.
- [ ] Canceling the edit returns the user to the profile page without modifying the expense.
- [ ] All tests in `tests/test_edit_expense.py` pass.
