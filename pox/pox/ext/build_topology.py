import os
import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.cli import CLI
sys.path.append("../../")
from pox.ext.jelly_pox import JELLYPOX
from subprocess import Popen
from time import sleep, time
import random

from construct_paths import Paths

class JellyFishTop(Topo):
    ''' TODO, build your topology here'''

    k = 5#Ports per switch #24
    r = 3#Ports dedicated to connecting to other ToR switches #10
    num_switches = 5#49

    def portListContainsOther(self, port, portList):
        for x in portList:
            if x != port:
                return True
        return False

    def build(self):

        hostList = []
        switchList = []
        portList = []


        #Add all switches to the topology
        counter = 0
        for y in range(self.num_switches):
            switchList.append(self.addSwitch('s%s' % (y)))
            for j in range(self.k-self.r):
                host = self.addHost('h' + str(counter), ip='0.0.0.0')
                hostList.append(host)
                self.addLink(switchList[y], hostList[-1], bw=10)
                counter += 1
            for x in range(self.r):
                portList.append(y)

        for currentSwitch in range(self.num_switches):

            canConnect = []
            for z in range(len(switchList)):
                is_neighbor = False
                for link in self.links():
                    if switchList[z] in link and switchList[currentSwitch] in link:
                        is_neighbor = True
                        break

                if not is_neighbor and z in portList and z != currentSwitch:
                    canConnect.append(z)

            while currentSwitch in portList and len(canConnect) > 0:
                if len(canConnect) == 1:
                    randNum = 0
                else:
                    randNum = random.randint(0, len(canConnect)-1)

                print "randNum: " + str(randNum)
                print "length of port list: " + str(len(portList))
                randPort = canConnect[randNum]

                portList.remove(randPort)
                portList.remove(currentSwitch)
                canConnect.remove(randPort)
                self.addLink(switchList[currentSwitch], switchList[randPort], bw=10)

        for x in self.links():
            print x


        #leftHost = self.addHost( 'h1' )
        #rightHost = self.addHost( 'h2' )
        #leftSwitch = self.addSwitch( 's3' )
        #rightSwitch = self.addSwitch( 's4' )

        # Add links
        #self.addLink( leftHost, leftSwitch )
        #self.addLink( leftSwitch, rightSwitch )
        #self.addLink( rightSwitch, rightHost )


def experiment(net):
        net.start()
        sleep(20)
        net.pingAll()
        net.stop()

def main():
    topo = JellyFishTop()
    net = Mininet(topo=topo, host=CPULimitedHost, link = TCLink, controller=JELLYPOX)
    net.start()
    # NOTE: Must come after net.start
    for host in net.hosts:
        print str(host)
        print str(host.defaultIntf().name)
	host.cmdPrint('dhclient '+host.defaultIntf().name)
    CLI(net)
    net.stop()
    #paths = Paths(net)
#    paths.all_k_shortest_paths(paths.switches_by_dpid, 2)
    '''
    hosts_per_switch = 23
    ksp_res = paths.count_distinct_paths(hosts_per_switch, 0, None)
    ecmp8_res = paths.count_distinct_paths(hosts_per_switch, 1, ksp_res[1])
    ecmp64_res = paths.count_distinct_paths(hosts_per_switch, 2, ksp_res[1])
    print "KSP Result: " + str(ksp_res[0])
    print "ECMP-8 Result: " + str(ecmp8_res[0])
    print "ECMP-64 Result: " + str(ecmp64_res[0])

    paths.plot_results(ksp_res[0], ecmp8_res[0], ecmp64_res[0])
    '''

#   net.interact()
    '''
    Now code to genereate the hosts and links for us in the topo visualizer
    dumpFilename = "dump.txt"
    dumpFile = open(dumpFilename, "w+")
    #for node in self.values():
    #    dumpFile.write( '%s\n' % repr( node ) )
    dumpFile.write(str(net.do_dump()))
    dumpFile.close()

    linksFilename = "links.txt"
    linksFile = open(linksFilename, "w+")
    linksFile.write(str(net.links()))
    linksFile.close()
    '''
#    experiment(net)

if __name__ == "__main__":
    main()

