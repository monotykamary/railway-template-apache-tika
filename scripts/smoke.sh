#!/bin/sh
set -eu

: "${BASE_URL:?Set BASE_URL to the public proxy origin}"
: "${BASIC_AUTH_USER:?Set BASIC_AUTH_USER}"
: "${BASIC_AUTH_PASSWORD:?Set BASIC_AUTH_PASSWORD}"
base=${BASE_URL%/}

curl -fsS "$base/healthz" | grep -qi 'Apache Tika'

status=$(curl -sS -o /dev/null -w '%{http_code}' --request PUT --data-binary 'unauthorized probe' "$base/tika")
[ "$status" = "401" ]

text=$(printf 'Railway Tika extraction probe' | curl -fsS --user "$BASIC_AUTH_USER:$BASIC_AUTH_PASSWORD" --request PUT --header 'Content-Type: text/plain' --header 'Accept: text/plain' --data-binary @- "$base/tika")
printf '%s' "$text" | grep -q 'Railway Tika extraction probe'

status=$(curl -sS -o /dev/null -w '%{http_code}' --user "$BASIC_AUTH_USER:not-the-password" "$base/tika")
[ "$status" = "401" ]

printf '%s\n' "Apache Tika smoke checks passed"
