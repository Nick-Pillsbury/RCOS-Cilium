FROM fluent/fluent-bit:latest

COPY fluent-bit-config.yaml /fluent-bit/etc/fluent-bit.conf

CMD ["/fluent-bit/bin/fluent-bit", "-c", "/fluent-bit/etc/fluent-bit.conf"]