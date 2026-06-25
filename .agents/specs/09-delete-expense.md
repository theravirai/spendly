# Spec: Delete Expense

## Overview
Step 9 implements the delete expense functionality. Logged-in users will be able to delete an existing expense from the profile/dashboard page. This ensures that users can completely remove incorrect or obsolete expenses, completing the full CRUD capability (Create, Read, Update, Delete) of the Spendly personal expense tracker.

## Depends on
- **Step 3 — Login / Logout** (session management and login state verification)
- **Step 8 — Edit Expense** (expense management, Actions column styling and layout)

## Routes
| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/expenses/<int:id>/delete` | Verifies ownership and deletes the specified expense, then redirects to `/profile`. | Logged-in |

## Database changes
No database changes. The `expenses` table already contains all necessary columns.

We will add a database helper function to `database/db.py`:
- **`delete_expense(expense_id)`** — deletes the expense row matching the given `expense_id` from the `expenses` table.

## Templates
- **Modify:**
  - `templates/profile.html` — Add a delete button (with a trash icon) next to the edit button in the Actions column. Set its `href` to the delete route and include a JavaScript `confirm()` dialog on click to prevent accidental deletion.

## Files to change
| File | What changes |
|---|---|
| `app.py` | Import `delete_expense` from `database.db`. Implement GET for `/expenses/<int:id>/delete` with login authentication, user ownership validation, deletion logic, and a success flash message. |
| `database/db.py` | Add the `delete_expense(expense_id)` helper function. |
| `templates/profile.html` | Add a Delete link/button with a trash icon (using Lucide icons) and an `onclick` confirmation handler inside the Actions column. |
| `static/css/profile.css` | Add styles for the delete action button (hover/active state colors, red tint/alert theme) to match the existing visual language. |

## Files to create
| File | Description |
|---|---|
| `tests/test_delete_expense.py` | Pytest tests validating login authentication, ownership validation, successful deletion, and visual update of statistics. |

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
- Accidental prevention:
  - The Delete link must trigger a browser `confirm()` popup before navigating to the route.

## Definition of done
- [ ] Profile page transactions table has a delete button (with a trash/trash-2 icon) next to the edit button.
- [ ] Clicking the delete button prompts the user with a confirmation dialog ("Are you sure you want to delete this expense?").
- [ ] If the user cancels the confirmation, the deletion is aborted.
- [ ] Clicking the delete button and confirming redirects the user to `/expenses/<id>/delete` (or redirects to login if not authenticated).
- [ ] Accessing `/expenses/<id>/delete` directly with a non-existent expense ID returns a `404` error.
- [ ] Accessing `/expenses/<id>/delete` directly with another user's expense ID returns a `403` Forbidden error.
- [ ] Confirming the deletion removes the expense from the database and redirects the user back to `/profile` with a success flash message ("Expense deleted successfully!").
- [ ] The deleted expense is no longer visible in the Recent Expenses table.
- [ ] The dashboard statistics (Total Spent, Transactions, Top Category, and Category Breakdown) update correctly to reflect the deletion.
- [ ] All tests in `tests/test_delete_expense.py` pass.
