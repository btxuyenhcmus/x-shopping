# Pull base image
FROM python:3.7

# Set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /x-shopping

# Install dependencies
COPY requirements.txt /x-shopping/
RUN pip3 install -r requirements.txt

# Copy project
COPY . /x-shopping/

# Running project
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
