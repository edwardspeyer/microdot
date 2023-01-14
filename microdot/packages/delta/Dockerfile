FROM alpine:latest
RUN apk add cargo git
WORKDIR /src
ARG VERSION
RUN git clone --depth 1 --branch "$VERSION" \
    https://github.com/dandavison/delta.git .
ENV RUSTFLAGS="-C target-feature=+crt-static"
RUN cargo install --path . --target x86_64-alpine-linux-musl
RUN mkdir -p /out/bin
RUN cp /root/.cargo/bin/delta /out/bin/
