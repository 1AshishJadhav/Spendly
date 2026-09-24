# Spec: Profile Page

## Overview

This feature replaces the /profile stub with a fully designed profile page showing static, hardcoded data. The goal is to establish the complete UI layout — user info card, transaction history table, summary stats, and category breakdown — before any real database queries are wired up in Step 5. Building the UI first lets the team validate the design in isolation and ensures the templates are ready for the backend-connection step.

## Depends on

- Step 1: Database setup (schema must exist)
- Step 2: Registration (user accounts must be creatable)
- Step 3: Login + Logout (session must be set; /profile must be a protected route)

## Routes

- `GET /profile` - Displays the current user's profile information - logged-in

## Database changes

No database changes.

## Templates

- Create: templates/profile.html — full profile page extending base.html; contains four sections:
  1. User info card — avatar initials, name, email, member-since date (all hardcoded)
  2. Summary stats row — total spent, number of transactions, top category (hardcoded)
  3. Transaction history table — list of recent expenses with date, description, category badge, amount (hardcoded rows)
  4. Category breakdown — per-category totals displayed as a simple list or progress-bar rows (hardcoded)
- Modify: `templates/base.html` - Add a link to the Profile page in the navigation bar (visible only when logged in).

## Files to change

- `app.py` - Implement the `profile()` route to fetch user data and render the template.
- `database/db.py` - Add a helper function `get_user_by_id(user_id)` to retrieve user details.
- `templates/base.html` - Update navigation.

## Files to create

- `templates/profile.html`
- `static/css/profile.css`

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variable - never hardcore hex values
- All templates extends base.html
- Ensure the route redirects to `/login` if the user is not authenticated.

## Definition of done

- [ ] Visiting `/profile` while logged in displays the correct name and email from the database.
- [ ] Visiting `/profile` while logged out redirects the user to the login page.
- [ ] The navigation bar in `base.html` contains a "Profile" link that is only visible to logged-in users.
- [ ] The page follows the project's styling guidelines using `profile.css`.
