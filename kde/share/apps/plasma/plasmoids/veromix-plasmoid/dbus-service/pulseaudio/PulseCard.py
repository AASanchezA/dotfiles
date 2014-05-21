# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Nik Lutz <nik.lutz@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from .lib_pulseaudio import *
from VeromixUtils import *

class CardProfile:

    def __init__(self, card_info):
        self.name =  in_unicode(card_info.name)
        self.description =  in_unicode(card_info.description)
        self.n_sinks =  int(card_info.n_sinks)
        self.n_sources =  int(card_info.n_sources)
        self.priority =  int(card_info.priority)
        #print "got profile",  self.name, self.description, self.n_sinks, self.n_sources, self.priority

    def as_dict(self):
        info = {}
        info["name"] = in_unicode(self.name)
        info["description"] = in_unicode(self.description)
        info["n_sinks"] = in_unicode(self.n_sinks)
        info["n_sources"] = in_unicode(self.n_sources)
        info["priority"] = in_unicode(self.priority)
        return info

class CardInfo:

    def __init__(self, pa_card_info):
        self.index = int(pa_card_info.index)
        self.name = in_unicode(pa_card_info.name)
        self.owner_module = in_unicode(pa_card_info.owner_module)
        self.driver = in_unicode(pa_card_info.driver)
        self.n_profiles = int(pa_card_info.n_profiles)

        self.active_profile = CardProfile(pa_card_info.active_profile[0])
        self.proplist_string = in_unicode(pa_proplist_to_string(pa_card_info.proplist))
        self.proplist = proplist_to_dict(self.proplist_string)
        #print self.proplist
        #self.proplist = pa_card_info.proplist
        #print "got card", self.index, self.name, self.active_profile
        self.profiles = []
        for index in range(0, self.n_profiles):
            profile = pa_card_info.profiles[index]
            if profile:
                self.profiles.append(CardProfile(profile))

    def properties(self):
        # FIXME
        info = {}
        #info["owner_module"] = self.owner_module
        for key in list(self.proplist.keys()):
            info[key] = self.proplist[key]
        return info

    def active_profile_name(self):
        return in_unicode(self.active_profile.name)


    def profiles_dict(self):
        info = {}
        for profile in self.profiles:
            info[profile.name] = profile.as_dict()
        return info
