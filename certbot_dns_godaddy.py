"""
This module defines a certbot plugin to automate the process of completing a
``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and subsequently
removing, TXT records using the godaddy CCP API.
"""

from lexicon.providers import godaddy
import zope.interface

from certbot import interfaces
from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for godaddy

    This Authenticator uses the godaddy API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are '
                   'using godaddy for DNS).')

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='godaddy credentials INI file.')

    def more_info(self):
        return ('This plugin configures a DNS TXT record to respond to a '
                'dns-01 challenge using the godaddy API.')

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'godaddy credentials INI file',
            {
                'key': 'Key to access the Godaddy API',
                'secret': 'Secret to access the Godaddy API',
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_godaddy_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_godaddy_client().del_txt_record(domain, validation_name, validation)

    def _get_godaddy_client(self):
        return _GodaddyLexiconClient(credentials=self.credentials.conf)


class _GodaddyLexiconClient(dns_common_lexicon.LexiconClient):
    """Encapsulates all communication with godaddy via Lexicon."""

    def __init__(self, credentials):
        super(_GodaddyLexiconClient, self).__init__()
        config = dns_common_lexicon.build_lexicon_config('godaddy', {}, {
            'auth-key': credentials('key'),
            'auth-secret': credentials('secret')
        })
        self.provider = godaddy.Provider(config)

    # called while guessing domain name (going from most specific to tld):
    def _handle_general_error(self, e, domain_name):
        if 'Value in field domainname does not match requirements' in str(e):
            return None
        return super(_GodaddyLexiconClient, self)._handle_general_error(e, domain_name)