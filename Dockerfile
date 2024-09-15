# Stage 1: Build the frontend
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the backend
FROM public.ecr.aws/lambda/python:3.11 AS backend-build
WORKDIR /app/backend
COPY backend/pyproject.toml backend/poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi
COPY backend/ ./

# Stage 3: Final stage
FROM public.ecr.aws/lambda/python:3.11
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy backend from backend-build stage
COPY --from=backend-build /app/backend ${LAMBDA_TASK_ROOT}
COPY --from=backend-build /var/lang/lib/python3.11/site-packages ${LAMBDA_TASK_ROOT}

# Copy frontend build from frontend-build stage
COPY --from=frontend-build /app/frontend/build ${LAMBDA_TASK_ROOT}/frontend/build

# Install additional dependencies
RUN pip install mangum

# Copy the Lambda handler
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "lambda_handler.handler" ]