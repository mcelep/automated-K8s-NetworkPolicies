#!/bin/bash
# Take the input capture file as a command-line argument to the script
set -eux
IN_PCAP_FILE=$1
OUT_PCAP_FILE=${IN_PCAP_FILE}-full-conv
# Obtain the list of TCP stream IDs
TCP_STREAMS=$(tshark -r $IN_PCAP_FILE -2 -R "(tcp.flags.syn == 1 && tcp.flags.ack == 0) || (tcp.flags.syn == 1 && tcp.flags.ack == 1)" -T fields -e tcp.stream | sort -n | uniq)

# Generate a new tshark filter for each stream ID
TSHARK_FILTER=""
for stream in $TCP_STREAMS; do
  if [ "$TSHARK_FILTER" = "" ]; then
	TSHARK_FILTER="tcp.stream==${stream}"
  else
	TSHARK_FILTER="${TSHARK_FILTER}||tcp.stream==${stream}"
  fi
done
# Apply the stream ID filter and write out the filtered capture file
tshark -r $IN_PCAP_FILE -2 -R "${TSHARK_FILTER}" -w $OUT_PCAP_FILE
