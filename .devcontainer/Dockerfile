# Base image for the NYU Lab development environment
FROM rofrano/pipeline-selenium:latest

# Set up the Python development environment
WORKDIR /app

# Copy dependencies
COPY pyproject.toml poetry.lock ./

# Install Python dependencies using Poetry
RUN sudo python -m pip install --upgrade pip poetry && \
    sudo poetry config virtualenvs.create false && \
    sudo poetry install

# Install user mode tools
COPY .devcontainer/scripts/install-tools.sh /tmp/
RUN cd /tmp && bash ./install-tools.sh

# Expose the application port
EXPOSE 8080

# Default command to start Gunicorn with the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]