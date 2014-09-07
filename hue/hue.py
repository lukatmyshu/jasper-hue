import collections
import phue
import re
import logging


WORDS = ["LIGHTS", "LIGHT"]
#"Turn the" [identifier] [light/lights] [on/off]
pattern = r'Turn the (\w*) lights? (on|off)'

hue_bridge = "192.168.1.67"

def create_groups(bridge):
    groups = bridge.get_group()
    return dict((v["name"].lower(), k) for k,v in groups.items())

LightAction = collections.namedtuple("LightAction", ["light_group", "action"])
class InvalidGroupError(ValueError):
    def __init__(self, group, msg):
        self.group = group
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

def _handle(bridge, text):
    match = re.search(pattern, text)
    if not match:
        logging.warn("Invalid text: %s", text)
        raise ValueError("Invalid text: %s", text)

    light_group = match.groups()[0].lower()
    action = match.groups()[1].lower()

    logging.info("Light class: %s action %s", light_group, action)

    groups = create_groups(bridge)

    if light_group not in groups:
        raise InvalidGroupError("%s is not a valid group", light_group)

    group_id = groups[light_group]
    logging.info("Activating group %s" % group_id)

    bridge.set_group(group_id, "on", action == "on")
    return LightAction(group_id, action)

def handle(text, mic, profile):
    bridge = phue.Bridge(hue_bridge)
    try:
        light_group, action = _handle(bridge, text)
        mic.say("Turning %s lights %s", light_group, action)
    except InvalidGroupError, e:
        group = e.group
        mic.say("Invalid group %s" % group)
    except ValueError:
        mic.say("I'm sorry, I didn't understand that")

def isValid(text):
    return bool(re.search(pattern, text, re.IGNORECASE))
