"""Reject the disclosed affected chains in certifi and system OpenSSL stores."""
import json
import subprocess
import tempfile
from pathlib import Path

import certifi

fixtures = json.loads((Path(__file__).with_name("impacted-intermediates.json")).read_text())
assert len(fixtures) == 16, "The complete disclosed fixture set is required"
with tempfile.TemporaryDirectory() as temporary:
    for index, fixture in enumerate(fixtures):
        pem = Path(temporary) / (str(index) + ".pem")
        pem.write_text(fixture["pem"])
        subprocess.run(["openssl", "x509", "-in", str(pem), "-noout"], check=True, capture_output=True)
        stores = (
            ["-no-CApath", "-no-CAstore", "-CAfile", certifi.where()],
            ["-no-CApath", "-no-CAstore", "-CAfile", "/etc/ssl/certs/ca-certificates.crt"],
            [],
        )
        for store in stores:
            result = subprocess.run(["openssl", "verify"] + store + [str(pem)], capture_output=True, text=True)
            assert result.returncode != 0, "Distrusted chain accepted: " + fixture["name"]
            assert "verification failed" in result.stderr, result.stderr
print("PASS: all 16 disclosed chains rejected by certifi and system trust")
