# Development Guide

This guide will help you set up your development environment and understand the project structure.

## Table of Contents

- [Setup](#setup)
- [Project Structure](#project-structure)
- [Frontend Development](#frontend-development)
- [Backend Development](#backend-development)
- [Testing](#testing)
- [Debugging](#debugging)
- [Best Practices](#best-practices)

## Setup

### Prerequisites

- Node.js 18+ and npm 9+
- Python 3.11+
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/agentforge/agentforge.git
cd agentforge

# Install dependencies
./install-deps.sh  # or run manually:
# cd backend && pip install -r requirements.txt
# cd frontend && npm install

# Start development servers
./start-dev.sh
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
agentforge/
├── backend/                      # FastAPI application
│   ├── api/                      # API routes
│   │   └── routes/
│   │       ├── auth.py           # Authentication
│   │       ├── workflows.py      # Workflow management
│   │       ├── agents.py         # Agent operations
│   │       └── ...
│   ├── auth/                     # Authentication & security
│   │   ├── security.py           # Password hashing, JWT
│   │   └── dependencies.py       # FastAPI dependencies
│   ├── middleware/               # Request/response middleware
│   ├── exceptions/               # Custom exceptions
│   ├── schemas/                  # Pydantic models
│   ├── database/                 # SQLAlchemy models
│   ├── agents/                   # AI agent implementations
│   ├── core/                     # Configuration
│   └── main.py                   # FastAPI app entry point
│
├── frontend/                     # React + Vite application
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/               # UI components
│   │   │   ├── enterprise/       # Business components
│   │   │   ├── layout/           # Layout components
│   │   │   └── forms/            # Form components
│   │   ├── hooks/                # Custom React hooks
│   │   ├── types/                # TypeScript types
│   │   ├── utils/                # Utilities
│   │   │   ├── api.ts            # API client
│   │   │   └── helpers.ts        # Helper functions
│   │   ├── App.tsx               # Root component
│   │   └── main.tsx              # Entry point
│   └── package.json
│
└── docs/                         # Documentation
```

## Frontend Development

### Creating Components

1. **Create component file** in appropriate directory:
   ```bash
   # UI Component
   frontend/src/components/ui/MyButton.tsx
   
   # Business Component
   frontend/src/components/enterprise/WorkflowCard.tsx
   ```

2. **Implement component** with TypeScript:
   ```typescript
   import React from 'react'
   import { cn } from '../../utils/helpers'
   
   interface MyButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
     variant?: 'primary' | 'secondary'
   }
   
   export const MyButton = React.forwardRef<HTMLButtonElement, MyButtonProps>(
     ({ variant = 'primary', className, ...props }, ref) => {
       return (
         <button
           ref={ref}
           className={cn('btn', `btn-${variant}`, className)}
           {...props}
         />
       )
     }
   )
   
   MyButton.displayName = 'MyButton'
   ```

3. **Export from index**:
   ```typescript
   // components/ui/index.ts
   export { MyButton } from './MyButton'
   ```

### Using Hooks

```typescript
import { useAsync, useForm, useLocalStorage } from '../../hooks/useAsync'
import { api } from '../../utils/api'

export function MyComponent() {
  // Async operations
  const { data, loading, error, execute } = useAsync(
    async () => api.workflows.list()
  )
  
  // Form handling
  const { values, handleChange, handleSubmit } = useForm(
    { name: '' },
    async (values) => {
      await api.workflows.create(values)
    }
  )
  
  // Local storage
  const [user, setUser] = useLocalStorage('user', null)
}
```

### Styling

- Use Tailwind CSS utilities for most styling
- Component-specific styles in component file using `className`
- Dark theme (#0a0a0f) is default
- Color palette: Indigo, Violet, Cyan

### API Integration

```typescript
import { api } from '../../utils/api'
import { useApiQuery, useApiMutation } from '../../hooks/useAsync'

// Query data
const { data, isLoading } = useApiQuery(
  ['workflows'],
  () => api.workflows.list()
)

// Mutate data
const { mutate, isPending } = useApiMutation(
  (data) => api.workflows.create(data)
)
```

## Backend Development

### Creating API Routes

1. **Create route file** in `api/routes/`:
   ```python
   # backend/api/routes/my_feature.py
   from fastapi import APIRouter, Depends, HTTPException
   from backend.schemas.base import SuccessResponse, MySchema
   from backend.auth.dependencies import get_current_user
   
   router = APIRouter(prefix="/my-feature", tags=["my-feature"])
   
   @router.get("/", response_model=SuccessResponse[list[MySchema]])
   async def list_items(current_user: dict = Depends(get_current_user)):
       """List all items for current user."""
       return SuccessResponse(data=[])
   ```

2. **Define schemas** in `schemas/base.py`:
   ```python
   from pydantic import BaseModel, Field
   
   class MySchema(BaseModel):
       id: str
       name: str = Field(min_length=1, max_length=255)
       description: Optional[str] = None
   ```

3. **Register route** in `main.py`:
   ```python
   from backend.api.routes.my_feature import router as my_router
   
   app.include_router(my_router, prefix=settings.api_prefix)
   ```

### Error Handling

```python
from backend.exceptions.handlers import (
    AppException, ValidationError, NotFoundError, ForbiddenError
)

@router.get("/{id}")
async def get_item(id: str):
    if not id:
        raise ValidationError("ID cannot be empty")
    
    item = await db.get_item(id)
    if not item:
        raise NotFoundError("Item", id)
    
    if not can_access(item, current_user):
        raise ForbiddenError("You cannot access this item")
    
    return item
```

### Database Operations

```python
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import Workflow

@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str, db: AsyncSession = Depends(get_db)):
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise NotFoundError("Workflow", workflow_id)
    return workflow
```

## Testing

### Backend Testing

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=backend tests/

# Run with verbose output
pytest -v
```

### Writing Tests

```python
# tests/test_workflows.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_list_workflows():
    response = client.get("/api/v1/workflows")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)

def test_create_workflow():
    response = client.post(
        "/api/v1/workflows",
        json={"name": "My Workflow"}
    )
    assert response.status_code == 201
```

### Frontend Testing

```bash
cd frontend

# Run tests
npm test

# With coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

## Debugging

### Backend Debugging

```bash
# Using print statements
print(f"Debug: {variable}")

# Using pdb
python -m pdb -m uvicorn backend.main:app

# Enable debug logging
LOG_LEVEL=DEBUG uvicorn backend.main:app --reload
```

### Frontend Debugging

- Open browser DevTools (F12)
- Use React DevTools extension
- Add breakpoints in Sources tab
- Use `console.log()` for quick debugging

## Best Practices

### General

- Write meaningful commit messages
- Keep functions focused and small
- Use type hints and docstrings
- Write tests for new features
- Review code before committing

### Python

- Follow PEP 8
- Use async/await for I/O operations
- Use context managers for resource management
- Validate input with Pydantic
- Use logging instead of print

### TypeScript/React

- Use functional components with hooks
- Memoize expensive components
- Keep state management simple
- Use React Query for API calls
- Type everything explicitly

### Database

- Use transactions for related operations
- Index frequently queried columns
- Optimize N+1 queries
- Use connection pooling in production

---

For more information, see the main [README.md](README.md).
