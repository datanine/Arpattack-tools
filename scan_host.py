from scapy.all import *
 
interface = "eth0"
ip = conf.route.route("0.0.0.0")[2]
# 使用 split() 方法将 IP 地址按 "." 分割成四个部分
parts = ip.split(".")
# 提取前三个部分作为前半段 IP 地址
ip_parts = ".".join(parts[:3])

p=Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"{ip_parts}.1/24")
ans,unans=srp(p,timeout=2,iface=interface)

print("一共扫描到%d台主机："%len(ans))
result=[]

for s,r in ans:
    result.append([r[ARP].psrc,r[ARP].hwsrc])
result.sort()
for ip,mac in result:
    print(ip,"----->",mac)
