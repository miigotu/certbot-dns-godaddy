FROM certbot/certbot

COPY . src/certbot-dns-godaddy

RUN pip install -U pip
RUN pip install --no-cache-dir src/certbot-dns-godaddy

ENTRYPOINT ["/usr/bin/env"]
