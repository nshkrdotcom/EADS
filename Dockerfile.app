# Dockerfile.app

FROM python:3.9-slim-buster  # Or a suitable Python base image

WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for database connections (replace with your actual credentials). Best practice to inject credentials at run time so not stored in image.
# ENV PG_CONN_STR "...."  # Better to pass these at runtime
# ENV NEO4J_URI "...."
# ENV NEO4J_USERNAME "..."
# ENV NEO4J_PASSWORD "..."


# Expose port (if needed - depends on how your app runs)
# EXPOSE 5000  # Or your application's port

# Run your application
CMD ["python", "run_pipeline.py", "input.pdf", "output.tex"]  # Replace with your actual command. Pass in PDF and output filenames or make them configurable.
# CMD ["python", "run_pipeline.py", "/app/input/your_input.pdf", "/app/output/output.tex"]  #  Example - 

## OR 


ENTRYPOINT ["python", "run_pipeline.py"]
CMD ["/app/input/your_input.pdf", "/app/output/output.tex"] # Example – now you can override the command at runtime
