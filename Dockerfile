# 1. Use Python 3.13.7 base image
FROM python:3.13.7-slim

# 2. Set working directory inside the container
#    Any relative COPY or commands will use this path.
WORKDIR /app

# 3. Copy only requirements first (better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project
#    ✅ Option A (used below): Copies into current WORKDIR (/app)
COPY . .

#    ✅ Option B (also valid, same result as above):
#    COPY . /app
#    (Both work because WORKDIR is already /app)

# 6. Expose the port your app runs on
#    In your old file, EXPOSE $PORT was used (for platforms like Heroku).
#    Since you're not using $PORT, we use a fixed value (5000).
EXPOSE 5000

# 7. Run the app with Gunicorn
#    Old version: app:app  ❌ (wrong path based on your folder structure)
#    Correct version:
#    folder.filename:app_object
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app.app:app"]
