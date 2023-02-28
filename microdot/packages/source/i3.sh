set -ex

version="$1"

sudo apt install --yes --no-install-recommends \
  build-essential \
  libcairo2-dev \
  libev-dev \
  libpango1.0-dev \
  libpcre3-dev \
  libstartup-notification0-dev \
  libstartup-notification0-dev \
  libxcb-cursor-dev \
  libxcb-icccm4-dev \
  libxcb-keysyms1-dev \
  libxcb-randr0-dev \
  libxcb-shape0-dev \
  libxcb-util0-dev \
  libxcb-xinerama0-dev \
  libxcb-xkb-dev \
  libxcb-xkb-dev \
  libxcb-xrm-dev \
  libxkbcommon-dev \
  libxkbcommon-x11-dev \
  libyajl-dev \
  libyajl-dev \
  meson \
  ninja-build \
  suckless-tools \
  ;
  
wget "https://i3wm.org/downloads/i3-${version}.tar.xz"

tar xf "i3-${version}.tar.xz"

out="$PWD/out"

cd "i3-${version}"

mkdir -p build

cd build

meson --prefix $out ..

ninja

meson install
