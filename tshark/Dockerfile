FROM alpine:latest

RUN apk --no-cache add tshark
RUN adduser tshark --uid 1001 --ingroup wireshark --disabled-password 

RUN chmod +x /usr/bin/dumpcap

USER 1001
ENTRYPOINT [ "/usr/bin/tshark" ]
CMD [ "-h" ]
