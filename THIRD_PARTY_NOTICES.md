# Third-party notices

## Apache Tika

- Version: 4.2.0 official full container release
- Source: https://github.com/apache/tika/tree/4.2.0
- Container source: https://github.com/apache/tika-docker
- Copyright: The Apache Software Foundation
- License: Apache License 2.0

`assets/apache-tika-feather.svg` preserves all seven paths, original colors, and geometry of the complete feather group from `ASF_Tika-colour.svg` in `docs/assets/logos/asf-tika-logos.zip` at Apache Tika 4.2.0 source commit `91361891b61f6cc043a5ea81ced4867c17b93a9c` ([source archive](https://github.com/apache/tika/blob/91361891b61f6cc043a5ea81ced4867c17b93a9c/docs/assets/logos/asf-tika-logos.zip)). Archive SHA-256: `bb39805cb471565dc9f242e1c2d11096dab0fbde8e1556fea8ff1b550b66b212`. The standalone SVG removes the wordmark and changes only the viewport to enclose the complete feather. `assets/apache-tika-feather-transparent-512.png` rasterizes it proportionally at 480px high, centered on a transparent 512×512 canvas. Nothing is clipped or stretched. Alpha bounds `(109,16,403,496)` intentionally preserve the original portrait aspect ratio; the numeric audit uses a documented minimum ratio of 0.55 rather than cropping to satisfy 0.75. Apache artwork remains under Apache License 2.0 and the Apache Software Foundation branding ownership.

The historical `assets/apache-tika-icon.png` is a square crop and resize of `tika-app/src/main/resources/org/apache/tika/gui/tika.png` from the Apache Tika 3.3.2 source tag. It is redistributed under Apache License 2.0.

## Caddy

- Version: 2.10.2
- Source: https://github.com/caddyserver/caddy
- License: Apache License 2.0
