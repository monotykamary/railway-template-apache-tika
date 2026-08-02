# Apache Tika on Railway

Deploy a private Apache Tika 3.3.1 parsing service behind an authenticated HTTPS proxy on Railway.

The Deploy on Railway button is added after the published route is verified.

## What this deploys

- Apache Tika Server `3.3.1.0-full`, pinned to the official Linux/AMD64 image digest
- Caddy `2.10.2-alpine`, pinned by digest
- A public Caddy proxy with generated HTTP Basic authentication
- A private Tika service reachable only over Railway's internal network

Apache Tika 3.3.2 is the newest source release, but Apache has not published a matching stable Docker image. This template deliberately uses the newest stable official container release instead of a prerelease or locally repackaged binary.

## Usage

Read `BASIC_AUTH_USER` and `BASIC_AUTH_PASSWORD` from the proxy service variables, then submit a document:

```bash
curl --user "$BASIC_AUTH_USER:$BASIC_AUTH_PASSWORD" \
  --request PUT \
  --header 'Accept: text/plain' \
  --data-binary @document.pdf \
  "https://your-domain.example/tika"
```

The unauthenticated `/healthz` endpoint checks the private Tika `/tika` endpoint. All parsing endpoints require authentication. Requests larger than 50 MB are rejected by the proxy.

## Service topology

```text
Internet -> proxy:8080 -> tika:9998
```

Tika is stateless. No database or persistent volume is required. Temporary parsing files remain inside the container and disappear on redeploy.

## Security and limits

- Treat Tika as a sensitive document-processing API; do not remove proxy authentication casually.
- Parsing adversarial files carries risk. Keep the pinned release current and set realistic Railway memory limits.
- The full image includes OCR and broad parser support and therefore needs more memory than the minimal image.
- Processing time and memory vary substantially with document type and size.

## Updating

Update the official Tika and Caddy tags and immutable digests, review Apache security and release notes, then repeat text extraction, metadata, malformed-input, authentication, memory, and redeploy soak tests.

## Validation

```bash
npm test
BASE_URL=https://your-domain.example BASIC_AUTH_USER=tika BASIC_AUTH_PASSWORD=... ./scripts/smoke.sh
```

## Upstream

- Tika source: https://github.com/apache/tika/tree/3.3.1
- Tika Docker source: https://github.com/apache/tika-docker
- Documentation: https://tika.apache.org/3.3.1/
- License: Apache License 2.0

This repository contains only Railway deployment adapters and documentation. Apache Tika and Apache are trademarks of their respective owners. This project is not affiliated with Apache or Railway.
