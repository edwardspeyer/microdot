set -ex

version="$1"

sudo apt install --yes --no-install-recommends \
  build-essential \
  ca-certificates \
  ccache \
  cmake \
  git \
  libncurses-dev \
  ninja-build

git clone --depth 1 --branch "$version" \
  https://github.com/fish-shell/fish-shell.git .

cmake \
  -DCMAKE_INSTALL_PREFIX=out \
  -B build/ \
    .
make -C build/

make -C build/ install

rm -f \
  out/bin/fish_key_reader \
  out/bin/fish_indent
