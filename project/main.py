# -*- coding: utf-8 -*-
# Micropython wemos d1 mini with SHT30 temperature sensor on mqtt
# Copyright (C) 2017  Costas Tyfoxylos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from umqtt.simple import MQTTClient
import ujson
import esp
import time
import machine


def main():
    topic = configuration.get('topic')
    submit_interval = configuration.get('submit_interval')
    exception_timeout = configuration.get('exception_reset_timeout')
    try:
        client = MQTTClient(client_id, mqtt_server_ip)
        client.connect()
        print('Connected to {}'.format(mqtt_server_ip))
        temperature, humidity = sensor.measure()
        info = {'temperature': temperature,
                'humidity': humidity}
        client.publish(topic, ujson.dumps(info))
        client.disconnect()
        print('sleeping deeply for {} seconds'.format(submit_interval))
        # deep sleep argument in microseconds
        esp.deepsleep(submit_interval * 1000000)
    except Exception as e:
        print(('Caught exception, {}'
               'resetting in {} seconds...').format(e, exception_timeout))
        time.sleep(exception_timeout)
        machine.reset()

if __name__ == '__main__':
    main()
