#!/usr/bin/python 

from __future__ import unicode_literals
from __future__ import division
import ipaddress
from python_ping import ping


# from lafibre.info
# https://lafibre.info/ipv6/plages-ip-par-fai/msg87273/
#Free (AS12322) => 11 141 114 IPv4
#212.27.32.0/19    AS12322
#213.228.0.0/18    AS12322
#62.147.0.0/16     AS12322
#81.56.0.0/15      AS12322
#82.64.0.0/14      AS12322
#82.224.0.0/11     AS12322
#88.160.0.0/11     AS12322
#78.192.0.0/10     AS12322
#83.152.0.0/13     AS12322
#88.120.0.0/13     AS12322
#91.160.0.0/12     AS12322
#213.36.0.0/16     AS12322
#83.214.0.0/16     AS12322
#194.149.160.0/19  AS12322
#82.142.0.0/18     AS12322
#212.62.128.0/18   AS12322


FREE_6RD_PREFIX = "2a01:e30::"

def ipv4_to_ipv6rd(ipv4_addr, sixrd_pref):
    # Free 6rd prefix
    sixrd_prefix = ipaddress.ip_address(sixrd_pref)
    # Shift 68 times the 32b of IPv4 address
    ip4rd = int(ipv4_addr) << 68
    # Binary OR with 6rd prefix
    long_prefix = int(sixrd_prefix) | ip4rd
    # Add ::1 to get the address of the freebox
    sixrd_address = ipaddress.ip_address(long_prefix + 1)
    return sixrd_address

def send_ping(addr, count):
    seq = 0
    stats_delay = []
    stats_ttl = []
    while seq < count:
        res = ping.single_ping(str(addr), str(addr), 3000, seq, 64, ipv6=True, verbose=True)
        seq +=1
        stats_delay.append(res[0])
        stats_ttl.append(res[1][4])
    avg_rtt = sum(stats_delay)/len(stats_delay)
    avg_ttl = sum(stats_ttl)/len(stats_ttl)
    return avg_rtt, avg_ttl
        
        
ipv6pref_scanlist = [
    '2a01:e35:8780::/43', # ADSL: 6rd prefix for 88.120.0.0/13
    '2a01:e0a:2::/47' # Fiber: Native IPv6
]


f = open('./rttavg.txt', 'w', 0)
for ipv6pref in ipv6pref_scanlist:
    p = ipaddress.IPv6Network(ipv6pref)
    for freebox_ipv6pref in p.subnets(new_prefix=60):
        freebox_ipv6addr = freebox_ipv6pref.hosts().next()
        #print freebox_ipv6addr
        try:
            rttavg, ttlavg =  send_ping(freebox_ipv6addr, 10)
            line = str(freebox_ipv6addr) + " , " + str(rttavg) + " , " + str(ttlavg)
            f.write(line + "\n")
            print line
        except KeyboardInterrupt:
            f.close()
            break
#        except:
#            continue

#for ipv4_pref, sixrd_pref in six6rd_plan.iteritems():
#    free_net = ipaddress.ip_network(ipv4_pref)
#    for ipv4_addr in free_net:
#        sixrd_addr = ipv4_to_ipv6rd(ipv4_addr, sixrd_pref)
#        print sixrd_addr
#        try:
#            p = list(ping.quiet_ping(str(sixrd_addr), timeout=3000, count=3, ipv6=True))
#            print p[-1]
#        except:
#            continue