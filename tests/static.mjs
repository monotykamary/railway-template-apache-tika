import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

const tika = readFileSync("tika/Dockerfile", "utf8");
const proxy = readFileSync("proxy/Dockerfile", "utf8");
const caddy = readFileSync("proxy/Caddyfile", "utf8");
const entrypoint = readFileSync("proxy/entrypoint.sh", "utf8");
const readme = readFileSync("README.md", "utf8");

assert.match(tika, /apache\/tika:4\.0\.0-1-full@sha256:[a-f0-9]{64}/);
assert.match(proxy, /caddy:2\.10\.2-alpine@sha256:[a-f0-9]{64}/);
assert.doesNotMatch(`${tika}\n${proxy}`, /:latest/);
assert.match(caddy, /handle \/healthz/);
assert.match(caddy, /basic_auth/);
assert.match(caddy, /max_size 50MB/);
assert.match(entrypoint, /caddy hash-password/);
assert.match(entrypoint, /unset BASIC_AUTH_PASSWORD/);
assert.match(readme, /newest stable official container release/);
assert.doesNotMatch(`${tika}\n${proxy}\n${caddy}\n${entrypoint}`, /BASIC_AUTH_PASSWORD=\S+/);

console.log("static template checks passed");
