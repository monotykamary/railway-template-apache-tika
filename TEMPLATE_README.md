# Deploy and Host Apache Tika on Railway

## About Hosting Apache Tika

Apache Tika extracts text and metadata from more than a thousand document formats. This template deploys the stable official `4.0.0-1-full` container behind an authenticated Caddy proxy.

Retrieve the generated `BASIC_AUTH_USER` and `BASIC_AUTH_PASSWORD` values from the proxy service before calling parsing endpoints.

## Common Use Cases

- Extract searchable text from PDF, Office, ebook, image, and archive formats
- Detect file media types and metadata
- Add OCR and document ingestion to applications and search pipelines

## Dependencies for Apache Tika Hosting

### Deployment Dependencies

- Private Apache Tika service
- Public Caddy authentication proxy
- No database or persistent volume

### Implementation Details

Railway HTTPS routes to the proxy on port 8080. The proxy enforces generated HTTP Basic credentials, limits request bodies to 50 MB, and forwards requests over Railway private networking to Tika on port 9998. `/healthz` verifies the actual private Tika endpoint without exposing parsing APIs anonymously.

The template pins both image tags and Linux/AMD64 manifests. It uses Tika 4.0.0 because that is the newest stable official container release; it does not silently use a prerelease or a moving `latest` tag.

## Why Deploy Apache Tika on Railway?

Railway provides managed HTTPS, generated credentials, private service networking, health checks, and reproducible deployment for a stateless document parsing API.
