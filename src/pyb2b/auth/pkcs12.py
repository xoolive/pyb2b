import os
import typing
from datetime import datetime
from ssl import PROTOCOL_TLS, SSLContext
from tempfile import NamedTemporaryFile

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat
from cryptography.hazmat.primitives.serialization.pkcs12 import (
    load_key_and_certificates,
)
from cryptography.x509.base import Certificate


def check_cert(cert: typing.Optional[Certificate]) -> None:
    if not cert:
        raise ValueError("Broken client certificate")

    if cert.not_valid_after < datetime.utcnow():
        raise ValueError(
            f"Client certificate expired: Not After: {cert.not_valid_after}"
        )


def create_ssl_context(
    pkcs12_data: bytes,
    pkcs12_password_bytes: typing.Optional[bytes],
) -> SSLContext:
    (private_key, cert, ca_certs) = load_key_and_certificates(
        pkcs12_data, pkcs12_password_bytes
    )
    check_cert(cert)

    ssl_context = SSLContext(PROTOCOL_TLS)
    with NamedTemporaryFile(delete=False) as c:
        try:
            private_bytes = private_key.private_bytes(
                Encoding.PEM,
                PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
            c.write(private_bytes)

            public_bytes = cert.public_bytes(Encoding.PEM)
            c.write(public_bytes)

            if ca_certs:
                for ca_cert in ca_certs:
                    check_cert(ca_cert)
                    ca_public_bytes = ca_cert.public_bytes(Encoding.PEM)
                    c.write(ca_public_bytes)

            c.flush()
            c.close()
            ssl_context.load_cert_chain(c.name, password=pkcs12_password_bytes)
        finally:
            os.remove(c.name)

    return ssl_context
