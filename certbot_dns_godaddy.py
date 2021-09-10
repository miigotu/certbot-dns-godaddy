"""
This module defines a certbot plugin to automate the process of completing a
``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and subsequently
removing, TXT records using the godaddy CCP API.
"""

import logging

import zope.interface
from certbot import errors, interfaces
from certbot.plugins import dns_common, dns_common_lexicon
from lexicon.providers import godaddy
from requests.exceptions import RequestException
import tldextract

logger = logging.getLogger(__name__)


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
        super(Authenticator, cls).add_parser_arguments(add,default_propagation_seconds=30)
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
        return self.godaddy_client.add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        return self.godaddy_client.del_txt_record(domain, validation_name, validation)

    @property
    def godaddy_client(self):
        return _GodaddyLexiconClient(credentials=self.credentials.conf)


class _GodaddyLexiconClient(dns_common_lexicon.LexiconClient):
    """Encapsulates all communication with godaddy via Lexicon."""

    def __init__(self, credentials):
        super(_GodaddyLexiconClient, self).__init__()
        config = dns_common_lexicon.build_lexicon_config('godaddy', {}, {
            'auth_key': credentials('key'),
            'auth_secret': credentials('secret')
        })

        self.provider = godaddy.Provider(config)

    def add_txt_record(self, domain, record_name, record_content):
        """
        Add a TXT record using the supplied information.

        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :raises errors.PluginError: if an error occurs communicating with the DNS Provider API
        """
        ex = tldextract.extract(domain)
        try:
            self._find_domain_id(ex.registered_domain)
        except errors.PluginError as e:
            logger.debug('Encountered error finding domain_id during add: %s', e, exc_info=True)
            return

        try:
            self.provider.create_record(rtype='TXT', name=record_name, content=record_content)
        except RequestException as e:
            logger.debug('Encountered error adding TXT record: %s', e, exc_info=True)
            raise errors.PluginError('Error adding TXT record: {0}'.format(e))

    def del_txt_record(self, domain, record_name, record_content):
        """
        Delete a TXT record using the supplied information.

        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :raises errors.PluginError: if an error occurs communicating with the DNS Provider  API
        """
        ex = tldextract.extract(domain)
        try:
            self._find_domain_id(ex.registered_domain)
        except errors.PluginError as e:
            logger.debug('Encountered error finding domain_id during deletion: %s', e, exc_info=True)
            return

        try:
            self.provider.delete_record(rtype='TXT', name=record_name, content=record_content)
        except RequestException as e:
            logger.debug('Encountered error deleting TXT record: %s', e, exc_info=True)
