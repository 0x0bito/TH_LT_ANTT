import os
import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from ca_utils import CERTS_DIR, utcnow, load_cert

CRL_FILE = os.path.join(CERTS_DIR, "ca_crl.pem")


def load_key(filepath):
    with open(filepath, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def _write_crl(issuer_cert, issuer_key, revoked_certs):
    crl = (
        x509.CertificateRevocationListBuilder()
        .issuer_name(issuer_cert.subject)
        .last_update(utcnow())
        .next_update(utcnow() + datetime.timedelta(days=7))
    )
    for rc in revoked_certs:
        crl = crl.add_revoked_certificate(rc)
    crl = crl.sign(private_key=issuer_key, algorithm=hashes.SHA256())
    with open(CRL_FILE, "wb") as f:
        f.write(crl.public_bytes(serialization.Encoding.PEM))
    return crl


def create_empty_crl(issuer_cert, issuer_key):
    return _write_crl(issuer_cert, issuer_key, [])


def revoke_certificate(cert_file, issuer_cert_file, issuer_key_file,
                       reason=x509.ReasonFlags.key_compromise):
    cert = load_cert(cert_file)
    issuer_cert = load_cert(issuer_cert_file)
    issuer_key = load_key(issuer_key_file)

    revoked_certs = []
    if os.path.exists(CRL_FILE):
        with open(CRL_FILE, "rb") as f:
            crl = x509.load_pem_x509_crl(f.read())
        if crl.is_signature_valid(issuer_cert.public_key()):
            revoked_certs = list(crl)

    if not any(rc.serial_number == cert.serial_number for rc in revoked_certs):
        revoked_cert = (
            x509.RevokedCertificateBuilder()
            .serial_number(cert.serial_number)
            .revocation_date(utcnow())
            .add_extension(x509.CRLReason(reason), critical=False)
            .build()
        )
        revoked_certs.append(revoked_cert)

    return _write_crl(issuer_cert, issuer_key, revoked_certs)


def check_revocation_status(cert_file):
    cert = load_cert(cert_file)
    if not os.path.exists(CRL_FILE):
        return False
    with open(CRL_FILE, "rb") as f:
        crl = x509.load_pem_x509_crl(f.read())
    return any(rc.serial_number == cert.serial_number for rc in crl)
