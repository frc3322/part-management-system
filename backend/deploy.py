#!/usr/bin/env python3
"""Deployment script for the Part Management System backend."""

import os
import sys
import subprocess
import argparse

# Constants for repeated values
DEFAULT_DATABASE_URL = "sqlite:///parts_prod.db"
SECRET_KEY_WARNING = "   WARNING: Using auto-generated SECRET_KEY. Set SECRET_KEY environment variable in production!"


def run_command(command: str, description: str, env: dict = None) -> bool:
    """Run a shell command and return success status.

    Args:
        command: Command to execute
        description: Description of the command for logging
        env: Environment variables to set for the command

    Returns:
        bool: True if command succeeded, False otherwise
    """
    print(f"[DEPLOY] {description}")
    print(f"   Command: {command}")

    try:
        subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True, env=env
        )
        print("   SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   FAILED with exit code {e.returncode}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False


def check_uv() -> bool:
    """Check if uv is installed."""
    return run_command("uv --version", "Checking uv installation")


def install_dependencies() -> bool:
    """Install project dependencies using uv."""
    return run_command(
        "uv pip install -r requirements.txt", "Installing dependencies with uv"
    )


def run_development() -> bool:
    """Run the application in development mode."""
    return run_command("uv run python run.py", "Starting development server")


def run_production_multiworker(workers: int = 4, port: int = 8000) -> bool:
    """Run the application in production mode with multiple workers."""
    env = os.environ.copy()
    if not env.get("DATABASE_URL"):
        env["DATABASE_URL"] = DEFAULT_DATABASE_URL
    if not env.get("SECRET_KEY"):
        import secrets

        env["SECRET_KEY"] = secrets.token_hex(32)
        print(f"SECRET_KEY: {env['SECRET_KEY']}")
        print(SECRET_KEY_WARNING)
    if not env.get("FLASK_ENV"):
        env["FLASK_ENV"] = "production"

    command = f"uv run gunicorn -w {workers} -b 0.0.0.0:{port} run_prod:app"
    return run_command(
        command, f"Starting production server (multi-worker, {workers} workers)", env
    )


def run_production_eventlet(port: int = 8000) -> bool:
    """Run the application in production mode with eventlet (Linux/macOS only)."""
    env = os.environ.copy()
    if not env.get("DATABASE_URL"):
        env["DATABASE_URL"] = DEFAULT_DATABASE_URL
    if not env.get("SECRET_KEY"):
        import secrets

        env["SECRET_KEY"] = secrets.token_hex(32)
        print(f"SECRET_KEY: {env['SECRET_KEY']}")
        print(SECRET_KEY_WARNING)
    if not env.get("FLASK_ENV"):
        env["FLASK_ENV"] = "production"

    command = f"uv run gunicorn -k eventlet -w 1 -b 0.0.0.0:{port} run_prod:app"
    return run_command(
        command, "Starting production server (eventlet - Unix only)", env
    )


def run_production_gevent(workers: int = 4, port: int = 8000) -> bool:
    """Run the application in production mode with gevent (Linux/macOS only)."""
    env = os.environ.copy()
    if not env.get("DATABASE_URL"):
        env["DATABASE_URL"] = DEFAULT_DATABASE_URL
    if not env.get("SECRET_KEY"):
        import secrets

        env["SECRET_KEY"] = secrets.token_hex(32)
        print(f"SECRET_KEY: {env['SECRET_KEY']}")
        print(SECRET_KEY_WARNING)
    if not env.get("FLASK_ENV"):
        env["FLASK_ENV"] = "production"

    command = f"uv run gunicorn -k gevent -w {workers} -b 0.0.0.0:{port} run_prod:app"
    return run_command(
        command,
        f"Starting production server (gevent, {workers} workers - Unix only)",
        env,
    )


def run_production_waitress(port: int = 8000) -> bool:
    """Run the application in production mode with Waitress (cross-platform)."""
    # Set environment variables for the subprocess
    env = os.environ.copy()
    if not env.get("DATABASE_URL"):
        env["DATABASE_URL"] = DEFAULT_DATABASE_URL
    if not env.get("SECRET_KEY"):
        # Generate a random secret key for development - NOT for production!
        import secrets

        env["SECRET_KEY"] = secrets.token_hex(32)
        print(f"SECRET_KEY: {env['SECRET_KEY']}")
        print(SECRET_KEY_WARNING)
    if not env.get("FLASK_ENV"):
        env["FLASK_ENV"] = "production"

    command = f"uv run waitress-serve --host=0.0.0.0 --port={port} run_prod:app"
    return run_command(
        command, "Starting production server (Waitress - cross-platform)", env
    )


def main():
    """Main deployment script entry point."""
    parser = argparse.ArgumentParser(
        description="Deploy Part Management System backend"
    )
    parser.add_argument(
        "mode",
        choices=[
            "dev",
            "prod-multi",
            "prod-waitress",
            "prod-eventlet",
            "prod-gevent",
            "install",
        ],
        help="Deployment mode",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of workers for multi-worker modes (default: 4)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000 for prod, 5000 for dev)",
    )

    args = parser.parse_args()

    # Set default port based on mode
    if args.mode == "dev" and args.port == 8000:
        args.port = 5000

    print("DEPLOY: Part Management System Backend Deployment")
    print(f"   Mode: {args.mode}")
    print(f"   Port: {args.port}")
    if args.mode in ["prod-multi", "prod-gevent"]:
        print(f"   Workers: {args.workers}")
    print()

    # Check uv installation
    if not check_uv():
        print("ERROR: uv package manager is required but not installed.")
        print("   Install uv from: https://github.com/astral-sh/uv")
        sys.exit(1)

    # Install dependencies for all modes except dev (if already running)
    if args.mode != "dev" and not install_dependencies():
        print("ERROR: Failed to install dependencies")
        sys.exit(1)

    # Execute the requested mode
    success = False

    if args.mode == "install":
        success = install_dependencies()
    elif args.mode == "dev":
        success = run_development()
    elif args.mode == "prod-multi":
        success = run_production_multiworker(args.workers, args.port)
    elif args.mode == "prod-waitress":
        success = run_production_waitress(args.port)
    elif args.mode == "prod-eventlet":
        success = run_production_eventlet(args.port)
    elif args.mode == "prod-gevent":
        success = run_production_gevent(args.workers, args.port)

    if success:
        print("SUCCESS: Deployment completed successfully!")
    else:
        print("FAILED: Deployment failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
