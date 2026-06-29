# Implementation Plan: Demo Mode

This plan details the implementation for adding a session-isolated Demo Mode to the Outflow expense tracker.

## Goal
Hiring managers and recruiters must be able to explore the fully functional application with a single click from the landing page. Their operations must be isolated to their own temporary database user and seed data to prevent visual interference between simultaneous visitors, while keeping the database clean.

## Proposed Changes

### 1. Database Helpers & Data Seeding

#### [MODIFY] [db.py](/outflow/database/db.py)
- Import `uuid` and `date` / `timedelta`.
- Add `cleanup_old_demo_users()`:
  - Query for user IDs where `email LIKE 'demo_session_%'` and `created_at < datetime('now', '-24 hours')`.
  - For found user IDs, delete from `expenses` then delete from `users` (to respect foreign key constraints).
- Add `create_demo_user()`:
  - Generate a random UUID: `uid = uuid.uuid4().hex`.
  - Create user with name `"Demo Mode"` and email `f"demo_session_{uid}@outflow.com"`.
  - Return `(user_id, name)`.
  - Generate a rich list of relative expenses spanning the last 90 days.
  - Insert all expenses using `conn.executemany` with categories: `Food`, `Transport`, `Bills`, `Shopping`, `Entertainment`, `Healthcare`, `Travel`, `Other`.
  
  *Relative expense data outline (computed relative to `date.today()`):*
  - **Bills**: monthly rent (€850) and utilities (€120) at days -5, -35, -65.
  - **Food**: groceries (€60 to €90) every 5 days; coffee/dining out (€15 to €40) every 3 days.
  - **Transport**: public transport pass (€45) every 30 days; taxi/ride (€25) every 10 days.
  - **Shopping**: clothing (€120) at day -12; electronics (€89) at day -40.
  - **Entertainment**: movie tickets (€22) at day -2; concert ticket (€65) at day -28.
  - **Healthcare**: pharmacy (€25) at day -8; dentist (€75) at day -45.
  - **Travel**: weekend trip flight (€180) at day -22; hotel (€140) at day -21.
  - **Other**: gift for friend (€35) at day -15.

### 2. Routes & Controller Logic

#### [MODIFY] [app.py](/outflow/app.py)
- Import `uuid`.
- Add a new route `GET /demo`:
  - Run `cleanup_old_demo_users()`.
  - Call `create_demo_user()` to create and seed the new temporary demo account.
  - Store `session["user_id"] = user_id`, `session["user_name"] = user_name`, and `session["is_demo"] = True`.
  - Flash a welcome message.
  - Redirect to `profile`.
- Update `valid_categories` in `add_expense()` and `edit_expense()` to include `"Healthcare"` and `"Travel"`:
  ```python
  valid_categories = ["Food", "Transport", "Bills", "Health", "Healthcare", "Travel", "Entertainment", "Shopping", "Other"]
  ```

### 3. UI Stylesheets

#### [MODIFY] [style.css](/outflow/static/css/style.css)
- Add styles for the top banner:
  - `.demo-banner`: light amber warning background (`var(--accent-2-light)`), sticky position, 1px bottom border.
  - `.demo-banner-inner`: flex layout, handles text and CTA alignment.
  - `.demo-banner-cta`: underlined text using `var(--accent-2)`.
- Add styles for the navbar demo elements:
  - `.nav-demo-badge`: rounded pill, background `var(--accent-light)`, text color `var(--accent)`.
  - `.nav-demo-dot`: small green dot pulsing using CSS `@keyframes pulse`.

#### [MODIFY] [profile.css](/outflow/static/css/profile.css)
- Define colors and classes for the new categories:
  - `:root`: add `--color-healthcare: var(--danger);` and `--color-travel: #2a9d8f;`
  - Add progress fills: `.bar-healthcare` and `.bar-travel`.
  - Add badges: `.badge-healthcare` and `.badge-travel`.

### 4. HTML Templates

#### [MODIFY] [landing.html](/outflow/templates/landing.html)
- Replace the secondary CTA button with:
  ```html
  <a href="{{ url_for('demo_login') }}" class="btn-hero-secondary">Try Demo</a>
  ```

#### [MODIFY] [base.html](/outflow/templates/base.html)
- Add the sticky `.demo-banner` just above the navbar if `session.get('is_demo')` is true.
- Modify the navbar logic:
  - If `session.get('is_demo')` is true, show the "Demo Mode" pill badge, a "Create Account" CTA button (linking to `/register`), and a "Sign out" link.
  - Else, show standard user greeting or login/get started actions.

#### [MODIFY] [add_expense.html](/outflow/templates/add_expense.html) & [edit_expense.html](/outflow/templates/edit_expense.html)
- Add select options for `<option value="Healthcare">Healthcare</option>` and `<option value="Travel">Travel</option>`.

## Verification Plan

### Manual Verification
1. Open the homepage, click "Try Demo".
2. Confirm instant login and redirection to `/profile`.
3. Confirm the demo banner is shown at the top of the screen.
4. Confirm the navbar badge "Demo Mode" is displayed with a pulsing green dot, and the "Create Account" button is present.
5. Review the statistics cards, category breakdown progress bars, and recent transactions list to verify multiple months of realistic transactions are present.
6. Verify categories: Add a new expense with category "Healthcare" and another with "Travel", and verify they render correctly with proper styling and badge colors.
7. Edit and delete some transactions, verifying they reflect instantly.
8. Click "Create Account" or "Sign out" in the navbar, and verify they navigate to the registration/login pages correctly.
9. Open another browser/incognito window, click "Try Demo" again, and verify that the data in the second browser is independent and does not show the edits/additions from the first session.

### Automated Verification
1. Run `pytest` to verify that existing registration, login, add, edit, and delete tests still pass successfully.
