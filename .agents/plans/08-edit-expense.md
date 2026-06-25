# Implementation Plan - Edit Expense

This plan details the implementation for Step 8: Edit Expense.

## Goal
Implement the edit expense flow, allowing logged-in users to modify their existing expenses. Ensure authorization (ownership checks), input validation, and proper database updates.

## Proposed Changes

### 1. Database Helpers
In [database/db.py](/expense-tracker/database/db.py):
* Add `get_expense_by_id(expense_id)` helper function:
  - Connect to the DB using `get_db()`.
  - Execute `SELECT * FROM expenses WHERE id = ?`.
  - Return the single row as a dictionary-like object (using `sqlite3.Row` functionality), or `None` if not found.
* Add `update_expense(expense_id, amount, category, date, description)` helper function:
  - Connect to the DB using `get_db()`.
  - Execute `UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ?`.
  - Run the query within a database transaction context (`with conn:`).

### 2. Update Queries
In [database/queries.py](/expense-tracker/database/queries.py):
* Modify `get_recent_transactions(user_id, limit=10, start_date=None, end_date=None)`:
  - Update the query select statement to include `id`: `SELECT id, date, description, category, amount FROM expenses ...`.
  - Include `"id": row["id"]` in the returned dictionary list elements.

### 3. Flask Route and Views
In [app.py](/expense-tracker/app.py):
* Import `get_expense_by_id` and `update_expense` from `database.db`.
* Update the placeholder `@app.route("/expenses/<int:id>/edit")` route to support `GET` and `POST` methods:
  - If user is not logged in (`session.get("user_id")` is absent), redirect to the login page.
  - Fetch the expense using `get_expense_by_id(id)`.
  - If the expense does not exist, abort with a `404` Not Found error.
  - If the expense's `user_id` does not match the logged-in `session["user_id"]`, abort with a `403` Forbidden error.
  - On `GET`, render `edit_expense.html` pre-populated with the fetched expense details.
  - On `POST`, retrieve and validate the request form parameters:
    - `amount`: non-empty, numeric float, greater than 0.
    - `category`: non-empty, must be one of `Food`, `Transport`, `Bills`, `Health`, `Entertainment`, `Shopping`, `Other`.
    - `date`: non-empty, matches `YYYY-MM-DD`.
    - `description`: optional, maximum 200 characters.
  - If validation fails, render `edit_expense.html` with an `error` message and preserve the user's updated form inputs.
  - If validation succeeds, update the expense using `update_expense(id, amount, category, date, description)`.
  - Flash the success message `"Expense updated successfully!"` and redirect to the `/profile` page.

### 4. Templates and CSS Styling
* **Template ([templates/profile.html](/expense-tracker/templates/profile.html))**:
  - Add an "Actions" header column in the transactions table: `<th>Actions</th>` (placed at the end, after `Amount`).
  - In each row of the transactions table, add an action cell containing an Edit link pointing to `url_for('edit_expense', id=expense.id)`. Include a Lucide pencil icon (e.g. `data-lucide="edit-2"` or `data-lucide="edit-3"`).
* **Styles ([static/css/profile.css](/expense-tracker/static/css/profile.css))**:
  - Style the action column and the edit button/icon. Ensure the edit link has hover states (e.g. changing color to `var(--accent)`).
* **Template ([templates/edit_expense.html](/expense-tracker/templates/edit_expense.html)) [NEW]**:
  - Create the standalone Jinja2 template extending `base.html`.
  - Reuse the same forms and styling classes as `add_expense.html` from `expense.css`.
  - Build the input form containing pre-populated fields: Amount, Category, Date, and Description.
  - Include cancel link routing back to `/profile` and submit button ("Save Changes").
  - Show error banner if a validation error is present.

### 5. Verification Plan
* Create a dedicated test file `tests/test_edit_expense.py`.
* Test cases:
  - Unauthenticated access to GET and POST `/expenses/<id>/edit` (should redirect to `/login`).
  - Accessing a non-existent expense ID (should return `404`).
  - Accessing another user's expense ID (should return `403`).
  - GET requests to edit own expense pre-populates form inputs with current database values.
  - Successful POST updates the DB, redirects to `/profile`, and flashes a success message.
  - Input validations (empty fields, invalid/negative amount, invalid category, date format, description too long) prevent updating the DB and show error banner with preserved values.
