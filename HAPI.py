#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.10
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

NICE_RESULT = [
    u'成功',  # HAPI_RESULT_SUCCESS
    u'失败',  # HAPI_RESULT_FAILURE
    u'已经初始化过了',  # HAPI_RESULT_ALREADY_INITIALIZED
    u'未初始化',  # HAPI_RESULT_NOT_INITIALIZED
    u'无法加载文件',  # HAPI_RESULT_CANT_LOADFILE
    u'参数设置失败',  # HAPI_RESULT_PARM_SET_FAILED
    u'无效参数',  # HAPI_RESULT_INVALID_ARGUMENT
    u'无法加载 Geo',  # HAPI_RESULT_CANT_LOAD_GEO
    u'无法生成预设',  # HAPI_RESULT_CANT_GENERATE_PRESET
    u'无法加载预设',  # HAPI_RESULT_CANT_LOAD_PRESET
    u'资产已被加载',  # HAPI_RESULT_ASSET_DEF_ALREADY_LOADED
    u'无许可',  # HAPI_RESULT_NO_LICENSE_FOUND
    u'不允许使用非商用许可',  # HAPI_RESULT_DISALLOWED_NC_LICENSE_FOUND
    u'不允许使用非商用资产',  # HAPI_RESULT_DISALLOWED_NC_ASSET_WITH_C_LICENSE
    u'不允许非商用资产使用LC许可',  # HAPI_RESULT_DISALLOWED_NC_ASSET_WITH_LC_LICENSE
    u'LIC 错误',  # HAPI_RESULT_DISALLOWED_LC_ASSET_WITH_C_LICENSE
    u'不允许的第三方插件',  # HAPI_RESULT_DISALLOWED_HENGINEINDIE_W_3PARTY_PLUGIN
    u'资产不合法',  # HAPI_RESULT_ASSET_INVALID
    u'节点不合法',  # HAPI_RESULT_NODE_INVALID
    u'用户阻止',  # HAPI_RESULT_USER_INTERRUPTED
    u'场景文件不合法',  # HAPI_RESULT_INVALID_SESSION
]
NICE_STATE = [
    u'Cook 成功',  # HAPI_STATE_READY
    u'Cook 失败，有致命错误',  # HAPI_STATE_READY_WITH_FATAL_ERRORS
    u'Cook 失败，有个别节点错误',  # HAPI_STATE_READY_WITH_COOK_ERRORS
    u'开始 Cook',  # HAPI_STATE_STARTING_COOK
    u'正在 Cook',  # HAPI_STATE_COOKING
    u'开始加载',  # HAPI_STATE_STARTING_LOAD
    u'加载中',  # HAPI_STATE_LOADING
    u'已达到最大限度',  # HAPI_STATE_MAX
    u'准备达到最大限度',  # HAPI_STATE_MAX_READY_STATE
]


class MAPI(object):
    def __init__(self, port, host="localhost"):
        super(MAPI, self).__init__()
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

    def save_to_hip(self, hip_file):
        save_result = self._client.SaveHIPFile(hip_file, False)
        return save_result

    def disconnect(self):
        if self._client:
            self._client.Cleanup()
            self._transport.close()

    def get_asset_info(self, node_id):
        return self._client.GetAssetInfo(node_id=node_id).asset_info

    def printCompleteNodeInfo(self, node_id):
        info_result = self._client.GetNodeInfo(node_id)
        node_info = info_result.node_info
        object_info_list = []
        if (node_info.type == NodeType.SOP):
            # For pure SOP asset, a parent object will be created automatically,
            # so use parent's ID to get the object info
            object_info_list.append(self._client.GetObjectInfo(node_info.parentId).object_info)
        elif (node_info.type == NodeType.OBJ):
            # This could have children objects or not.
            # If has children, get child object infos.
            # If no children, presume this node is the only object.
            object_count = self._client.ComposeObjectList(parent_node_id=node_info.parentId,
                                                          categories=None).object_count
            if (object_count > 0):
                object_info_list = self._client.GetComposedObjectList(
                    parent_node_id=node_info.parentId,
                    start=0,
                    length=object_count).object_infos_array
            else:
                object_info_list.append(self._client.GetObjectInfo(node_id=node_id).object_info)
        else:
            print "Unsupported node type: ", node_info.type
            return
        for object_info in object_info_list:
            geo_info = self._client.GetDisplayGeoInfo(object_info.nodeId).geo_info
            for part_index in range(geo_info.partCount):
                self.processGeoPart(object_info.nodeId, geo_info.nodeId, part_index)

    def processGeoPart(self, object_node_id, geo_node_id, part_id):
        print "Object: {}, Geo: {}, Part: {}".format(object_node_id, geo_node_id, part_id)
        part_info = self._client.GetPartInfo(geo_node_id, part_id).part_info
        name_list = self._client.GetAttributeNames(node_id=geo_node_id,
                                                   part_id=part_info.id,
                                                   owner=AttributeOwner.POINT,
                                                   count=part_info.attributeCounts[
                                                       AttributeOwner.POINT]).attribute_names_array
        print 'Attribute names:', [self.get_string(name_list[i])
                                   for i in range(part_info.attributeCounts[AttributeOwner.POINT])]

        print "Point Positions: "
        self.processFloatAttrib(geo_node_id, part_id, AttributeOwner.POINT, "P")

        print "Number of Faces: ", part_info.faceCount
        if (part_info.type != PartType.CURVE):
            faceCounts = self._client.GetFaceCounts(geo_node_id, part_id, 0,
                                                    part_info.faceCount).face_counts_array
            print 'faces list:', faceCounts
            vertexList = self._client.GetVertexList(geo_node_id, part_id, 0,
                                                    part_info.vertexCount).vertex_list_array
            print "Vertex Indices into Points array:"
            curr_index = 0
            for ii in range(part_info.faceCount):
                for jj in range(faceCounts[ii]):
                    print  "Vertex:[", curr_index, "], belonging to face: ", ii, ", index: ", \
                        vertexList[curr_index], " of points array"
                    curr_index += 1

    def processFloatAttrib(self, geo_node_id, part_id, owner, name):
        attrib_info = self._client.GetAttributeInfo(node_id=geo_node_id,
                                                    part_id=part_id,
                                                    name=name,
                                                    owner=owner).attr_info
        attrib_data = self._client.GetAttributeFloatData(node_id=geo_node_id,
                                                         part_id=part_id,
                                                         name=name,
                                                         attr_info=attrib_info,
                                                         stride=-1,
                                                         start=0,
                                                         length=attrib_info.count).data_array
        for elem_index in range(attrib_info.count):
            print '\t', attrib_data[elem_index * attrib_info.tupleSize: (
                                                                                    elem_index + 1) * attrib_info.tupleSize]

    def cook(self, node_id):
        self._client.CookNode(node_id=node_id, cook_options=self._cook_options)
