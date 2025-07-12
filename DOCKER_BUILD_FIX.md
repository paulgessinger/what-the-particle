# Docker Build Fix - uv.lock Issue

## Problem
The Docker build was failing with this error:

```
> [python-base 8/9] RUN uv sync --frozen:
0.247 Using CPython 3.11.13 interpreter at: /usr/local/bin/python3
0.247 Creating virtual environment at: .venv
0.249 error: Unable to find lockfile at `uv.lock`. To create a lockfile, run `uv lock` or `uv sync`.
------
ERROR: failed to build: failed to solve: process "/bin/sh -c uv sync --frozen" did not complete successfully: exit code: 2
```

## Root Cause
The `uv.lock` file exists in the repository (177KB, already committed) but was not being copied to the Docker container before running `uv sync --frozen`.

The `--frozen` flag requires the lockfile to be present to ensure reproducible builds with exact dependency versions.

## Solution Applied

### Before (❌ Broken):
```dockerfile
# Copy Python configuration files
COPY pyproject.toml ./
COPY README.md ./

# Copy backend source code
COPY backend ./backend

# Install Python dependencies using uv
RUN uv sync --frozen  # ❌ Fails - no uv.lock file available
```

### After (✅ Fixed):
```dockerfile
# Copy Python configuration files
COPY pyproject.toml ./
COPY uv.lock ./       # ✅ Added this line
COPY README.md ./

# Copy backend source code
COPY backend ./backend

# Install Python dependencies using uv
RUN uv sync --frozen  # ✅ Works - lockfile is available
```

## Verification

### File Status
- ✅ `uv.lock` exists in repository: `177KB file`
- ✅ `uv.lock` is tracked by git: `git ls-files | grep uv.lock`
- ✅ `uv.lock` is now copied to Docker container

### Docker Build Process
1. **Stage 1 (Frontend)**: ✅ Builds SvelteKit app
2. **Stage 2 (Python)**: ✅ Now copies `uv.lock` before `uv sync --frozen`
3. **Dependency Installation**: ✅ Uses exact versions from lockfile
4. **Final Image**: ✅ Contains both frontend and backend

## Benefits of This Fix

1. **Reproducible Builds**: `uv sync --frozen` ensures exact dependency versions
2. **Faster Builds**: uv can skip dependency resolution using the lockfile
3. **Security**: Prevents dependency confusion attacks by using locked versions
4. **Consistency**: Docker builds use same dependencies as local development

## Commit Details
```
commit 4a60649
Fix Docker build: Add uv.lock file to COPY command

The Docker build was failing because uv.lock was not being copied to the container,
causing 'uv sync --frozen' to fail. The uv.lock file is already committed to the
repository but wasn't being included in the Docker build context.
```

## Expected Docker Build Flow Now
```bash
# This should now work:
docker build -t particle-explorer .

# Build stages:
# 1. Frontend build (Node.js) → creates /app/frontend/build
# 2. Python setup → copies uv.lock and runs uv sync --frozen
# 3. Final image → combines frontend build + Python backend
```

The Docker build should now complete successfully without the uv.lock error.