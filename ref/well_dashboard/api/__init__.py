"""
Well Dashboard API Package

This package contains the FastAPI backend for the Well Dashboard application.

Structure:
    routes/     - Route modules (auth, projects, wells, wellbore, export, etc.)
    models/     - Pydantic request/response models
    database.py - Async SQLite database operations
    auth.py     - JWT authentication utilities
    config.py   - Application configuration
    excel_export.py - Excel export engine
    main.py     - FastAPI app factory and router registration
"""
