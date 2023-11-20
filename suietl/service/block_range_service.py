
from suietl.service.block_timestamp_graph import SuiBlockTimestampGraph
from base.service.graph_operations import GraphOperations
from base.service.block_range_service import BlockRangeService


class SuiBlockRangeService(BlockRangeService):
    def __init__(self, rpc):
        graph = SuiBlockTimestampGraph(rpc)
        self._graph_operations = GraphOperations(graph)

