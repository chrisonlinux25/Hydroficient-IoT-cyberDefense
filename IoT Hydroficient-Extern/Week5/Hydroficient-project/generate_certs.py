import ipaddress
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_ca_certificate():
    """Generate the Certificate Authority (CA) certificate"""

    print("[1/3] Generating Certificate Authority (CA)...")
    print("Generating CA private key (2048 bits)...")

    # Step 1: Generate a private key for the CA
    ca_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    print("      Creating CA certificate (valid for 10 years)...")

    # Step 2: Define the CA's identity
    ca_name = x509.Name([
        x509.NameAttribute(
            NameOID.ORGANIZATION_NAME,
            "Grand Marina Hotel"
        ),
        x509.NameAttribute(
            NameOID.ORGANIZATIONAL_UNIT_NAME,
            "Water Systems Security"
        ),
        x509.NameAttribute(
            NameOID.COMMON_NAME,
            "Grand Marina Root CA"
        ),
    ])

    # Step 3: Build and sign the CA certificate
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(
            datetime.now(timezone.utc) + timedelta(days=3650)
        )
        .add_extension(
            x509.BasicConstraints(
                ca=True,
                path_length=None
            ),
            critical=True,
        )
        .sign(ca_key, hashes.SHA256())
    )

    print("CA certificate created successfully!\n")

    return ca_key, ca_cert


def generate_server_certificate(ca_key, ca_cert):
    """Generate the server certificate signed by the CA"""

    print("[2/3] Generating Server Certificate...")
    print("Generating server private key (2048 bits)...")

    # The server gets its OWN key pair (separate from CA)
    server_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    print("Creating server certificate (valid for 1 year)...")

    # Server's identity
    server_name = x509.Name([
        x509.NameAttribute(
            NameOID.ORGANIZATION_NAME,
            "Grand Marina Hotel"
        ),
        x509.NameAttribute(
            NameOID.ORGANIZATIONAL_UNIT_NAME,
            "MQTT Broker"
        ),
        x509.NameAttribute(
            NameOID.COMMON_NAME,
            "localhost"
        ),
    ])

    server_cert = (
        x509.CertificateBuilder()
        .subject_name(server_name)
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(
            datetime.now(timezone.utc) + timedelta(days=365)
        )
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(
                    ipaddress.IPv4Address("127.0.0.1")
                ),
            ]),
            critical=False,
        )
        .add_extension(
            x509.BasicConstraints(
                ca=False,
                path_length=None
            ),
            critical=True,
        )
        .sign(ca_key, hashes.SHA256())
    )

    print("Common Name: localhost")
    print("Subject Alternative Names: localhost, 127.0.0.1")
    print("Server certificate created successfully!\n")

    return server_key, server_cert


def save_certificates(
    ca_cert,
    server_cert,
    server_key,
    output_dir="certs"
):
    print("[3/3] Saving certificates to certs/ folder...")

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Save CA certificate (public)
    with open(output_path / "ca.pem", "wb") as f:
        f.write(
            ca_cert.public_bytes(
                serialization.Encoding.PEM
            )
        )

    print("      Saved: certs/ca.pem")

    # Save server certificate (public)
    with open(output_path / "server.pem", "wb") as f:
        f.write(
            server_cert.public_bytes(
                serialization.Encoding.PEM
            )
        )

    print("      Saved: certs/server.pem")

    # Save server private key (SECRET!)
    with open(output_path / "server-key.pem", "wb") as f:
        f.write(
            server_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    print("Saved: certs/server-key.pem\n")


def main():

    print("=" * 55)
    print("  Certificate Generation for Grand Marina Hotel")
    print("=" * 55)
    print()

    # Generate CA
    ca_key, ca_cert = generate_ca_certificate()

    # Generate server certificate
    server_key, server_cert = generate_server_certificate(
        ca_key,
        ca_cert
    )

    # Save certificates
    save_certificates(
        ca_cert,
        server_cert,
        server_key
    )

    print("Verifying certificates...")

    print(f"CA Subject: {ca_cert.subject.rfc4514_string()}")
    print(
        f"CA Valid Until: "
        f"{ca_cert.not_valid_after_utc.date()}"
    )

    print(
        f"Server Subject: "
        f"{server_cert.subject.rfc4514_string()}"
    )

    print(
        f"Server Issuer: "
        f"{server_cert.issuer.rfc4514_string()}"
    )

    print(
        f"Server Valid Until: "
        f"{server_cert.not_valid_after_utc.date()}"
    )

    print("Chain verified: Server cert is signed by CA")
    print()
    print("=" * 55)
    print("  Certificates generated successfully!")
    print("=" * 55)
    print()
    print("Files created:")
    print("  certs/ca.pem         - CA certificate (share with clients)")
    print("  certs/server.pem     - Server certificate (for Mosquitto)")
    print("  certs/server-key.pem - Server private key (keep secret!)")


if __name__ == "__main__":
    main()

