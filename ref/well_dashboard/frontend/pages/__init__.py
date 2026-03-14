"""
Page Modules — Well Dashboard Frontend

Each module exposes a single ``*_page()`` function that renders the full
content area for one top-level tab.

Pages
-----
projects    Project listing and creation (📋 Projects tab)
well_data   Well selection, creation, and detail editor (🔧 Well Data tab)
templates   Template browser and deletion (📐 Templates tab)
reports     Excel export controls (📊 Reports tab)
settings    User profile and API status (⚙️ Settings tab)

Adding a new page
-----------------
1. Create ``frontend/pages/my_page.py`` with a ``my_page()`` function.
2. Import and call it inside ``frontend/main.py`` for the corresponding tab.
3. Optionally add a tab entry in ``frontend/components/navigation.py``.
"""
