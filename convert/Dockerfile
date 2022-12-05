FROM gcr.io/google-appengine/python

# Sets the user name to use when running the image.
USER root
RUN apt update
RUN apt install -y ffmpeg

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
# Use -p python3 or -p python3.7 to select python version. Default is version 2.
RUN virtualenv /env

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Copy source code
COPY . .

# Run the application
CMD ["python3", "app.py"]