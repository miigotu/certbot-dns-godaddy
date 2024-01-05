certbot-dns-godaddy
==================

[![Version](https://img.shields.io/pypi/v/certbot-dns-godaddy.svg)](https://pypi.python.org/pypi/certbot-dns-godaddy) [![License: Apache](https://img.shields.io/pypi/l/certbot-dns-godaddy.svg)](https://github.com/miigotu/certbot-dns-godaddy/blob/master/LICENSE.txt) [![Docker image size](https://img.shields.io/docker/image-size/miigotu/certbot-dns-godaddy)](https://hub.docker.com/repository/docker/miigotu/certbot-dns-godaddy)

[godaddy](https://www.godaddy.com/) DNS Authenticator plugin for [certbot](https://certbot.eff.org/).

This plugin automates the process of completing a `dns-01` challenge by creating, and subsequently removing, `TXT` records using the godaddy [API](https://developer.godaddy.com/doc/endpoint/domains) via [lexicon](https://github.com/AnalogJ/lexicon).

**Note:** This manual assumes certbot >=2.7.4 which has improved the naming scheme for external plugins.

Installation
------------

    # create a virtual environment, to avoid conflicts
    python3 -m venv /some/path

    # use the pip in the virtual environment to install or update
    /some/path/bin/pip install -U certbot-dns-godaddy

    # yse the cerbot from the virtualenv, to avoid accidentally
    # using one from a different environment that does not have this library
    /some/path/bin/certbot

Named Arguments
---------------

To start using DNS authentication for godaddy, pass the following arguments on certbot's command line:

| Option                                  | Description                                                                           |
|-----------------------------------------|---------------------------------------------------------------------------------------|
| `--authenticator dns-godaddy`           | select the authenticator plugin (Required)                                            |
| `--dns-godaddy-credentials FILE`        | godaddy credentials INI file. (Required)                                              |
| `--dns-godaddy-propagation-seconds NUM` | how long to wait before ACME tries to verify DNS. (Default: 30, Recommended: \>= 600) |
| `--dns-godaddy-ttl NUM`  | TTL for TXT record. (Default 600. For WildCard >= 600 )

You may need to set an unexpectedly high propagation time (≥ 900 seconds) to give the godaddy DNS time to propagate the entries! This may be annoying when calling certbot manually but should not be a problem in automated setups.

Credentials
-----------

Use of this plugin requires a configuration file containing godaddy API credentials, obtained from your [developer.godaddy.com](https://developer.godaddy.com/).

An example `credentials.ini` file:

``` {.sourceCode .ini}
dns_godaddy_secret      = 0123456789abcdef0123456789abcdef01234567
dns_godaddy_key = abcdef0123456789abcdef01234567abcdef0123
```

The path to this file can be provided interactively or using the `--dns-godaddy-credentials` command-line argument. Certbot records the path to this file for use during renewal, but does not store the file's contents.

**CAUTION:** You should protect these API credentials as you would the password to your godaddy account. Users who can read this file can use these credentials to issue arbitrary API calls on your behalf. Users who can cause Certbot to run using these credentials can complete a `dns-01` challenge to acquire new certificates or revoke existing certificates for associated domains, even if those domains aren't being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be accessed by other users on your system. The warning reads "Unsafe permissions on credentials configuration file", followed by the path to the credentials file. This warning will be emitted each time Certbot uses the credentials file, including for renewal, and cannot be silenced except by addressing the issue (e.g., by using a command like `chmod 600` to restrict access to the file).

Examples
--------

To acquire a single certificate for both `example.com` and `*.example.com`, waiting 900 seconds for DNS propagation:

    certbot certonly \\
      --authenticator dns-godaddy \\
      --dns-godaddy-credentials ~/.secrets/certbot/godaddy.ini \\
      --dns-godaddy-propagation-seconds 900 \\
      --dns-godaddy-ttl 600 \\
      --keep-until-expiring --non-interactive --expand \
      --server https://acme-v02.api.letsencrypt.org/directory \
      -d 'example.com' \\
      -d '*.example.com'

Docker
------

You can build a docker image from source using the included `Dockerfile` or pull the latest version directly from Docker Hub:

    docker pull miigotu/certbot-dns-godaddy

Once that's finished, the application can be run as follows:

    docker run --rm \
      -v /var/lib/letsencrypt:/var/lib/letsencrypt \
      -v /etc/letsencrypt:/etc/letsencrypt \
      --cap-drop=all \
      miigotu/certbot-dns-godaddy certbot certonly \
        --authenticator dns-godaddy \
        --dns-godaddy-propagation-seconds 900 \
        --dns-godaddy-ttl 600 \
        --dns-godaddy-credentials /var/lib/letsencrypt/godaddy_credentials.ini \
        --keep-until-expiring --non-interactive --expand \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --agree-tos --email "webmaster@example.com" \
        -d example.com -d '*.example.com'

You may want to change the volumes `/var/lib/letsencrypt` and `/etc/letsencrypt` to local directories where the certificates and configuration should be stored.

Exception
---------

If receives error like invalid argument `dns-godaddy-ttl`. Goto `/etc/letsencrypt/renewal/[YOURDOMAIN].conf` and edit file and in the end add `dns_godaddy_ttl = 600`. This is required once and then subssequent requests will not fail