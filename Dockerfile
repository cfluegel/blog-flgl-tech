FROM lipanski/docker-static-website:latest
# FROM nginx:latest

MAINTAINER Christoph Fluegel <docker@flgl.tech>
ARG VERSION
ENV VERSION $VERSION

# COPY pelican/output/* /usr/share/nginx/html/
COPY pelican/output/* . 
