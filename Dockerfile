FROM certbot/certbot
LABEL org.opencontainers.image.source="https://github.com/miigotu/certbot-dns-godaddy"
LABEL maintainer="miigotu@gmail.com"
ENV PYTHONIOENCODING="UTF-8"

COPY . src/certbot-dns-godaddy

RUN pip install -U pip
RUN pip install --no-cache-dir --use-feature=in-tree-build src/certbot-dns-godaddy

ENTRYPOINT ["/usr/bin/env"]
