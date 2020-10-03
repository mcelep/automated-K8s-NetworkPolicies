#tshark -r "../.tmp/checkoutservice-848d6d8588-lwnw5.pcap.gz.base64" -Y " ip.src == 172.17.0.22 && tcp.flags.syn==1 && tcp.flags.ack==0 && not icmp" --color -Tfields -eip.src_host -eip.dst_host  -e tcp.dstport | sort --unique

tshark -r "../.tmp/frontend-5f5dd6455f-4mlq7.pcap.gz.base64" -Y " ip.src == 172.17.0.25 && tcp.flags.syn==1 && tcp.flags.ack==0 && not icmp" --color -Tfields  -eip.dst_host  -e tcp.dstport -Eseparator=, | sort --unique
