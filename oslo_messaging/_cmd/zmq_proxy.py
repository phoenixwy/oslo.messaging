#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import logging

from oslo_config import cfg

from oslo_messaging._drivers import impl_zmq
from oslo_messaging._drivers.zmq_driver.broker import zmq_proxy
from oslo_messaging._drivers.zmq_driver.broker import zmq_queue_proxy
from oslo_messaging import server

CONF = cfg.CONF
CONF.register_opts(impl_zmq.zmq_opts)
CONF.register_opts(server._pool_opts)
CONF.rpc_zmq_native = True


USAGE = """ Usage: ./zmq-proxy.py [-h] [] ...

Usage example:
 python oslo_messaging/_cmd/zmq-proxy.py"""


def main():
    parser = argparse.ArgumentParser(
        description='ZeroMQ proxy service',
        usage=USAGE
    )

    parser.add_argument('--config-file', dest='config_file', type=str,
                        help='Path to configuration file')
    parser.add_argument('-d', '--debug', dest='debug', type=bool,
                        default=False,
                        help="Turn on DEBUG logging level instead of INFO")
    args = parser.parse_args()

    if args.config_file:
        cfg.CONF(["--config-file", args.config_file])

    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(name)s '
                               '%(levelname)-8s %(message)s')

    reactor = zmq_proxy.ZmqProxy(CONF, zmq_queue_proxy.UniversalQueueProxy)

    try:
        while True:
            reactor.run()
    except (KeyboardInterrupt, SystemExit):
        reactor.close()

if __name__ == "__main__":
    main()
