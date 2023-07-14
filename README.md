certbot-dns-godaddy
==================

[![Version](https://img.shields.io/pypi/v/certbot-dns-godaddy.svg)](https://pypi.python.org/pypi/certbot-dns-godaddy) [![License: Apache](https://img.shields.io/pypi/l/certbot-dns-godaddy.svg)](https://github.com/miigotu/certbot-dns-godaddy/blob/master/LICENSE.txt) [![Docker image size](https://img.shields.io/docker/image-size/miigotu/certbot-dns-godaddy)](https://hub.docker.com/repository/docker/miigotu/certbot-dns-godaddy)

[godaddy](https://www.godaddy.com/) DNS Authenticator plugin for [certbot](https://certbot.eff.org/).

This plugin automates the process of completing a `dns-01` challenge by creating, and subsequently removing, `TXT` records using the godaddy [API](https://developer.godaddy.com/doc/endpoint/domains) via [lexicon](https://github.com/AnalogJ/lexicon).

**Note:** This manual assumes certbot ≥ v1.7, which has improved the naming scheme for external plugins. If you cannot upgrade, please also refer to the Old option naming scheme\_ section below.

Installation
------------

    pip install certbot-dns-godaddy

Named Arguments
---------------

To start using DNS authentication for godaddy, pass the following arguments on certbot's command line:

Option|Description|
---|---|
`--authenticator dns-godaddy`|select the authenticator plugin (Required)|
`--dns-godaddy-credentials FILE`|godaddy credentials INI file. (Required)|
`--dns-godaddy-propagation-seconds NUM`|waiting time for DNS to propagate before asking the ACME server to verify the DNS record. (Default: 30, Recommended: \>= 600)|

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
        --dns-godaddy-credentials /var/lib/letsencrypt/godaddy_credentials.ini \
        --keep-until-expiring --non-interactive --expand \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --agree-tos --email "webmaster@example.com" \
        -d example.com -d '*.example.com'

You may want to change the volumes `/var/lib/letsencrypt` and `/etc/letsencrypt` to local directories where the certificates and configuration should be stored.

Old option naming scheme
------------------------

It is recommended to use the newest certbot version, at least `v1.7`.

If you're using a certbot version below `v1.7` all options related to external plugins (such as this one) must be prefixed by the name of the plugin. This means that every occurence of `dns-godaddy` in the command line options must be replaced by `certbot-dns-godaddy:dns-godaddy`, i.e.:

    --authenticator certbot-dns-godaddy:dns-godaddy
    --certbot-dns-godaddy:dns-godaddy-credentials
    --certbot-dns-godaddy:dns-godaddy-propagation-seconds

Further, every occurence of `dns_godaddy` in the config file must be prefixed by `certbot_dns_godaddy:`, resulting in a file like this:

``` {.sourceCode .ini}
certbot_dns_godaddy:dns_godaddy_key      = ...
certbot_dns_godaddy:dns_godaddy_secret = ...
```
