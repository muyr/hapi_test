#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.11
# Email : muyanru345@163.com
###################################################################
from HART import HART
from HART_Auto import HART_Auto
from HART_Auto.ttypes import *
from thrift.transport import TTransport, TSocket
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from hdata import NodeType, PartType, AttributeOwner, ParmType
import os
ENV_OPTIONS = {
    'use_cooking_thread': True,  # 使用多线程进行 cook
    'cooking_thread_stack_size': -1,  # 设置线程的堆栈大小。要将堆栈大小设置为 Houdini 的默认值，请使用-1。这个值是字节单位。
    'houdini_environment_files': '',
    # 以":" 或"" 来连接多个路径(在 OS 上不同)。Houdini 的 user prefs 文件夹的 houdini. 遵循了与 env 文件相同的语法. 转换为 grub 文件
    'otl_search_path': '',
    'dso_search_path': '',
    'image_dso_search_path': '',
    'audio_dso_search_path': '',
}

class MAPIBase(object):
    def __init__(self, port, host="localhost"):
        super(MAPIBase, self).__init__()
        self._port = port
        self._host = host
        self._transport = None
        self._client = None
        self._cook_options = CookOptions()
        self.connect()

    def connect(self):
        if self._transport is None:
            socket = TSocket.TSocket(self._host, self._port)
            # using buffer to get faster transport
            self._transport = TTransport.TBufferedTransport(socket)
        # create client
        self._client = HART.Client(TBinaryProtocol(self._transport))
        # connect to server
        self._transport.open()

    def init(self):
        self._client.Initialize(self._cook_options, **ENV_OPTIONS)

    def load_hda(self, hda_file):
        load_result = self._client.LoadAssetLibraryFromFile(hda_file, False)
        count = self._client.GetAvailableAssetCount(load_result.library_id).asset_count
        if count > 1:
            raise Exception('Should only be loading 1 asset here')
        name_list = self._client.GetAvailableAssets(load_result.library_id, count)
        print name_list
        # 上面的目的就是获取 hda 或 otl 里面资产的名字，以便可以去实例化一个，
        # 如果已经约定知道了名字，可以无需去获取
        return self.get_string(name_list.asset_names_array[0])

    def get_string(self, string_handle):
        buffer_result = self._client.GetStringBufLength(string_handle)
        string_result = self._client.GetString(string_handle, buffer_result.buffer_length)
        return string_result.string_value

    def instance_hda(self, operator_name):
        create_result = self._client.CreateNode(parent_node_id=-1,
                                                operator_name=operator_name,
                                                node_label=self.get_valid_name(
                                                    os.path.basename(operator_name)),
                                                cook_on_creation=True)
        return create_result

    def get_valid_name(self, text):
        return ''.join([i if i.isalnum() else '_' for i in text])

    def disconnect(self):
        if self._client:
            self._client.Cleanup()
            self._transport.close()
