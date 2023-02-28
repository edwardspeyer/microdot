set -ex

version="$1"

sudo apt install --yes --no-install-recommends \
  autoconf \
  automake \
  bison \
  build-essential \
  ca-certificates \
  ccache \
  git \
  libevent-dev \
  libncurses-dev \
  pkg-config

git clone --depth 1 --branch "$version" \
  https://github.com/tmux/tmux.git .

sh autogen.sh

./configure --enable-static --prefix ./out

make install
