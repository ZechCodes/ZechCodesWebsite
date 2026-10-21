# Container trust maintenance

The image installs certifi 2026.10.19 through uv 0.13.4, then replaces both
`/etc/ssl/certs/ca-certificates.crt` and the entire hashed certificate directory
with that bundle. Existing anchors cannot survive through old hash links.
Poetry 1.8.5 preserves compatibility with this project's existing lock format.
A rebuild and deployment are required; changing this repository does not update
a running container. Rebuild after future CA trust changes.

Both build and runtime stages use Python 3.11 on Debian Bookworm. Build
pip is pinned to 26.2.2 so its bundled trust also includes the distrust update.
