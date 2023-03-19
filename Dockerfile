FROM python:3.11-alpine

# Install Python dependencies from Pipfile
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && \
    pipenv install --system --deploy

# Copy the rest of the application
COPY app /app

# Run the application
CMD ["python", "/app/app.py"]