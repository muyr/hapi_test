#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.11
# Email : muyanru345@163.com
###################################################################

from base import MAPIBase


class NodeFlags(object):
    """Equivalent of HAPI's HAPI_NodeFlags
    """
    ANY = -1
    NONE = 0
    DISPLAY = 1 << 0
    RENDER = 1 << 1
    TEMPLATED = 1 << 2
    LOCKED = 1 << 3
    EDITABLE = 1 << 4
    BYPASS = 1 << 5
    NETWORK = 1 << 6

    OBJ_GEOMETRY = 1 << 7
    OBJ_CAMERA = 1 << 8
    OBJ_LIGHT = 1 << 9
    OBJ_SUBNET = 1 << 10

    SOP_CURVE = 1 << 11
    SOP_GUIDE = 1 << 12

    TOP_NONSCHEDULER = 1 << 13


class HandleNodeAPI(MAPIBase):
    ANY = -1
    NONE = 0
    OBJ = 1 << 0
    SOP = 1 << 1
    CHOP = 1 << 2
    ROP = 1 << 3
    SHOP = 1 << 4
    COP = 1 << 5
    VOP = 1 << 6
    DOP = 1 << 7
    TOP = 1 << 8

    def __init__(self, port=9090):
        super(HandleNodeAPI, self).__init__(port=port)
        self.init()

    def test(self):
        op_name = self.load_hda(
            'd:/github/hapi_test/data/examples/HAPI_Test_Nodes_EditableNodeNetwork.hda')
        print 'Step 1. Load HDA/OTL File, get asset name:\n\t', op_name
        root_node_id = self.instance_hda(op_name).new_node_id
        print 'Step 2. Instance asset, new node id:\n\t', root_node_id

        # Get the editable node network node id.
        count = self._client.ComposeChildNodeList(
            parent_node_id=root_node_id,
            node_type_filter=HandleNodeAPI.ANY,
            node_flags_filter=NodeFlags.EDITABLE | NodeFlags.NETWORK,
            recursive=True).count
        print 'Step 3. The count of editable network:\n\t', count

        composed_child_id_list = self._client.GetComposedChildNodeList(parent_node_id=root_node_id,
                                                                    count=count).child_node_ids_array
        # print composed_child_list
        print 'Step 4. The editable networks ids:\n\t', composed_child_id_list
        network_id = composed_child_id_list[0]
        # Get the editable node network info.
        network_node_info = self._client.GetNodeInfo(node_id=network_id).node_info
        print 'Step 5. The network\' child node count is:\n\t', network_node_info.childNodeCount

        sub_node_count = self._client.ComposeChildNodeList(
            parent_node_id=network_id,
            node_type_filter=HandleNodeAPI.ANY,
            node_flags_filter=NodeFlags.ANY,
            recursive=True).count
        child_node_ids = self._client.GetComposedChildNodeList(
            parent_node_id=network_id,
            count=sub_node_count).child_node_ids_array
        # Get node id of our merge SOP.
        print 'Step 6. Child node names:\n\t'
        for c_id in child_node_ids:
            c_info = self._client.GetNodeInfo(node_id=c_id).node_info
            print '\t', self.get_string(c_info.nameSH)

        # Create a node.
        box_node_id = self._client.CreateNode(
            parent_node_id=network_id,
            operator_name="box",
            node_label='',
            cook_on_creation=True).new_node_id
        print 'Step 7. Create a box node, id is:\n\t', box_node_id
        # Get and verify the box node info.
        box_node_info = self._client.GetNodeInfo(node_id=box_node_id).node_info
        print 'Step 8. The box node\'s parent node id is:\n\t', network_id
        print 'Step 9. The box node is createdPostAssetLoad?\n\t', box_node_info.createdPostAssetLoad

        # Check new child count.
        network_node_info = self._client.GetNodeInfo(node_id=network_id).node_info
        print 'Step 10. Now the network\'s child node count is:\n\t', network_node_info.childNodeCount

        merge_node_id = child_node_ids[-1]
        # print ''
        # First query should return nothing at index 1.
        query_result = self._client.QueryNodeInput(node_to_query=merge_node_id, input_index=1)
        print 'Step 11. The merge node\'s second input is:', query_result.connected_node_id
        # Connect the box to our merge SOP.
        result = self._client.ConnectNodeInput(node_id=merge_node_id,
                                               input_index=1,
                                               node_id_to_connect=box_node_id,
                                               output_index=0)
        print 'Step 12. Connect the box node to merge node', result

        # Second query should return the box.
        result = self._client.QueryNodeInput(node_to_query=merge_node_id, input_index=1)
        print 'Step 13. Now the merge node\'s second input is:', result.connected_node_id
        # Disconnect the box.
        result = self._client.DisconnectNodeInput(node_id=merge_node_id, input_index=1)
        print 'Step 14. Disconnect.', result
        # Thrid query, after the disconnect, should again return nothing.
        result = self._client.QueryNodeInput(node_to_query=merge_node_id, input_index=1)
        print 'Step 13. Now the merge node\'s second input is:', result.connected_node_id

        result = self._client.DeleteNode(node_id=box_node_id)
        # print result
        print 'Step 14. Delete the box node.', result

if __name__ == '__main__':
    api = HandleNodeAPI()
    api.test()
