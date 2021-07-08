from mycroft import MycroftSkill, intent_file_handler


class WyzeThermostat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('thermostat.wyze.intent')
    def handle_thermostat_wyze(self, message):
        self.speak_dialog('thermostat.wyze')


def create_skill():
    return WyzeThermostat()

