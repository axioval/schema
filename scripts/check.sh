#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"
export PATH="$HOME/.local/bin:$PATH"

# Resolve checksum-pinned remote packages before sandboxed evaluation. Pkl still
# requires HTTPS resource permission for metadata and redirected release assets;
# file and environment resources remain denied.
pkl project resolve \
  --root-dir "$repo_root" \
  --allowed-modules 'file:,pkl:,package:,projectpackage:' \
  --allowed-resources 'https://openbimrs\.github\.io/pkl/.*,https://github\.com/openbimrs/pkl/releases/download/.*,https://release-assets\.githubusercontent\.com/.*,prop:pkl.outputFormat' \
  --timeout 30 \
  .

python3 -m unittest discover -s tests -v
python3 scripts/validate.py

# Exercise the distributable MCS transport without retaining binary artifacts.
mcs_tmp="$(mktemp -d)"
trap 'rm -rf "$mcs_tmp"' EXIT
python3 scripts/mcs.py pack examples/minimal "$mcs_tmp/one.mcs" --repository-root "$repo_root"
python3 scripts/mcs.py pack examples/minimal "$mcs_tmp/two.mcs" --repository-root "$repo_root"
cmp "$mcs_tmp/one.mcs" "$mcs_tmp/two.mcs"
sha256sum "$mcs_tmp/one.mcs" "$mcs_tmp/two.mcs"
python3 scripts/mcs.py verify "$mcs_tmp/one.mcs"
