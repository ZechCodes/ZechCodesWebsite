# Container trust maintenance

Both stages use Python 3.11 on Debian Bookworm and explicitly refresh the
system ca-certificates package. Builds install certifi 2026.10.19 using
uv 0.13.4; build pip is pinned to 26.2.2. Poetry 1.8.5 preserves compatibility
with this project's lock format.

Each stage parses all 16 disclosed affected intermediate/cross-sign fixtures
and verifies that certifi, the system bundle, and default OpenSSL trust reject
them. Rebuild after future CA changes. A rebuild and deployment are required;
editing this repository does not update a running container.
