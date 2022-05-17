# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['certbot_dns_godaddy']
install_requires = \
['acme>=0.31.0',
 'certbot>=0.31.0',
 'dns-lexicon>=3.2.3',
 'urllib3>=1.26.4,<2.0.0',
 'zope.interface>=5.4.0']

entry_points = \
{'certbot.plugins': ['dns-godaddy = certbot_dns_godaddy:Authenticator']}

setup_kwargs = {
    'name': 'certbot-dns-godaddy',
    'version': '0.2.2',
    'description': 'A certbot plugin that implements letsencrypt dns wildcard support for godaddy using lexicon',
    'long_description': 'certbot-dns-godaddy\n==================\n\n[![Version](https://img.shields.io/pypi/v/certbot-dns-godaddy.svg)](https://pypi.python.org/pypi/certbot-dns-godaddy) [![License: Apache](https://img.shields.io/pypi/l/certbot-dns-godaddy.svg)](https://github.com/miigotu/certbot-dns-godaddy/blob/master/LICENSE.txt) [![Docker image size](https://img.shields.io/docker/image-size/miigotu/certbot-dns-godaddy)](https://hub.docker.com/repository/docker/miigotu/certbot-dns-godaddy)\n\n[godaddy](https://www.godaddy.com/) DNS Authenticator plugin for [certbot](https://certbot.eff.org/).\n\nThis plugin automates the process of completing a `dns-01` challenge by creating, and subsequently removing, `TXT` records using the godaddy [API](https://developer.godaddy.com/doc/endpoint/domains) via [lexicon](https://github.com/AnalogJ/lexicon).\n\n**Note:** This manual assumes certbot ≥ v1.7, which has improved the naming scheme for external plugins. If you cannot upgrade, please also refer to the Old option naming scheme\\_ section below.\n\nInstallation\n------------\n\n    pip install certbot-dns-godaddy\n\nNamed Arguments\n---------------\n\nTo start using DNS authentication for godaddy, pass the following arguments on certbot\'s command line:\n\nOption|Description|\n---|---|\n`--authenticator dns-godaddy`|select the authenticator plugin (Required)|\n`--dns-godaddy-credentials FILE`|godaddy credentials INI file. (Required)|\n`--dns-godaddy-propagation-seconds NUM`|waiting time for DNS to propagate before asking the ACME server to verify the DNS record. (Default: 30, Recommended: \\>= 600)|\n\nYou may need to set an unexpectedly high propagation time (≥ 900 seconds) to give the godaddy DNS time to propagate the entries! This may be annoying when calling certbot manually but should not be a problem in automated setups.\n\nCredentials\n-----------\n\nUse of this plugin requires a configuration file containing godaddy API credentials, obtained from your [developer.godaddy.com](developer.godaddy.com).\n\nAn example `credentials.ini` file:\n\n``` {.sourceCode .ini}\ndns_godaddy_secret      = 0123456789abcdef0123456789abcdef01234567\ndns_godaddy_key = abcdef0123456789abcdef01234567abcdef0123\n```\n\nThe path to this file can be provided interactively or using the `--dns-godaddy-credentials` command-line argument. Certbot records the path to this file for use during renewal, but does not store the file\'s contents.\n\n**CAUTION:** You should protect these API credentials as you would the password to your godaddy account. Users who can read this file can use these credentials to issue arbitrary API calls on your behalf. Users who can cause Certbot to run using these credentials can complete a `dns-01` challenge to acquire new certificates or revoke existing certificates for associated domains, even if those domains aren\'t being managed by this server.\n\nCertbot will emit a warning if it detects that the credentials file can be accessed by other users on your system. The warning reads "Unsafe permissions on credentials configuration file", followed by the path to the credentials file. This warning will be emitted each time Certbot uses the credentials file, including for renewal, and cannot be silenced except by addressing the issue (e.g., by using a command like `chmod 600` to restrict access to the file).\n\nExamples\n--------\n\nTo acquire a single certificate for both `example.com` and `*.example.com`, waiting 900 seconds for DNS propagation:\n\n    certbot certonly \\\\\n      --authenticator dns-godaddy \\\\\n      --dns-godaddy-credentials ~/.secrets/certbot/godaddy.ini \\\\\n      --dns-godaddy-propagation-seconds 900 \\\\\n      --keep-until-expiring --non-interactive --expand \\\n      --server https://acme-v02.api.letsencrypt.org/directory \\\n      -d \'example.com\' \\\\\n      -d \'*.example.com\'\n\nDocker\n------\n\nYou can build a docker image from source using the included `Dockerfile` or pull the latest version directly from Docker Hub:\n\n    docker pull miigotu/certbot-dns-godaddy\n\nOnce that\'s finished, the application can be run as follows:\n\n    docker run --rm \\\n      -v /var/lib/letsencrypt:/var/lib/letsencrypt \\\n      -v /etc/letsencrypt:/etc/letsencrypt \\\n      --cap-drop=all \\\n      miigotu/certbot-dns-godaddy certbot certonly \\\n        --authenticator dns-godaddy \\\n        --dns-godaddy-propagation-seconds 900 \\\n        --dns-godaddy-credentials /var/lib/letsencrypt/godaddy_credentials.ini \\\n        --keep-until-expiring --non-interactive --expand \\\n        --server https://acme-v02.api.letsencrypt.org/directory \\\n        --agree-tos --email "webmaster@example.com" \\\n        -d example.com -d \'*.example.com\'\n\nYou may want to change the volumes `/var/lib/letsencrypt` and `/etc/letsencrypt` to local directories where the certificates and configuration should be stored.\n\nOld option naming scheme\n------------------------\n\nIt is recommended to use the newest certbot version, at least `v1.7`.\n\nIf you\'re using a certbot version below `v1.7` all options related to external plugins (such as this one) must be prefixed by the name of the plugin. This means that every occurence of `dns-godaddy` in the command line options must be replaced by `certbot-dns-godaddy:dns-godaddy`, i.e.:\n\n    --authenticator certbot-dns-godaddy:dns-godaddy\n    --certbot-dns-godaddy:dns-godaddy-credentials\n    --certbot-dns-godaddy:dns-godaddy-propagation-seconds\n\nFurther, every occurence of `dns_godaddy` in the config file must be prefixed by `certbot_dns_godaddy:`, resulting in a file like this:\n\n``` {.sourceCode .ini}\ncertbot_dns_godaddy:dns_godaddy_key      = ...\ncertbot_dns_godaddy:dns_godaddy_secret = ...\n```\n',
    'author': 'Dustyn Gibson',
    'author_email': 'miigotu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miigotu/certbot-dns-godaddy',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

