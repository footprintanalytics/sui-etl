from blockchainetl_common.graph.graph_operations import Point
from suietl.service.service import Service


class SuiBlockTimestampGraph:
    def __init__(self, rpc):
        self._service = Service(rpc)

    def get_first_point(self):
        number, block = self._service.get_genesis_checkpoint_timestamp()
        print(number, block)
        return self.block_to_point(number, block)

    def get_last_point(self):
        number, block = self._service.get_latest_checkpoint_timestamp()
        print(number, block)
        return self.block_to_point(number, block)

    def get_point(self, block_number):
        number, block = self._service.get_checkpoint_timestamp(block_number)
        return self.block_to_point(number, block)

    def get_points(self, block_numbers):
        return [self.block_to_point(number, self._service.get_checkpoint_timestamp(number)) for number in block_numbers]

    @staticmethod
    def block_to_point(number, timestamp):
        return Point(number, timestamp)
