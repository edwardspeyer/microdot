FROM debian:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install --yes --no-install-recommends \
    build-essential ca-certificates cmake git libncurses-dev \
    ninja-build
WORKDIR /src
ARG VERSION
RUN git clone --depth 1 --branch "$VERSION" \
    https://github.com/fish-shell/fish-shell.git .
RUN cmake \
    -DCMAKE_INSTALL_PREFIX=/out \
    -B build/ \
    .
RUN make -C build/
RUN make -C build/ install
