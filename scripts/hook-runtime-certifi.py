import os
import sys

if getattr(sys, "frozen", False):
    base = sys._MEIPASS  # type: ignore[attr-defined]
    bundled = os.path.join(base, "certifi", "cacert.pem")
    if os.path.exists(bundled):
        os.environ.setdefault("SSL_CERT_FILE", bundled)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", bundled)
    else:
        # Fall back to system CA bundle on Linux
        for path in [
            "/etc/ssl/certs/ca-certificates.crt",
            "/etc/ssl/cert.pem",
            "/etc/pki/tls/certs/ca-bundle.crt",
        ]:
            if os.path.exists(path):
                os.environ.setdefault("SSL_CERT_FILE", path)
                os.environ.setdefault("REQUESTS_CA_BUNDLE", path)
                break
