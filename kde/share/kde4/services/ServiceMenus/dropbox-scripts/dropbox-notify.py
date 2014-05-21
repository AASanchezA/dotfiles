#!/usr/bin/python
# originally script found at http://forum.kde.org/viewtopic.php?f=66&t=23580

import dbus
from optparse import OptionParser

def main():
   parser = OptionParser(usage="%prog [options] <summary> [body]", version="%prog 0.1")
   parser.add_option("-a", "--app", dest="app_name", help="Specifies the application name.", default="notify-dbus.py")
   parser.add_option("-i", "--icon", dest="icon", help="Specifies an icon filename or stock icon to display.", default="")
   parser.add_option("-t", "--expire-timeout", type="int", dest="timeout", help="Specifies the timeout in milliseconds at which to expire the notification.", default=0)
   (options, args) = parser.parse_args()
   if len(args) < 1:
      parser.error("No summary specified.")
   if len(args) > 1:
       BODY = args[1]
   else:
       BODY = ""
   dbus = DBus()
   dbus.notify(app_name=options.app_name, app_icon=options.icon, summary=args[0], body=BODY, timeout=options.timeout)

class DBus():
   """Wrapper class for notify daemon dbus interface"""

   def __init__(self):
      self.__notify = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
      self.__iface = dbus.Interface(self.__notify, "org.freedesktop.Notifications")

   def notify(self, app_name='', replaces_id=dbus.UInt32(), app_icon='', summary='', body='', actions=dbus.Array(signature="s"), hints=dbus.Dictionary(signature="sv"), timeout=0):
      self.__iface.Notify(app_name, replaces_id, app_icon, summary, body, actions, hints, timeout)

if __name__ == "__main__":
   main();
