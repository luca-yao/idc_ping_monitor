#coding:utf-8
import requests, rrdtool, os
from common import LogHandler

paras = {
    'province_map' : {
        'China'                                 : '中國' ,
        'TW-Hinet'                              : '中華電信' ,
        'CHT-IDC-7A03-1'                        : '新莊機房-7A03-1' ,
        'CHT-IDC-7A03-2'                        : '新莊機房-7A03-2' ,
        'CHT-IDC-7A07-1'                        : '新莊機房-7A07-1' ,
        'CHT-IDC-7A07-2'                        : '新莊機房-7A07-2' ,
        'CHT-IDC-7A10-1'                        : '新莊機房-7A10-1' ,
        'CHT-IDC-7A10-2'                        : '新莊機房-7A10-2' ,
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
        'Netmarble-APIS'                        : 'Netmarble_APIS' ,
        'Netmarble-NMSS'                        : 'Netmarble_NMSS',
    } , 
    'prometheus_gateway' : 'http://192.168.1.100:9091' , 
    'data_dir' : '/usr/local/smokeping/data/DNS',
    'LOG_FILE' : '/usr/local/smokeping/var/idc_ping_monitor.log'
}
def pushMetrics(instance, key, value):
    headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
    pushgateway = '%s/metrics/job/smokeping-collected/instance/%s' % (paras['prometheus_gateway'], instance)
    metrics = 'smokeping_%s{instance=\"%s\" , IDC=\"%s\" , alias=\"%s\"} %d' % (key, instance, 'CHT', paras['province_map'].get(instance), value)
    request_code = requests.post(pushgateway , data='{0}\n'.format(metrics).encode('utf-8') , headers=headers)
    @LogHandler(pushgateway)
    def info():
        return metrics + ' - ' + str(request_code.status_code)

def getMonitorData(rrd_file): 
    rrd_info = rrdtool.info(rrd_file)
    last_update = rrd_info['last_update'] - 60
    args = '-s ' + str(last_update) 
    results = rrdtool.fetch(rrd_file , 'AVERAGE' , args )
    if results and results[2] and results[2][0] and results[2][0][1] is not None:
        lost_package_num = int(results[2][0][1])
    else:
        lost_package_num = 0
    average_rrt = 0 if not results[2][0][2] else results[2][0][2] * 1000

    return lost_package_num , round(average_rrt , 4)

if __name__ == '__main__':
    rrd_data_dir = os.path.join(paras['data_dir'])
    for filename in os.listdir(rrd_data_dir):
        (instance , postfix) = os.path.splitext(filename)
        if postfix == '.rrd' :
            (lost_package_num , rrt) = getMonitorData(os.path.join(paras['data_dir'] , filename))
            pushMetrics(instance, 'rrt' , rrt)
            pushMetrics(instance, 'lost_package_num' , lost_package_num)
