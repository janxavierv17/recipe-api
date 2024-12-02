# Use the official Nginx image without root privileges for improved security
# https://hub.docker.com/r/nginxinc/nginx-unprivileged
FROM nginxinc/nginx-unprivileged:1-alpine

# Define the maintainer label for the image
LABEL maintainer = "Jan"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
# The port of our UWSGI
ENV APP_PORT=9000 

# Switch to the root user to perform privileged operations
USER root

# Run necessary setup commands:
# - Create a static file volume directory
# - Set the appropriate permissions for the static file directory
# - Create the default Nginx configuration file if it doesn't exist
# - Change ownership and permissions for the default Nginx config
# - Ensure the custom run.sh script is executable
RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

# Declare the volume for the static files directory
VOLUME /vol/static

# Switch back to the Nginx user for running the container, for security
USER nginx

CMD [ "/run.sh" ]