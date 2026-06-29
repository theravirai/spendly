# Spec: Demo Mode

## Overview
Recruiters and hiring managers should be able to explore the Outflow application immediately with a single click, bypassing the sign-up flow. "Demo Mode" creates a dedicated, session-isolated, and pre-populated temporary demo user account loaded with realistic, multi-month financial transactions spanning all 8 core expense categories. The interface will feature prominent visual indicators (a top banner, navbar status badge, and custom CTAs) to signal they are in Demo Mode and make it simple to transition to creating a personal account.

## Depends on
- **Step 03 — Login and Logout**: Session management and authentication helpers.
- **Step 05 — Backend connection for profile**: Profile stats, breakdowns, and recent transactions.
- **Step 08 — Edit expense**: Editing existing expenses.
- **Step 09 — Delete expense**: Deleting existing expenses.

## Routes
- `GET /demo` — Public. Clean up expired temporary accounts, dynamically provision a temporary demo user, seed multi-month expense history, set `session["user_id"]`, `session["user_name"]`, and `session["is_demo"] = True`, and redirect to `/profile`.
- `GET /register` — Public (Modified). If the user is in Demo Mode, they can still view registration to sign up. If they sign up successfully, clear the demo session and log them into the new account.
- `GET /login` — Public (Modified). If the user is in Demo Mode and navigates to login, continue to login normally.

## Database changes
No schema modifications are required. Standard `users` and `expenses` tables are used. Temporary demo users are created with:
- `name = "Demo Mode"`
- `email = "demo_session_<uuid>@outflow.com"` (generated dynamically using Python's `uuid` library)

## Templates
- **Create:** None.
- **Modify:**
  - `templates/landing.html`: Replace the "See Demo" video modal button with "Try Demo" linking to the `/demo` route.
  - `templates/base.html`:
    - Insert a subtle, sticky top warning banner at the top of the body when `session["is_demo"]` is active, reading: *"You are exploring Outflow in Demo Mode. Changes made here are temporary and may be reset."* and a CTA link *"Create Your Account"*.
    - Customize navbar: if in Demo Mode, display a green "Demo Mode" pill/badge with a pulsing dot, a "Create Account" CTA, and a "Sign out" link.
  - `templates/add_expense.html` & `templates/edit_expense.html`: Update the Category select list options to include `Healthcare` and `Travel`.

## Files to change
- `app.py`: Define new `/demo` route, update validation logic for categories to include `Healthcare` and `Travel`.
- `database/db.py`: Add `create_demo_user()` helper, add relative multi-month expense seeding, and add `cleanup_old_demo_users()` function to remove accounts older than 24 hours.
- `static/css/style.css`: Add styles for `.demo-banner`, `.demo-banner-inner`, `.demo-banner-cta`, `.nav-demo-badge`, and `.nav-demo-dot` with subtle pulsing animation.
- `static/css/profile.css`: Add category bar colors and badge colors for `.bar-healthcare`, `.bar-travel`, `.badge-healthcare`, and `.badge-travel`.
- `templates/base.html`
- `templates/landing.html`
- `templates/add_expense.html`
- `templates/edit_expense.html`

## New dependencies
Uses Python's standard `uuid` module for generating unique emails.

## Rules for implementation
- Keep database operations inside `database/db.py`.
- Ensure all category updates are backward compatible.
- Clean up expired demo users automatically during the `/demo` login flow to prevent DB clutter.
- Do not expose any email or password credentials for the demo mode anywhere in the UI or javascript.
- All styles must use existing CSS design system tokens (e.g. `var(--accent)`, `var(--accent-2)`, etc.).

## Definition of done
- [ ] Clicking "Try Demo" on the landing page immediately redirects to the dashboard `/profile` with a successful login.
- [ ] A dedicated session-isolated user is created, populated with relative multi-month expenses across Food, Transport, Bills, Shopping, Entertainment, Healthcare, Travel, and Other.
- [ ] No login credentials are required or exposed.
- [ ] The top warning banner is visible on all pages while logged in as a demo user.
- [ ] The navbar clearly displays "Demo Mode" and provides a CTA to "Create Account".
- [ ] Adding, editing, and deleting expenses is fully functional inside Demo Mode, only affecting the current visitor's session.
- [ ] All pre-existing unit and integration tests continue to pass.
- [ ] Outflow runs correctly on port 5001.
