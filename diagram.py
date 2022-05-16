from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.digitalocean.network import LoadBalancer
from diagrams.k8s.infra import Master, Node
from diagrams.onprem.compute import Server
from diagrams.azure.identity import ActiveDirectory
import urllib.request

RHCOS = "Red Hat CoreOs"

graph_attr = {"compound": "true"}


### Utility class for human readable properties of nodes
class CustomNode(object):

    def __init__(self, name, osname, ipadd):
        self.name = name
        self.osname = osname
        self.ipadd = ipadd

    def display(self):
        return "{0}\n {1}\n {2}".format(self.name, self.osname, self.ipadd)


### Creation of OCP components
MasterNodes = []
MasterNodes.append(CustomNode("ocpdev03", RHCOS, "10.10.12.101"))
MasterNodes.append(CustomNode("ocpdev04", RHCOS, "10.10.12.102"))
MasterNodes.append(CustomNode("ocpdev05", RHCOS, "10.10.12.103"))

CloudPakForIntegrationNodes = []
CloudPakForIntegrationNodes.append(CustomNode("ocpdev10", RHCOS, "10.10.12.110"))
CloudPakForIntegrationNodes.append(CustomNode("ocpdev11", RHCOS, "10.10.12.111"))

OpenshiftContainerStorageNodes = []
OpenshiftContainerStorageNodes.append(CustomNode("ocpdev15", RHCOS, "10.10.12.115"))
OpenshiftContainerStorageNodes.append(CustomNode("ocpdev16", RHCOS, "10.10.12.116"))

OpenshiftMonitoringStack = []
OpenshiftMonitoringStack.append(CustomNode("ocpdev06", RHCOS, "10.10.12.106"))
OpenshiftMonitoringStack.append(CustomNode("ocpdev07", RHCOS, "10.10.12.107"))

OpenshiftRouters = []
OpenshiftRouters.append(CustomNode("ocpdev108", RHCOS, "10.10.12.108"))
OpenshiftRouters.append(CustomNode("ocpdev109", RHCOS, "10.10.12.109"))

#Diagram Code

with Diagram("OCP DEV CLUSTER", show=False, direction="TB", graph_attr=graph_attr) as diag:
    with Cluster("OCP DEV CLUSTER - domain: corporate.local"):
        lbServices = LoadBalancer("APP LOAD BALANCER")
        lbCluster = LoadBalancer("API LOAD BALANCER")
        with Cluster("sandbox"):
            with Cluster("masters", direction='RL') as clusterMasters:
                masters = []
                for node in reversed(MasterNodes):
                    masters.append(Master(node.display()))
            with Cluster("workers") as clusterWorkers:
                with Cluster("cp4i"):
                    cp4i = []
                    for node in reversed(CloudPakForIntegrationNodes):
                        cp4i.append(Node(node.display()))
                with Cluster("infra"):
                    with Cluster("ocs"):
                        ocs = []
                        for node in reversed(OpenshiftContainerStorageNodes):
                            ocs.append(Node(node.display()))
                    with Cluster("monitoring"):
                        monitoring = []
                        for node in reversed(OpenshiftMonitoringStack):
                            monitoring.append(Node(node.display()))
                    with Cluster("router"):
                        routers = []
                        for node in reversed(OpenshiftRouters):
                            routers.append(Node(node.display()))
        with Cluster("Externals"):            
            ad = ActiveDirectory(CustomNode("Active Directory", "corporate.local", "").display())
            bastion = Server(CustomNode("ocpdev01", RHCOS, "10.10.12.191").display())
            
            #Test custom using an image from internet
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'Mozilla/Chome/Edge')
            proxy_url = "https://e7.pngegg.com/pngimages/863/387/png-clipart-proxy-server-computer-software-anonymity-information-technology-anonymous-web-browsing-others-blue-computer-network.png"
            proxy_icon = "./custom-icons/proxy.png"
            filename, headers = opener.retrieve(proxy_url, proxy_icon)
            proxy = Custom(CustomNode("Proxy", "proxy100:3128", "").display(),proxy_icon)

    lbCluster >> Edge(ltail="loadbalancer_lbCluster", lhead="cluster_masters", color="red",
                      style="dashed") >> masters[1]
    lbServices >> Edge(ltail="loadbalancer_lbServices", lhead="cluster_workers", color="red",
                       style="dashed") >> monitoring[0]

diag