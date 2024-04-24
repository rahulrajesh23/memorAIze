FROM python:3.10

# Set the working directory to /backend in the container
WORKDIR /backend

# Copy the current directory contents into the container at /backend
COPY ./app /backend/app
COPY ./static /backend/static
COPY requirements.txt /backend/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MODULE_NAME="app.main"
ENV VARIABLE_NAME="app"
ENV PORT=8000

# Run the app when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


