from mycroft import MycroftSkill, intent_file_handler

import os
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
from wyze_sdk.models.devices import ThermostatSystemMode
from wyze_sdk.models.devices import ThermostatSystemMode

def login(self):
    username = self.settings.get('wyze_username')
    password = self.settings.get('wyze_password')
    client = Client(email=username, password=password)
    self.log.info("Logging in for " + username)
    return client


class WyzeThermostat(MycroftSkill):
    client = None
    device = None

    def get_thermostat():
        try:
            response = client.devices_list()
            for device in client.devices_list():
                if device.product.model == "CO_EA1":
                    print(repr(device))
                    return device
                break
        except WyzeApiError as e:
            # You will get a WyzeApiError is the request failed
            print(f"Got an error: {e}")
        return None

    def __init__(self):
        MycroftSkill.__init__(self)
        client = login(self)
        device = get_thermostat()

    @intent_file_handler('read_temperature.intent')
    def handle_thermostat_read_temperature(self, message):
        client = login(self)
        thermostat = client.thermostats.info(device_mac=device.mac)
        self.speak_dialog('read_temperature', data={"temperature": str(thermostat.temperature)})

    @intent_file_handler('read.intent')
    def handle_thermostat_read(self, message):
        client = login(self)
        thermostat = client.thermostats.info(device_mac=device.mac)
        if thermostat.time2temp_val > 0:
            self.speak_dialog('read_with_time', data={"temperature": str(thermostat.cool_sp), "time": str(thermostat.time2temp_val)})
        else:
            self.speak_dialog('read', data={"temperature": str(thermostat.cool_sp)})

    @intent_file_handler('set.intent')
    def handle_thermostat_set(self, message):
        client = login(self)
        numbers = [int(i) for i in message.utterance.split() if i.isdigit()]
        if len(numbers) > 0:
            cooling_setpoint=numbers[0]
            client.thermostats.set_cooling_setpoint(device_mac=device.mac, device_model="CO_EA1",
                                                          cooling_setpoint=cooling_setpoint)
        thermostat = client.thermostats.info(device_mac=device.mac)
        if thermostat.time2temp_val > 0:
            self.speak_dialog('read_with_time', data={"temperature": str(thermostat.cool_sp), "time": str(thermostat.time2temp_val)})
        else:
            self.speak_dialog('read', data={"temperature": str(thermostat.cool_sp)})

def create_skill():
    return WyzeThermostat()

