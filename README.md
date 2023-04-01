# HW3 BLE Central Programming

> Modified from ble_scan_connect.py 

## Members 

- 毛楷維 b07901134
- 涂銘洋 b07202031
- 古振宏 b08901103

## Codes added

```python
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)
    # Processing data of notifications from the server
    def handleNotification(self, cHandle, data): <--
        print("Received data: " + str(data)) 	 <--
```

```python
try :
    testService = dev.getServiceByUUID(UUID(0xfff0))
    for ch in testService.getCharacteristics():
        print(str(ch))

    ch = dev.getCharacteristics(uuid=UUID(0xfff1))[0]
    if (ch.supportsRead()):
        print(ch.read())

    cccd = ch.getDescriptors(forUUID=0x2902)[0] <--
    cccd.write(b"\x01\x00")                     <--
    print("Enabled notifications.")             <--
    print(cccd.read())                          <--

    while True:                                 <--
        if dev.waitForNotifications(1000):  	<--
            print("Notify!")            		<--
        print("Waiting...")                 	<--
```

## sudo minicom -s

Configurations -> Serial port setup -> Serial Device : /dev/tty.usbserial-xxx (checked by `ls /dev` on terminal)

## sudo minicom

Log in Raspberry Pi

## Open iPhone app 'BLE scanner'

Configurations : 
- properties : READ WRITE NOTIFY
- READ value
- service UUID : FFF0
- characteristic UUID : FFF1

Start advertising

## Run `sudo python ble_enableNotify.py` on target
