FROM debian:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install --yes --no-install-recommends \
    autoconf automake bison build-essential ca-certificates git \
    libevent-dev libncurses-dev pkg-config
WORKDIR /src
ARG VERSION
RUN git clone --depth 1 --branch "$VERSION" \
    https://github.com/tmux/tmux.git .
RUN sh autogen.sh
RUN ./configure --enable-static --prefix /out
RUN make install
