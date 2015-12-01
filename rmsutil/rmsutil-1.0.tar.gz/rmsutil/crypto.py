import base64
import hashlib
import hmac


def opaque_id(key, identifier):
    """Calculate an opaque ID corresponding to a private identifier.

    This function uses HMAC-SHA256 to hash a private identifier to an
    unpredictable, opaque ID. The hashed ID can be used in place of the
    original in order to avoid exposing a potentially sensitive value,
    such as a database table's monotonic primary key, in an insecure
    context.

    Args:
        key (six.text_type): URL-safe Base64-encoded HMAC key. The
            decoded key must provide at least 128 bits (16 bytes)
            of entropy.
        identifier (six.text_type): Private value to hash.

    Returns:
        six.text_type: 32-byte opaque ID, encoded as a URL-safe Base64
            string.
    """

    # NOTE(kgriffs): The identifier will probably only include simple
    #   ASCII chars, but encode as UTF-8 just in case.
    msg_bytes = identifier.encode('utf-8')

    # NOTE(kgriffs): Under Python 2.7, base64.urlsafe_b64decode can not
    #   handle a Unicode string. Py3k can handle either, so we just
    #   normalize to bytes.
    key_b64_bytes = key.encode()
    key_bytes = base64.urlsafe_b64decode(key_b64_bytes)

    if len(key_bytes) < 16:
        raise ValueError('Decoded key must be at least 16 bytes in length')

    digest = hmac.new(key_bytes, msg_bytes, hashlib.sha256).digest()
    encoded_digest = base64.urlsafe_b64encode(digest)

    return encoded_digest.decode()
