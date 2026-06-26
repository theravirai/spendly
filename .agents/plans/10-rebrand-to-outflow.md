# Plan - Rebrand Outflow to Outflow

This plan outlines the steps to perform a complete product rebrand of the expense tracker application from **Outflow** to **Outflow**.

## Steps

1. **Update Codebase Documents and Configs**
   - Update [AGENTS.md](/outflow/AGENTS.md) to use "Outflow" and "outflow".

2. **Update Database Helpers and Seed Data**
   - Update [database/db.py](/outflow/database/db.py) to rename seed user email from `demo@outflow.com` to `demo@outflow.com`.

3. **Update UI Templates**
   - Update page titles, meta/SEO details, and copy across all HTML templates:
     - [templates/base.html](/outflow/templates/base.html) (Navbar, Footer, general title)
     - [templates/landing.html](/outflow/templates/landing.html) (Hero text, Badges, CTAs, Copy)
     - [templates/login.html](/outflow/templates/login.html) & [templates/register.html](/outflow/templates/register.html) (Auth titles/subtitles)
     - [templates/profile.html](/outflow/templates/profile.html) (Dashboard overview text, headings)
     - [templates/add_expense.html](/outflow/templates/add_expense.html) & [templates/edit_expense.html](/outflow/templates/edit_expense.html) (Titles)
     - [templates/privacy.html](/outflow/templates/privacy.html) & [templates/terms.html](/outflow/templates/terms.html) (Copy and support emails)

4. **Update Tests**
   - Update email assertions and mock requests in all files under the `tests/` directory to use `@outflow.com` instead of `@outflow.com`.

5. **Verify and Clean Up**
   - Run `pytest` to ensure all tests pass.
   - Perform a case-insensitive search for "outflow" to ensure no occurrences remain in the core codebase.
