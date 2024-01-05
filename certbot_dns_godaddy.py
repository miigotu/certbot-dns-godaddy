"""
This module defines a certbot plugin to automate the process of completing a
``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and subsequently
removing, TXT records using the godaddy CCP API.
"""

import logging
from typing import Any, Callable

from certbot.plugins import dns_common_lexicon

logger = logging.getLogger(__name__)


class Authenticator(dns_common_lexicon.LexiconDNSAuthenticator):
    """DNS Authenticator for GoDaddy

    This Authenticator uses the GoDaddy API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are '
                   'using GoDaddy for DNS).')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        
        params_dict = args[0].to_dict()
        self.ttl = str(params_dict.get("dns_godaddy_ttl", 600))
        super().__init__(*args, **kwargs)
        self._add_provider_option('key',
                                  'Key to access the Godaddy API',
                                  'auth_key')
        self._add_provider_option('secret',
                                  'Secret to access the Godaddy API',
                                  'auth_secret')

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None],
                             default_propagation_seconds: int = 30) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add('credentials', help='GoDaddy credentials INI file.')
    
    def more_info(self) -> str:
        return ('This plugin configures a DNS TXT record to respond to a '
                'dns-01 challenge using the godaddy API.')
    
    @property
    def _provider_name(self) -> str:
        return 'godaddy'
    
    @property
    def _ttl(self) -> int:
        """
        Time to live to apply to the DNS records created by this Authenticator
        """
        return self.ttl
