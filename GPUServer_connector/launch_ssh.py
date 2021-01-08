#!/usr/bin/python3.8

import json
from colab_ssh import launch_ssh
from colab_ssh import get_tunnel_config



launch_ssh('1ih6ACosTCp4vtqmz0kMEObj6US_4WKtwytKGHJxCH6DThVfr', '777')

f = open("/content/connection/service_server_connection_info", "w")
f.write(json.dumps(get_tunnel_config()))
f.close()
