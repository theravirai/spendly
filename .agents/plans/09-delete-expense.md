# Implementation Plan - Delete Expense

This plan details the implementation for Step 9: Delete Expense.

## Goal
Implement the delete expense functionality, allowing logged-in users to delete their existing expenses. Ensure authorization (ownership checks), deletion execution in the database, proper flash messages, dashboard updates, and visual confirmation on the frontend to prevent accidental deletion.

## Proposed Changes

### 1. Database Helpers
In [database/db.py](/outflow/database/db.py):
* Add `delete_expense(expense_id)` helper function:
  - Connect to the DB using `get_db()`.
  - Execute `DELETE FROM expenses WHERE id = ?`.
  - Execute the query within a transaction context (`with conn:`).
  - Close connection.

### 2. Flask Route and Views
In [app.py](/outflow/app.py):
* Import `delete_expense` from `database.db`.
* Update the placeholder `@app.route("/expenses/<int:id>/delete")` route:
  - Verify that the user is logged in (i.e. `session.get("user_id")` is present). If not, redirect to `/login`.
  - Fetch the expense using `get_expense_by_id(id)`.
  - If the expense does not exist, abort with a `404` Not Found error.
  - If the expense's `user_id` does not match the logged-in `session["user_id"]`, abort with a `403` Forbidden error.
  - Execute database deletion of the expense using `delete_expense(id)`.
  - Flash the success message `"Expense deleted successfully!"`.
  - Redirect the user to `/profile`.

### 3. Templates and CSS Styling
* **Template ([templates/profile.html](/outflow/templates/profile.html))**:
  - In each row of the transactions table, add a delete link/button next to the edit link in the Actions cell.
  - The delete link should point to `url_for('delete_expense', id=expense.id)`.
  - Include a Lucide icon for deletion (e.g. `data-lucide="trash-2"` or `data-lucide="trash"`).
  - To prevent accidental deletion, add an inline `onclick` handler: `onclick="return confirm('Are you sure you want to delete this expense?');"`.
* **Styles ([static/css/profile.css](/outflow/static/css/profile.css))**:
  - Style the delete action button (e.g., hover color changed to a red accent like `var(--error)` or similar).

### 4. Verification Plan
* Create a dedicated test file `tests/test_delete_expense.py` containing the following tests:
  - Unauthenticated access to `/expenses/<id>/delete` redirects to `/login`.
  - Authenticated deletion attempt of a non-existent expense ID returns `404`.
  - Authenticated deletion attempt of an expense belonging to another user returns `403`.
  - Successful authenticated deletion of an expense removes it from the database, redirects to `/profile`, and flashes `"Expense deleted successfully!"`.
  - Verify that dashboard statistics (Total Spent, Transactions, Top Category, and Category Breakdown) update correctly after deletion.
