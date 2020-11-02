import sys
import os
from HART import HART
from HART_Auto import HART_Auto
from HART_Auto.ttypes import *
from thrift.transport import TTransport, TSocket
from thrift.protocol.TBinaryProtocol import TBinaryProtocol


#***************************Thrift*****************************
host = "localhost"
port = "9090"
    #making socket
socket = TSocket.TSocket(host, port)
    #using buffer to get faster transport
transport = TTransport.TBufferedTransport(socket)
    #using Convert to Binary protocol
protocol = TBinaryProtocol(transport)
    #create client
client = HART.Client(protocol)
    #connect to server
try:
    transport.open()
except:
    print("Connection Error!!")

# print(help(client.LoadAssetLibraryFromFile))
    #init session
cook_options = CookOptions()
client.Initialize(cook_options, True, -1,"","","","","")
VGeo = client.CreateNode(-1, "Object/geo", "Hello_Houdini_Engine_Geo", True).new_node_id
# result = client.LoadAssetLibraryFromFile('d:/mu_ref/thrift/pyhapi/FourShapes.hda', False)
# count = client.GetAvailableAssetCount(result.library_id).asset_count
# name_list = client.GetAvailableAssets(result.library_id, count).asset_names_array
# for i in range(count):
#     print(name_list[i])
#     print(client.GetString(name_list[i], 18))
# client.GetString()

# # VGeo = client.Load(-1, "Object/geo", "Validation_Geo", True).new_node_id
# client.SaveHIPFile(os.path.join("d:/","Debug2.hip"),False)
# client.Cleanup()
# transport.close()
