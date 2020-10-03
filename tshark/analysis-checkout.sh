#tshark -r "../.tmp/checkoutservice-848d6d8588-lwnw5.pcap.gz.base64" -Y " ip.src == 172.17.0.22 && tcp.flags.syn==1 && tcp.flags.ack==0 && not icmp" --color -Tfields -eip.src_host -eip.dst_host  -e tcp.dstport | sort --unique

tshark -r "../.tmp/checkoutservice-8894dfcd8-bq9d9.pcap" -Y " ip.src == 172.17.0.20 && tcp.flags.syn==1 && tcp.flags.ack==0 && not icmp" --color -Tfields  -eip.dst_host  -e tcp.dstport -Eseparator=, | sort --unique
