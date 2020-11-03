#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.11
# Email : muyanru345@163.com
###################################################################

from base import MAPIBase


class HandleGroupAPI(MAPIBase):
    INVALID = -1
    POINT = 0
    PRIM = 1
    MAX = 2

    def __init__(self, port=9090):
        super(HandleGroupAPI, self).__init__(port=port)
        self.init()

    def test(self):
        op_name = self.load_hda('d:/github/hapi_test/data/examples/HAPI_Test_Groups_AllTypes.hda')
        print 'Step 1. Load HDA/OTL File, get asset name:\n\t', op_name
        root_node_id = self.instance_hda(op_name).new_node_id
        print 'Step 2. Instance asset, new node id:\n\t', root_node_id

        object_info = self._client.GetObjectInfo(node_id=root_node_id).object_info
        print 'Step 3. Get object info:\n\t', object_info
        geo_info = self._client.GetDisplayGeoInfo(object_info.nodeId).geo_info
        print 'Step 4. Get geo info:\n\t', geo_info

        # 获取 group 们的名字
        point_group_names = self._client.GetGroupNames(
            node_id=geo_info.nodeId,
            group_type=HandleGroupAPI.POINT,
            group_count=geo_info.pointGroupCount).group_names_array
        point_group_names = map(self.get_string, point_group_names)
        print 'Step 5. Get [Point] groups name: \n\t', point_group_names
        primitive_group_names = self._client.GetGroupNames(
            node_id=geo_info.nodeId,
            group_type=HandleGroupAPI.PRIM,
            group_count=geo_info.primitiveGroupCount).group_names_array
        primitive_group_names = map(self.get_string, primitive_group_names)
        print 'Step 5. Get [Primitive] groups name:\n\t', primitive_group_names

        # Get part info.
        for part_index in range(geo_info.partCount):
            part_info = self._client.GetPartInfo(node_id=geo_info.nodeId,
                                                 part_id=part_index).part_info
            print 'Step 6. Get Part info:\n\t', part_info
            # Get group partial membership.
            for point_grp in point_group_names:
                partial_group_membership = self._client.GetGroupMembership(
                    node_id=geo_info.nodeId,
                    part_id=part_index,
                    group_type=HandleGroupAPI.POINT,
                    group_name=point_grp,
                    start=0,
                    length=part_info.pointCount).membership_array

                # Check membership.
                print 'Step 7: Get [Point] group membership:\n\t', point_grp, partial_group_membership
            # Get group full membership.
            for prim_grp in primitive_group_names:
                primitive_group_membership = self._client.GetGroupMembership(
                    node_id=geo_info.nodeId,
                    part_id=part_index,
                    group_type=HandleGroupAPI.PRIM,
                    group_name=prim_grp,
                    start=0,
                    length=part_info.faceCount).membership_array
                print 'Step 7: Get [Primitive] group membership:\n\t', prim_grp, primitive_group_membership


if __name__ == '__main__':
    api = HandleGroupAPI()
    api.test()
