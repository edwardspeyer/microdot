set -ex

version="$1"

url="https://github.com/dandavison/delta/releases/download/${version}/git-delta_${version}_amd64.deb"

wget $url
dpkg -x git-delta*.deb v
mkdir -p out/bin
cp v/usr/bin/delta out/bin/
