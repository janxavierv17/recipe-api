#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Substitute environment variables into the Nginx configuration template
# and save the result to the Nginx configuration directory
envsubst </etc/nginx/default.conf.tpl >/etc/nginx/conf.d/default.conf

# Start Nginx in the foreground
nginx -g 'daemon off;'
