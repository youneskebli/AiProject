FROM python:3.10

EXPOSE 8501

WORKDIR /app

# Install build tools and dependencies, including HDF5 libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    dbus \
    libhdf5-dev

# Pre-install Cython
RUN pip install Cython==0.29.21

# Copy the requirements file into the container
COPY requirements.txt ./requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

# Install remaining dependencies
RUN pip install -r requirements.txt

# Install specific version of click
RUN pip install click==8.0.0

RUN pip install tornado==6.1


# Copy the rest of the application code
COPY . .

# Set environment variable
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Run the application
CMD ["streamlit", "run", "app.py"]
