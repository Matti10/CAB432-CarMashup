############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu – by default here the latest version
############################################################
# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Mattias Winsen (n10467874)

# Install basic applications, Python, Python tools
RUN apt-get update
RUN apt-get install -y \
 build-essential \
 curl \
 dialog \
 git \
 net-tools \
 python3 \
 python3-dev \
 python3-setuptools \
 python-distribute \
 python3-pip \
 tar \
 wget
 
# Get pip3 to download and install Python requirements:
RUN pip3 install flask
RUN pip3 install cherrypy
RUN pip3 install Flask-Bootstrap4
RUN pip3 install Flask-WTF
RUN pip install requests
RUN pip install wtforms
RUN pip install wtforms
RUN pip install google-search
RUN pip install google-search-results
RUN pip install boto3

# Copy the application folder inside the container
ADD /app /app
# Expose ports
EXPOSE 80
# Set the default directory where CMD will execute
WORKDIR /app

# Set the default command to execute when creating a new container
# i.e. using CherryPy to serve the application
CMD python3 server.py