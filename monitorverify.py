import dns.resolver
import socket
import deets

def verify(dnsserver):
    myResolver = dns.resolver.Resolver()
    myResolver.timeout = 5
    myResolver.lifetime = 5
    try:
        # Is IP?
        socket.inet_aton(dnsserver)
        # Then set our DNS server to the IP
        myResolver.nameservers = [dnsserver]
    except socket.error:
        # Is not IP?  Then resolve the hostname
        dnsquery = myResolver.query(dnsserver, "A")
        # We only want the 1st A record
        #myResolver.nameservers = [arecord]
        arecord = dnsquery[0]
        myResolver.nameservers = [arecord]
    try:
        # Resove the FQDN we are testing
        cdnip = myResolver.query(monitoredsite, "A")
        edgeip = str(cdnip[0])
    except:
        edgeip = "Failure"
    return edgeip
