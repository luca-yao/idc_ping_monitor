
## 前言
Smokeping是一個很常見的套件，但在使用的時候要透過自有網頁查看，~~我很懶得開好幾個頁面做監控~~，但因為它是使用RRDTOOL，所以我們還得再透過Python來拆解RRD，並將資料轉到Prometheus PushGateway，再透過Grafana繪製。

```懶惰是有代價的 σ`∀´)σ```

## 內文
本次主要由以下三項組成：
- smokeping： 負責收集資訊
- prometheus：負責轉存數據
- grafana：   負責呈現數據

※本篇內容將不包含smokeping安裝教學，日後會再寫一篇跟大家分享
本程式原始來源為 https://github.com/wilsonchai8/idc_ping_monitor

因為原作者本身的分類對我來說，有些不必要，因此使用上會有多餘的分類之外，也因為欄位不同導至Python在執行的時候導致錯誤發生，因此我將這些問題修正後分享出來給大家。

以下我就不貼太多了 ~~省得看了討厭~~ 

我只貼了幾個未來使用上，應該、可能、或許要調整的地方。

#### 用於你Smokeping要使用到的host對應
```
paras = {
    'province_map' : {
        'China'                                 : '中國' ,
        'TW-Hinet'                              : '中華電信' ,
        'TW-FET'                                : '遠傳電信' ,
        'TW-TTN'                                : '台灣固網' ,
        'Singapro-1'                            : '新加坡-1' ,
        'Singapro-2'                            : '新加坡-2' ,
        'Cloudflare-1'                          : 'CloudFlare_1' ,
        'Cloudflare-2'                          : 'CloudFlare_2' ,
        'Google-1'                              : 'Google_1' ,
        'Google-2'                              : 'Google_2' ,
        'Hongkong-1'                            : '香港-1' ,
        'Hongkong-2'                            : '香港-2' ,
        'Macao-1'                               : '澳門-1' ,
        'Macao-2'                               : '澳門-2' ,
        'Japan-KDDI'                            : '日本-KDDI' ,
        'Japan-DOCOMO'                          : '日本-DOCOMO' ,
        'Korea-NICT'                            : '韓國-NICT' ,
        'Korea-KT'                              : '韓國-KT' ,
        'Malaysian-Digi'                        : '馬來西亞-Digi' ,
        'Malaysian-Celcom'                      : '馬來西亞-Celcom' ,
        'Malaysian-Maxis'                       : '馬來西亞-Maxis' ,
        'Thailand-AIS'                          : '泰國-AIS' ,
        'Vietnam-VNPT'                          : '越南-VNPT' ,
        'GT-DNS-1'                              : '亞太DNS-1' ,
        'GT-DNS-2'                              : '亞太DNS-2' ,
} ,
```

#### 檔案放置路徑
```
    'prometheus_gateway' : 'http://192.168.1.100:9091' ,  #修改主機IP
    'data_dir' : '/usr/local/smokeping/data/DNS',                  #修改至RRD產出的資料夾位置
    'LOG_FILE' : '/usr/local/smokeping/var/idc_ping_monitor.log'     #修改至要存放LOG的地方
}
```

#### 排程
```bash
*/1 * * * * root python3 /usr/local/smokeping/etc/collection_to_prometheus.py
```

因為該程式的使用也有透過`LogHandler`寫到自己的log檔案中，所以如果執行上有問題，可以透過自帶的Log File去排查，我個人覺得這是一個很棒的想法。

- 因為是Python主動去解析資料並將之到轉發到Prometheus，所以需要啟動PushGateway接收資料 下載將同版本的PushGateway
```
wget https://github.com/prometheus/pushgateway/releases/download/v1.6.0/pushgateway-1.6.0.linux-amd64.tar.gz
tar zxvf pushgateway-1.6.0.linux-amd64.tar.gz
nohup ./pushgateway &  
```
確認是否啟動
```
netstat -nltup | grep pushgateway
or
ps -ef |grep pushgateway
```

※可以去pushgateway確認是否有接收到資料
`http://localhost:9091`
如果有成功接收到會如下圖呈現
![Imgur](https://i.imgur.com/dRj54YJ.png)
### Grafana Dashboard
![Imgur](https://i.imgur.com/CGQk5GX.png)
