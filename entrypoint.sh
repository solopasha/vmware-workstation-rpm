#!/bin/bash
set -euxo pipefail

pushd "$1"

if [ -z "$1" ]; then
    echo "Please specify package to build"
    exit 1
fi
VERSION="$(rpmspec -q --qf "%{version}-%{release}\n" "$1.spec" | head -1)"
echo "VERSION=$VERSION" >> $GITHUB_ENV
sudo -s -u builduser -- <<EOF
spectool -g "$1.spec"
fedpkg --release f$(rpm -E %fedora) srpm
mock -r fedora-$(rpm -E %fedora)-$(uname -m)-rpmfusion_free --rebuild "$1-$VERSION.src.rpm" --enable-network --isolation=simple
EOF
