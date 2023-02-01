FROM alpine:latest

# Install python/pip and other requirements
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install requests flask

# Copy the script file into the container
COPY docker_getPythonSongs.py .

# Make the script executable
RUN chmod +x docker_getPythonSongs.py

# Docker service should run on port 80
EXPOSE 80 

CMD ["python3","docker_getPythonSongs.py"]
root@ubuntu2004:~/getLyrics# 
