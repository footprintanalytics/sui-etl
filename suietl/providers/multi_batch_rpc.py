# The MIT License (MIT)
#
# Copyright (c) 2016 Piper Merriam
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import threading
import time
from typing import (
    Any,
    Optional,
    Union, List,
)

from eth_typing import (
    URI,
)
from web3 import HTTPProvider
from web3._utils.request import make_post_request

lock = threading.Lock()


class NoActiveProviderError(Exception):
    """Base exception if all providers are offline"""


class EndpointStatus():
    endpoint_url: Union[URI, str]
    status: str
    err_code: Optional[int]
    fail_time: Optional[int]

    def __init__(self, endpoint_url: Union[URI, str]):
        self.endpoint_url = endpoint_url
        self.status = 'active'

    def fail_pass_time(self):
        return int(time.time()) - self.fail_time

    def is_active(self):
        if self.status == 'active':
            return True
        elif self.status == 'failed':
            if self.err_code == 429 and self.fail_pass_time() > 60 * 10:
                self.status = 'active'
                return True
            if self.err_code in [400, 500] and self.fail_pass_time() > 60 * 1:
                self.status = 'active'
                return True
        return False

    def fail(self, err_code: int):
        self.fail_time = int(time.time())
        self.status = 'failed'
        self.err_code = err_code
        pass


class EndpointManager():
    logger = logging.getLogger("etl.providers.EndpointManager")
    call_times: int = 0
    _current_endpoint_index: int = 0
    _last_working_provider_index: int = 0

    def __init__(self, endpoint_urls: List[Union[URI, str]]) -> None:
        self._hosts_uri = endpoint_urls
        self._endpoints_len = len(self._hosts_uri)
        self._endpoints = [EndpointStatus(endpoint_url) for index, endpoint_url in enumerate(endpoint_urls)]
        self.endpoint = self._endpoints[0]
        self.endpoint_uri = self.endpoint.endpoint_url

    def get_next_active_endpoint(self, depth=0):
        if depth > (self._endpoints_len * 2):
            raise NoActiveProviderError("No active provider")
        with lock:
            self._current_endpoint_index = (self._current_endpoint_index + 1) % self._endpoints_len
        endpoint = self._endpoints[self._current_endpoint_index]
        if not endpoint.is_active():
            return self.get_next_active_endpoint(depth + 1)
        # self.logger.info("change endpoint to : %s,  index: %s ", endpoint.endpoint_url, self._current_endpoint_index)
        self.display_endpoint_stats()
        return endpoint

    def display_endpoint_stats(self):
        self.call_times = (self.call_times + 1) % 200
        if self.call_times == 0:
            active_ = [index for index, endpoint in enumerate(self._endpoints) if endpoint.is_active()]
            self.logger.info("active endpoints %s ", active_)
            not_active_ = [endpoint.endpoint_url for index, endpoint in enumerate(self._endpoints) if
                           not endpoint.is_active()]
            self.logger.info("not active endpoints %s ", '\n'.join(not_active_))


# Mostly copied from web3.py/providers/rpc.py. Supports batch requests.
# Will be removed once batch feature is added to web3.py https://github.com/ethereum/web3.py/issues/832
class BatchMultiHTTPProvider(HTTPProvider):
    def __init__(
            self, endpoint_manager: EndpointManager = None,
            request_kwargs: Optional[Any] = None,
            session: Optional[Any] = None
    ) -> None:
        super().__init__(endpoint_manager.endpoint_uri, request_kwargs, session)
        self.endpoint_manager = endpoint_manager
        self.endpoint = self.endpoint_manager.get_next_active_endpoint()

    def make_batch_request(self, text):
        # self.logger.info("Making request HTTP. URI: %s ",self.endpoint.endpoint_url)
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                          self.endpoint.endpoint_url, text)
        request_data = text.encode('utf-8')
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        self.endpoint = self.endpoint_manager.get_next_active_endpoint()
        try:
            raw_response = make_post_request(
                self.endpoint.endpoint_url,
                request_data,
                headers=headers,
                timeout=10
            )
            response = self.decode_rpc_response(raw_response)
            self.logger.debug("Getting response HTTP. URI: %s, "
                              "Request: %s, Response: %s",
                              self.endpoint.endpoint_url, text, response)

            # block_numbers = set()
            if response and 'error' in response:
                raise ValueError(response['error']['message'])
            return response, self.endpoint.endpoint_url
        except Exception as error:  # pylint: disable=W0703
            self.logger.warning(
                {
                    "error": str(error),
                    "provider": self.endpoint.endpoint_url,
                }
            )
            error_code = 400
            if 'Too Many Requests' in str(error):
                error_code = 429
            if 'not support json rpc' in str(error) or 'return none data' in str(error):
                error_code = 500
            self.endpoint.fail(error_code)

            return self.make_batch_request(text)
