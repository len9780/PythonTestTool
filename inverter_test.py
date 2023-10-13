import json
import itertools
import ssl
import paho.mqtt.client as mqtt
import time


def mqtt_init(host_address,crt):
 client = mqtt.Client()
 client.tls_set(crt, tls_version=ssl.PROTOCOL_TLSv1_2)
 client.tls_insecure_set(True)
 client.connect(host_address, 1884, 10)
 return client
 
def send_mqtt_msg(client,topic,data):
  client.publish(topic, data)
def send_data(data,config_data,client_obj,topic):
 print(config_data['time_interval'])
 print(config_data['total_time'])
 print(round(float(config_data['total_time']/config_data['time_interval']))
)
 loop_cnt=round(float(config_data['total_time']/config_data['time_interval']))

 i_cnt=0
 while i_cnt<(loop_cnt-1):
  for i in dat:
    if i_cnt>(loop_cnt-1):
        break
    #print(i,end='\n\n')
    print(i)
    #print("cnt:"+str(i_cnt))
    send_mqtt_msg(client_obj,topic,str(i).replace("'", '"') )
    i_cnt+=1
    time.sleep(int(config_data['time_interval']))

def make_req_msg(cmd, data, data_len):
    send=[]
    j={}
#    j['cmd'] = cmd
    sub_data={}
    print(data_len)
    for i in data:
     if (i[0]=='S'):
          j['cmd'] = "setReg"
          j['reg']=i
          j['val']=data[i]
          j['cmdid']="123aa"
          send.append(str(j))
          #print(j.copy())
     else:
         if (i[0]=='M'):
          j.clear()
          #if 'reg' in j:
          #  del j['reg']
          #sub_data[i]=data[i]
          #print(i)
          sub_data.clear()
          sub_data[i]=data[i]
#          print("-----")
#          print(sub_data)
#          print("-----")
          j['cmd'] = "setMultiReg"
          j['val']=sub_data
          j['cmdid']="123aa"
          #send.append(j.copy())
          send.append(str(j))
          #print(j.copy())
    #print(send)
     #print("------")
    #print(send)
    return send
"""
#    # print(data)
#    # print(data_len)
#    all_combination = []
#    for i in range(1, data_len + 1):
#       # print("data_len")
#        #permutations = set(list(itertools.permutations(data, i)))
#        #remove duplicate item with set
#        all_combination.append(set(list(itertools.combinations(data, i))))
#        #print(str(i) + ":", end="")
#        #print(all_combination, end='\n')
#    for n in all_combination:
#        for nn in n:
#        #    print(str(",".join(nn)))# + str(type(",".join(nn))))
#            j['node_name']+=nn
#            print(j['node_name'])
#            #print(json.dumps(j,indent=4))
#            send.append(json.dumps(j,indent=4))
#            j['node_name'].clear()
#    print(len(send))
#    print(send)
"""


jsonfile = open('test_data.json', 'r')
# print(type(jsonfile))
# a = json.load(jsonfile)
data = json.load(jsonfile)

#dat = make_req_msg("get_node_info", data['vals'], len(data['vals']))
#print(data['set_cmd_vals'])
dat = make_req_msg("setReg", data['set_cmd_vals'], len(data['set_cmd_vals']))
#print(dat[0])
#print(dat[1])
#print(dat)
client_obj = mqtt_init("gw01.cwoiot.com","./cert.crt")
send_data(dat,data,client_obj,data['mqtt_topic'])
