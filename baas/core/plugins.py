#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import new
from util import text
from baas import plugins

class PluginLoader(object):

    def __init__(self):
        self.plugins = {}
        self.help = ''
        self.commands = {}

    def load_plugins(self):
        """
            loads the plugins from the plugin dir
        """
        for file in os.listdir(plugins.__path__[0]):
            file_parts = os.path.splitext(file)
            if  file_parts[1] == '.py' and file[0:2] != '__':
                self.plugins[file_parts[0].capitalize()] = getattr(__import__('baas.plugins.'+file_parts[0], globals(), locals(),[file_parts[0].capitalize()]),file_parts[0].capitalize())()

    def load_map(self):
        """
            combines command map
        """
        for name in self.plugins:
            cmd_map = self.plugins[name].get_map()
            if cmd_map:
                for (cmd,func) in cmd_map:
                    self.commands[cmd] = func

    def load_help(self):
        """
            combines help text, retrieved from the plugins
        """
        help_infos = {}
        help_list = []
        help_additional = []
        for name in self.plugins:
            help_info = self.plugins[name].get_help()
            if help_info:
                help_infos[name] = help_info

        for h in help_infos:
            for t in help_infos[h].get('commands'):
                help_list.append(t)
            for a in help_infos[h].get('additional'):
                help_additional.append(a)

        self.help = "\n".join(help_list)
        self.help += "\n%s" % "\n".join(help_additional)           

class Plugin(object):

    def __init__(self):
        pass

    def get_map(self):
        return None

    def get_help(self):
        return None

    def strip_tags(self, value):
        """
            Return the given HTML with all tags stripped.
        """
        return re.sub(r'<[^>]*?>', '', value)        

    def overlap_link(self, r1, r2):
        """
            overlaps rows by link
        """
        return r1['link'].strip() == r2['link'].strip()

    def overlap_title(self, r1, r2):
        """
            overlaps rows by title
        """
        return text.overlap(r1["title"], r2["title"]) > 1
