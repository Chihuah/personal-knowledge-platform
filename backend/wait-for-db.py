#!/usr/bin/env python
"""
Wait for PostgreSQL database to be ready before running migrations and starting the application.
This script handles connection retries with exponential backoff.
"""

import os
import sys
import time
import subprocess
from urllib.parse import urlparse

import psycopg


def parse_db_url(db_url: str) -> dict:
    """Parse PostgreSQL connection URL."""
    parsed = urlparse(db_url)
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "user": parsed.username or "postgres",
        "password": parsed.password or "",
        "dbname": parsed.path.lstrip("/") or "postgres",
    }


def wait_for_db(db_url: str, max_retries: int = 30, initial_delay: float = 1.0) -> bool:
    """
    Wait for PostgreSQL to be ready.
    
    Args:
        db_url: PostgreSQL connection URL
        max_retries: Maximum number of connection attempts
        initial_delay: Initial delay between retries (seconds)
    
    Returns:
        True if connection successful, False if max retries exceeded
    """
    db_params = parse_db_url(db_url)
    retry_count = 0
    delay = initial_delay
    
    print(f"Waiting for PostgreSQL at {db_params['host']}:{db_params['port']}...")
    
    while retry_count < max_retries:
        try:
            conn = psycopg.connect(
                host=db_params["host"],
                port=db_params["port"],
                user=db_params["user"],
                password=db_params["password"],
                dbname=db_params["dbname"],
                connect_timeout=5,
            )
            conn.close()
            print("✓ PostgreSQL is ready!")
            return True
        except (psycopg.OperationalError, psycopg.Error) as e:
            retry_count += 1
            if retry_count >= max_retries:
                print(f"✗ Failed to connect to PostgreSQL after {max_retries} attempts")
                print(f"Last error: {e}")
                return False
            
            print(f"Connection attempt {retry_count}/{max_retries} failed, retrying in {delay}s...")
            time.sleep(delay)
            # Exponential backoff with max 10 seconds
            delay = min(delay * 1.5, 10.0)
    
    return False


def run_migrations() -> bool:
    """Run Alembic migrations."""
    print("Running database migrations...")
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd="/app/backend",
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            print("✓ Migrations completed successfully")
            return True
        else:
            print(f"✗ Migration failed with return code {result.returncode}")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("✗ Migration timed out")
        return False
    except Exception as e:
        print(f"✗ Migration error: {e}")
        return False


def start_application() -> None:
    """Start the FastAPI application."""
    print("Starting FastAPI application...")
    subprocess.run(
        [
            "uvicorn",
            "app.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
        cwd="/app/backend",
    )


def main():
    """Main entry point."""
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://pkp:pkp@postgres:5432/pkp",
    )
    
    # Remove the driver prefix for connection testing
    if "+" in db_url:
        db_url_for_test = db_url.replace("+psycopg", "")
    else:
        db_url_for_test = db_url
    
    # Wait for database
    if not wait_for_db(db_url_for_test):
        print("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("Failed to run migrations. Exiting.")
        sys.exit(1)
    
    # Start application
    start_application()


if __name__ == "__main__":
    main()
