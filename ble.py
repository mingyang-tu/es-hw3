# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

# 創建一個掃描器對象並設置委託
scanner = Scanner().withDelegate(ScanDelegate())

# 開始掃描BLE裝置
devices = scanner.scan(10.0)
n = 0
addr = []

# 列出已發現的藍牙裝置
for dev in devices:
    print("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print(" %s = %s" % (desc, value))

# 要求用戶輸入要連接的裝置的編號
number = input('Enter your device number: ')
print('Device', number)

# 連接到所選擇的裝置
num = int(number)
print(addr[num])
print("Connecting...")
dev = Peripheral(addr[num], 'random')

# 列出已連接的裝置支持的所有服務
print("Services...")
for svc in dev.services:
    print(str(svc))

# 找到適當的特徵來設置CCCD值
try:
    testService = dev.getServiceByUUID(UUID(0xfff0))
    for ch in testService.getCharacteristics():
        print(str(ch))

    # 假設特徵UUID為0xfff1
    ch = dev.getCharacteristics(uuid=UUID(0xfff1))[0]
    if (ch.supportsRead()):
        print(ch.read())

    # 得到該特徵的CCCD句柄
    cccd_handle = ch.getHandle() + 1

    # 寫入0x0002的CCCD值以啟用通知
    ch.write(bytes([0x02, 0x00]), withResponse=True)
    print("CCCD value set to 0x0002 for characteristic with UUID 0xfff1")

    # 讀取該特徵的值以確認CCCD值是否設置成功
    cccd_value = ch.read()
    print("CCCD value for characteristic with UUID 0xfff1: ", cccd_value.hex())

finally:
    dev.disconnect()
