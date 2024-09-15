# Stage 1: Build the frontend
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the backend
FROM python:3.11 AS backend-build
WORKDIR /app/backend
COPY backend/pyproject.toml backend/poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi
COPY backend/ ./

# Stage 3: Final stage
FROM python:3.11-slim
WORKDIR /app

# Copy backend from backend-build stage
COPY --from=backend-build /app/backend /app/backend
COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-build /usr/local/bin /usr/local/bin

# Copy frontend build from frontend-build stage
COPY --from=frontend-build /app/frontend/build /app/frontend/build

# Install uvicorn for running the FastAPI app
RUN pip install uvicorn

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]