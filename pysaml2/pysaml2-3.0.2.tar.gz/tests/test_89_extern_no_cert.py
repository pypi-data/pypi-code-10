from saml2 import md
from saml2 import saml
from saml2 import config
from saml2 import xmldsig
from saml2 import xmlenc

from saml2.filter import AllowDescriptor
from saml2.mdstore import MetadataStore
from saml2.attribute_converter import ac_factory
from saml2.extension import mdui
from saml2.extension import idpdisc
from saml2.extension import dri
from saml2.extension import mdattr
from saml2.extension import ui

from pathutils import full_path

__author__ = 'roland'

sec_config = config.Config()

ONTS = {
    saml.NAMESPACE: saml,
    mdui.NAMESPACE: mdui,
    mdattr.NAMESPACE: mdattr,
    dri.NAMESPACE: dri,
    ui.NAMESPACE: ui,
    idpdisc.NAMESPACE: idpdisc,
    md.NAMESPACE: md,
    xmldsig.NAMESPACE: xmldsig,
    xmlenc.NAMESPACE: xmlenc
}

ATTRCONV = ac_factory(full_path("attributemaps"))

METADATACONF = {
    "1": [{
        "class": "saml2.mdstore.MetaDataExtern",
        "metadata": [
            ('http://example-sp.carrierwave.com/wordpress/wp-content/plugins/saml-20-single-sign-on/saml/www/module.php/saml/sp/metadata.php/1',)]
        }],
    "2": [{
        "class": "saml2.mdstore.MetaDataExtern",
        "metadata": [
            ('http://example-sp.carrierwave.com/wordpress/wp-content/plugins/saml-20-single-sign-on/saml/www/module.php/saml/sp/metadata.php/1',
             full_path("inc-md-cert.pem"))]
        }],
    "10": [{
        "class": "saml2.mdstore.MetaDataExtern",
        "metadata": [
            ("http://md.incommon.org/InCommon/InCommon-metadata-export.xml",
             full_path("inc-md-cert.pem"))]
        }
    ]
}

def test_no_cert_no_signature():
    mds = MetadataStore(list(ONTS.values()), ATTRCONV, sec_config,
                        disable_ssl_certificate_validation=True)

    mds.imp(METADATACONF["1"])
    assert len(mds.keys()) >= 1

def test_cert_no_signature():
    mds = MetadataStore(list(ONTS.values()), ATTRCONV, sec_config,
                        disable_ssl_certificate_validation=True)

    mds.imp(METADATACONF["2"])
    assert len(mds.keys()) >= 1

def test_signature_no_cert():
    mds = MetadataStore(list(ONTS.values()), ATTRCONV, sec_config,
                        disable_ssl_certificate_validation=True)

    mds.imp(METADATACONF["10"])
    assert len(mds.keys()) > 1

if __name__ == "__main__":
    test_no_cert_no_signature()