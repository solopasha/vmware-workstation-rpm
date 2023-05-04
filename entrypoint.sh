#!/bin/bash
set -euxo pipefail
shopt -s nullglob
shopt -s extglob
mkdir /out
for package in "$@"
do
pushd "$package"
VERSION="$(rpmspec -q --qf "%{version}-%{release}\n" "$package.spec" | head -1)"
echo "VERSION=$VERSION" >> $GITHUB_ENV
sudo -s -u builduser -- <<EOF
spectool -g "$package.spec"
fedpkg --release f$(rpm -E %fedora) srpm
mock -r fedora-$(rpm -E %fedora)-$(uname -m)-rpmfusion_free --rebuild "$package"-*.src.rpm
EOF
mv /var/lib/mock/fedora-38-x86_64/result/{akmod*,*common!(*.src.rpm)} /out
popd
done
