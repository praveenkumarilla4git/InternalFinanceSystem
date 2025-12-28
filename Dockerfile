# 1. Start with a pre-built "Base Image" that has Python installed
# We use 'slim' because it is small and fast
FROM python:3.10-slim

# 2. Create a working folder inside the container
# Think of this like: "cd /app"
WORKDIR /app

# 3. Copy our "requirements.txt" first
COPY requirements.txt .

# 4. Install the dependencies (Flask) inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of our code (main.py, templates, etc.) into the container
COPY . .

# 6. Initialize the database inside the container
# We run schema.py so the container creates its own finance.db
RUN python schema.py

# 7. Tell the container to listen on port 5000
EXPOSE 5000

# 8. The command to run when the container starts
CMD ["python", "main.py"]