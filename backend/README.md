# Part Management System - Backend

A Flask-based REST API backend for the Part Management System, providing comprehensive part lifecycle management through a clean, database-driven architecture.

## Features

- **RESTful API**: Complete CRUD operations for parts management with authentication
- **Database Integration**: SQLAlchemy ORM with SQLite (easily configurable for PostgreSQL/MySQL)
- **Part Lifecycle Management**: Support for review → CNC/Hand fabrication → completion workflow
- **Search & Filtering**: Advanced search across multiple fields with pagination
- **File Management**: STEP file upload, download, and automatic GLTF/GLB conversion for 3D visualization
- **Authentication**: API key-based authentication with rate limiting
- **Validation**: Comprehensive input validation and error handling
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Frontend Serving**: Built-in frontend static file serving for full-stack deployment
- **Development Data**: Automatic sample data initialization for development

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone and navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## Authentication

The API uses a secret key authentication system. All API endpoints (except health check) require authentication via one of these methods:

- **Header**: `X-API-Key: your-secret-key`
- **Query Parameter**: `?api_key=your-secret-key`
- **Request Body**: `{"api_key": "your-secret-key"}` (for POST/PUT requests)

The secret key is configured via the `SECRET_KEY` environment variable or `config.json` file.

## API Endpoints

### Parts Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/parts/` | Get all parts (with optional filtering) |
| POST | `/api/parts/` | Create a new part |
| GET | `/api/parts/<id>` | Get a specific part |
| PUT | `/api/parts/<id>` | Update a part |
| DELETE | `/api/parts/<id>` | Delete a part |

### Workflow Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/parts/<id>/approve` | Approve part for production |
| POST | `/api/parts/<id>/assign` | Assign part to user |
| POST | `/api/parts/<id>/unclaim` | Unclaim assigned part |
| POST | `/api/parts/<id>/complete` | Mark part as completed |
| POST | `/api/parts/<id>/revert` | Revert completed part |

### File Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/parts/<id>/upload` | Upload STEP file for a part |
| GET | `/api/parts/<id>/download` | Download original STEP file |
| GET | `/api/parts/<id>/model` | Get GLTF/GLB model for 3D visualization |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/parts/auth/check` | Check authentication status |

### Specialized Queries

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/parts/categories/<category>` | Get parts by category |
| GET | `/api/parts/stats` | Get system statistics |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check endpoint |

## File Management

The backend supports STEP file uploads for 3D part visualization. When a STEP file is uploaded:

1. The original STEP file is stored in the `uploads/` directory
2. The file is automatically converted to GLTF/GLB format using the `cascadio` library
3. The converted model can be accessed via the `/model` endpoint for 3D visualization

**Supported file formats**: `.step`, `.stp`

## Query Parameters

### GET /api/parts/

- `category`: Filter by category (`review`, `cnc`, `hand`, `completed`)
- `search`: Search across name, notes, subsystem, and assigned fields
- `sort_by`: Sort field (`name`, `status`, `assigned`, `created_at`)
- `sort_order`: Sort order (`asc`, `desc`)
- `limit`: Maximum results per page
- `offset`: Pagination offset

## Part Data Structure

```json
{
  "id": 1,
  "type": "cnc",
  "name": "Drive Gear",
  "subsystem": "Drive System",
  "assigned": "John Doe",
  "status": "In Progress",
  "notes": "Check tooth profile",
  "file": "gear.stl",
  "onshapeUrl": "https://...",
  "claimedDate": "2024-01-15T10:30:00Z",
  "category": "cnc",
  "createdAt": "2024-01-10T08:00:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

## Configuration

### Configuration File (config.json)

You can optionally create a `config.json` file in the backend directory to set configuration values. This file will be read by the deployment script and can be used instead of or alongside environment variables.

**Create configuration file:**
```bash
python create_config.py
```

**Example config.json:**
```json
{
  "DATABASE_URL": "sqlite:///parts_prod.db",
  "SECRET_KEY": "your-secure-secret-key-here",
  "FLASK_ENV": "production"
}
```

**Configuration precedence:** Environment Variables > config.json > Default Values

### Environment Variables

- `FLASK_ENV`: Environment (`development`, `testing`, `production`)
- `DATABASE_URL`: Database connection string (required in production)
- `SECRET_KEY`: API secret key for authentication (required, min 32 chars)
- `PORT`: Server port (default: 5000)
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)
- `BASE_PATH`: Base path for subpath deployments (e.g., `/part-management-system`)

### Configuration Classes

- `DevelopmentConfig`: Debug mode, SQLite database
- `TestingConfig`: Testing mode, separate test database
- `ProductionConfig`: Production settings

## Frontend Serving

The backend can serve the frontend static files directly, enabling full-stack deployment. When the backend receives requests for non-API routes, it serves the built frontend files from the `dist/` directory. This allows for:

- Single-server deployment
- Simplified hosting configuration
- Automatic routing for SPA applications

## Database

### Default Setup

- **Database**: SQLite (`parts.db` in development)
- **ORM**: SQLAlchemy
- **Migrations**: Automatic table creation

### Schema

The `Part` model includes:
- Primary key with auto-increment
- Indexed category field for performance
- Automatic timestamps (created_at, updated_at)
- Nullable fields for optional data
- Validation constraints

## Development

### Project Structure

```
backend/
├── app/                 # Flask application package
│   └── __init__.py     # Application factory
├── models/             # Database models
│   ├── __init__.py
│   └── part.py         # Part model
├── routes/             # API routes
│   ├── __init__.py
│   └── parts.py        # Parts API endpoints
├── utils/              # Utilities
│   ├── __init__.py
│   ├── auth.py         # Authentication utilities
│   ├── validation.py   # Data validation
│   └── step_converter.py # STEP to GLTF conversion
├── config.py           # Configuration
├── run.py             # Application entry point
├── requirements.txt    # Dependencies
└── README.md          # This file
```

### Adding New Features

1. **New Models**: Add to `models/` directory
2. **New Routes**: Add to `routes/` directory and register in `app/__init__.py`
3. **New Utilities**: Add to `utils/` directory
4. **Update Requirements**: Add new dependencies to `requirements.txt`

### Testing

```bash
# Set testing environment
export FLASK_ENV=testing

# Run tests (when implemented)
python -m pytest
```

## Deployment

### Production Setup with Gunicorn

For production deployment, use Gunicorn instead of the Flask development server for better performance, concurrency, and reliability.

#### Installation

Install production dependencies using uv (recommended for faster installs):
```bash
cd backend
uv pip install -r requirements.txt
```

#### Running with Gunicorn

**⚠️ Windows Compatibility Note:** Gunicorn has limited Windows support. For Windows deployment, consider using:
- Docker containers (recommended)
- Windows Services with Waitress
- IIS with wfastcgi
- Alternative ASGI servers like Uvicorn

Choose one of the following deployment options:

**Multi-worker setup (Linux/macOS only - not fully Windows compatible):**
```bash
uv run gunicorn -w 4 -b 0.0.0.0:8000 run_prod:app
```
- `-w 4`: 4 worker processes (adjust based on CPU cores)
- `-b 0.0.0.0:8000`: Bind to all interfaces on port 8000
- ❌ **Limited Windows Support**: May not work reliably on Windows

**Eventlet async setup (Linux/macOS only):**
```bash
uv run gunicorn -k eventlet -w 1 -b 0.0.0.0:8000 run_prod:app
```
- `-k eventlet`: Use eventlet worker class for async support
- `-w 1`: Single worker (eventlet handles concurrency internally)
- ❌ **Not Windows Compatible**: Requires Unix-like systems

**Gevent async setup (Linux/macOS only):**
```bash
uv run gunicorn -k gevent -w 4 -b 0.0.0.0:8000 run_prod:app
```
- `-k gevent`: Use gevent worker class for async support
- ❌ **Not Windows Compatible**: Requires Unix-like systems

#### Windows Alternative: Waitress WSGI Server

For Windows production deployment, use Waitress instead of Gunicorn:

```bash
# Run with Waitress (cross-platform)
uv run waitress-serve --host=0.0.0.0 --port=8000 run_prod:app
```

Or use the deployment script (automatically sets required environment variables and reads config.json):
```bash
# Using the deploy script (recommended - handles environment variables and config.json)
uv run python deploy.py prod-waitress --port 8000
```

**Configuration:**
The deployment script automatically sets configuration values with this precedence:
1. Environment variables (highest priority)
2. Values from `config.json` file
3. Auto-generated defaults (lowest priority)

- `DATABASE_URL=sqlite:///parts_prod.db` (if not set in env or config.json)
- `SECRET_KEY` (auto-generated if not set in env or config.json - shows warning)
- `FLASK_ENV=production` (if not set in env or config.json)

**⚠️ Security Warning:** The deployment script generates a random SECRET_KEY for convenience, but you should set your own secure SECRET_KEY in production.

For custom settings, set environment variables before running:
```bash
# Windows PowerShell
$env:DATABASE_URL="postgresql://user:pass@localhost/parts_prod"
$env:SECRET_KEY="your-secure-production-secret-key-here"
uv run python deploy.py prod-waitress --port 8000

# Or Linux/bash
DATABASE_URL="postgresql://user:pass@localhost/parts_prod" \
SECRET_KEY="your-secure-production-secret-key-here" \
uv run python deploy.py prod-waitress --port 8000
```

**Required Production Environment Variables:**
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secure random key for Flask sessions/cookies (min 32 characters recommended)

#### Environment Variables for Production

Set these environment variables in your production environment:
```bash
export FLASK_ENV=production
export DATABASE_URL="postgresql://user:password@localhost/parts_db"
export SECRET_KEY="your-secure-secret-key"
export CORS_ORIGINS="https://yourdomain.com"
```

### Production Considerations

1. **Database**: Use PostgreSQL or MySQL in production
2. **Environment Variables**: Set all required environment variables
3. **WSGI Server**: Use Gunicorn (configured above) instead of Flask dev server
4. **Reverse Proxy**: Configure Nginx or Apache as reverse proxy
5. **SSL/TLS**: Enable HTTPS in production
6. **Process Management**: Use systemd, supervisor, or Docker for process management

### Docker Example

```dockerfile
FROM python:3.9-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY . .
EXPOSE 8000

# Use Waitress for cross-platform compatibility (works on Windows too)
CMD ["uv", "run", "waitress-serve", "--host=0.0.0.0", "--port=8000", "run_prod:app"]
```

## API Documentation

For detailed API documentation, the backend provides OpenAPI/Swagger documentation at `/api/docs` (when implemented with Flask-RESTX or similar).

## Contributing

1. Follow the existing code style and structure
2. Add comprehensive docstrings to new functions
3. Include input validation for new endpoints
4. Update this README for significant changes
5. Test thoroughly before submitting changes

## License

This project is part of the Part Management System. See the main project README for license information.
