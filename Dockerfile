# FROM nginx:latest
# FROM lipanski/docker-static-website:latest
FROM httpd:2.4

MAINTAINER Christoph Fluegel <docker@flgl.tech>
ARG VERSION
ENV VERSION $VERSION

# COPY pelican/output/ /usr/share/nginx/html/
# COPY pelican/output/ . 
COPY pelican/output/ /usr/local/apache2/htdocs
