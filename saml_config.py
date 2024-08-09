from saml2 import BINDING_HTTP_POST
from saml2.config import SPConfig

# Note these should have been created part of the SAML Metadata

def get_saml_config():
    config = {
        'entityid': 'your-streamlit-app-entity-id',
        'metadata': {
            'local': ['path-to-okta-metadata.xml'],
        },
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        ('http://localhost:8501/saml/acs', BINDING_HTTP_POST),
                    ],
                    'single_logout_service': [
                        ('http://localhost:8501/saml/slo', BINDING_HTTP_POST),
                    ],
                },
                'allow_unsolicited': True,
                'authn_requests_signed': False,
                'logout_requests_signed': True,
            },
        },
        'key_file': 'path-to-your-private-key.pem',
        'cert_file': 'path-to-your-public-cert.pem',
        'xmlsec_binary': '/usr/bin/xmlsec1',
    }

    return SPConfig().load(config)
