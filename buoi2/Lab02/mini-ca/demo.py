import os
from ca_utils import (
    create_root_ca, create_intermediate_ca,
    issue_certificate, verify_certificate_chain, CERTS_DIR,
)
from revoke_utils import create_empty_crl, revoke_certificate, check_revocation_status


def main():
    print("=== Mini CA Demo ===\n")

    print("[1] Tạo Root CA...")
    root_key, root_cert = create_root_ca()
    print(f"    Subject: {root_cert.subject.rfc4514_string()}")
    print(f"    Valid until: {root_cert.not_valid_after_utc.date()}\n")

    print("[2] Tạo Intermediate CA...")
    int_key, int_cert = create_intermediate_ca(root_key, root_cert)
    print(f"    Subject: {int_cert.subject.rfc4514_string()}")
    print(f"    Valid until: {int_cert.not_valid_after_utc.date()}\n")

    print("[3] Cấp chứng chỉ cho end-entity...")
    entity_key, entity_cert = issue_certificate(
        int_key, int_cert,
        {"country": "VN", "org": "HUTECH", "common_name": "student.hutech.edu.vn"},
    )
    print(f"    Subject: {entity_cert.subject.rfc4514_string()}")
    print(f"    Valid until: {entity_cert.not_valid_after_utc.date()}\n")

    print("[4] Xác thực chuỗi chứng chỉ...")
    valid = verify_certificate_chain(entity_cert, [int_cert, root_cert])
    print(f"    Chain valid: {valid}\n")

    print("[5] Tạo CRL rỗng...")
    create_empty_crl(int_cert, int_key)
    print("    CRL created.\n")

    entity_cert_path = os.path.join(CERTS_DIR, "student.hutech.edu.vn_cert.pem")
    int_cert_path    = os.path.join(CERTS_DIR, "intermediate_cert.pem")
    int_key_path     = os.path.join(CERTS_DIR, "intermediate_key.pem")

    print("[6] Thu hồi chứng chỉ end-entity...")
    revoke_certificate(entity_cert_path, int_cert_path, int_key_path)
    print("    Certificate revoked.\n")

    print("[7] Kiểm tra trạng thái thu hồi...")
    revoked = check_revocation_status(entity_cert_path)
    print(f"    Is revoked: {revoked}\n")

    print("=== Done ===")


if __name__ == "__main__":
    main()
