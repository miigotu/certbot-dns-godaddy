ARG VERSION=v2.6.0
FROM certbot/certbot:$VERSION

LABEL org.opencontainers.image.source="https://github.com/miigotu/certbot-dns-godaddy"
LABEL maintainer="miigotu@gmail.com"
ENV PYTHONIOENCODING="UTF-8"

COPY . src/certbot-dns-godaddy

RUN pip install -U pip
RUN pip install --no-cache-dir src/certbot-dns-godaddy

ENTRYPOINT ["/usr/bin/env"]
