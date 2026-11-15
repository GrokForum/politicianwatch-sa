# Raw source files

Layout: `data/raw/<source_id>/<YYYY-MM-DD>/<name>` plus `manifest.jsonl` and a sidecar `.sha256` for each file.

**PDFs and other bulky binaries are not committed.** Re-download them from the URLs in `manifest.jsonl` and confirm the checksum. The manifest and `.sha256` files are committed.

Do not drop files that contain ID numbers, personal phone numbers, personal emails, or home addresses into this tree. If an IEC seat-allocation extract includes a candidate ID, strip that column before any derived file is written, and keep the raw extract out of git.
