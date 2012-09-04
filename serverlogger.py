# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# serverlogger - parses server logs (tf2 only currently)
# Copyright (c) 2012 Gavin Langdon <puttabutta@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#------------------------------------------------------------------------------



import SourceLib


class GameserverLogger(SourceLib.SourceLog.SourceLogParser):
  def __init__(self, servermanager, server):
    SourceLib.SourceLog.SourceLogParser.__init__(self)
    self.server = server
    self.manager = servermanager

    self.objects = { 'OBJ_SENTRYGUN_MINI' : 'Mini-sentry',
        'OBJ_ATTACHMENT_SAPPER' : 'Sapper',
        'OBJ_DISPENSER' : 'Dispenser',
        'OBJ_SENTRYGUN' : 'Sentry',
        'OBJ_TELEPORTER' : 'Teleporter'
        }

#  def append_prettylog(self, text, tag1=None, tag2=None):
#    if not tag1:
#      self.prettylog.insert_with_tags(self.prettylog.get_end_iter(), text)
#    elif not tag2:
#      self.prettylog.insert_with_tags(self.prettylog.get_end_iter(), text, self.prettylog.get_tag_table().lookup(tag1))
#    else:
#      self.prettylog.insert_with_tags(self.prettylog.get_end_iter(), text, self.prettylog.get_tag_table().lookup(tag1), self.prettylog.get_tag_table().lookup(tag2))
#
#
#  def action(self, remote, timestamp, key,value, properties):
#    def getcolortag(team):
#      return 'team_'+team.lower()
#
#    if key in ['say', 'say_team']:
#      text = value['player_name'] + ": "+value['message']
#      if key == 'say_team':
#        text = '(TEAM) ' + text
#
#      self.append_prettylog(text, getcolortag(value['player_team']), "say")
#
#    elif key == 'kill':
#      self.append_prettylog(value['attacker_name'], getcolortag(value['attacker_team']))
#      self.append_prettylog(" killed ")
#      self.append_prettylog(value['victim_name'], getcolortag(value['victim_team']))
#      self.append_prettylog(" with "+value['weapon'])
#
#    elif key == 'class':
#      self.append_prettylog(value['player_name'], getcolortag(value['player_team']))
#      self.append_prettylog(" changed to "+value['class'])
#      
#    elif key == 'team':
#      self.append_prettylog(value['player_name'])
#      self.append_prettylog(" joined team ")
#      self.append_prettylog(value['team'], getcolortag(value['team']))
#
#    elif key == 'connect':
#      self.append_prettylog(value['player_name'] + " (" + value['player_steamid'] + ") connected from " + value['ip'])
#
#    elif key == 'trigger':
#      if value['trigger'] == 'builtobject':
#        self.append_prettylog(value['player_name'], getcolortag(value['player_team']))
#        self.append_prettylog(" built a " + self.objects[properties['object']])
#
#      elif value['trigger'] == 'killedobject':
#        self.append_prettylog(value['player_name'], getcolortag(value['player_team']))
#        self.append_prettylog(" destroyed ")
#        self.append_prettylog(properties['objectowner']['player_name'] + "'s ", getcolortag(properties['objectowner']['player_team']))
#        self.append_prettylog(self.objects[properties['object']] + " with " + properties['weapon'])
#      else:
#        print(value, properties)
#        return
#    else:
#      return
#
#    self.append_prettylog("\n")
 

  def parse(self, line):
    SourceLib.SourceLog.SourceLogParser.parse(self, line)
    line = line.strip('\x00\xff\r\n\t')
    self.manager.append_to_log(self.server, line, 'remote')


