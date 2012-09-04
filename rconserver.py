# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# rconserver - Class for managing a server in rcontool
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

import socket

import pinggraph


class Gameserver(object):
  def __init__(self, ip, port, rcon_visible=False, rcon_password=None):
    self.ip = ip
    self.port = port
    self.rcon_visible = rcon_visible
    self.rcon_password = rcon_password
    self.rcon = None

    self.logging = False
    
    self.pings = []

    self.info = {}

  def __reduce__(self):
    '''Magical pickle packer, creates a new "gameserver" instance with the following args'''
    return Gameserver, (self.ip,self.port,self.rcon_visible,self.rcon_password)

  def __key(self):
    return (self.ip, self.port)

  def __hash__(self):
    '''Servers should be unique by IP'''
    return self.__key().__hash__()

  def __cmp__(self, other):
    return self.__hash__() < other.__hash__()

  def add_ping_history(self):
    self.pings.append(self.info['ping'])
    if len(self.pings) > pinggraph.PING_LIMIT:
      self.pings.pop(0)

  def rcon_cmd(self, command):
    if not self.rcon_connected():
      return False, "Password not set, ignoring"

    try:
      return True, self.rcon.rcon(command)
    except SourceLib.SourceRcon.SourceRconError as e:
      self.rcon = None
      return False, str(e)
    except socket.gaierror as e:
      self.rcon = None
      return False, str(e)

  def query(self):
    try:
      q = SourceLib.SourceQuery.SourceQuery(self.ip, self.port)
      self.info = q.info()
      if not self.info:
        self.info = { 'ping' : 1000, 'ip' : self.ip }
        return False, "Failed to connect to the server"

      if 'ping' in self.info:
        self.info['ping'] = int(self.info['ping'] * 1000)
      else:
        self.info['ping'] = 1000

      self.info['ip'] = self.ip
      return True, ""
    except (SourceLib.SourceQuery.SourceQueryError, socket.gaierror) as e:
      error = e
    except socket.timeout as e:
      error = "Request timed out"
    except socket.error as e:
      error = e

    self.info['ping'] = 1000
    return False, error

  def cleanup(self):
    if self.rcon_connected():
      self.rcon.disconnect()
    

  def set_rcon_visibility(self, enabled):
    self.rcon_visible = enabled

  def rcon_connected(self):
    return self.rcon != None

  def set_rcon(self, newpass):
    if not newpass:
      return

    if self.rcon_password != newpass or not self.rcon:
      self.rcon_password = newpass
      self.rcon = SourceLib.SourceRcon.SourceRcon(self.ip, self.port, self.rcon_password)


