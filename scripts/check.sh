#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"
export PATH="$HOME/.local/bin:$PATH"

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
