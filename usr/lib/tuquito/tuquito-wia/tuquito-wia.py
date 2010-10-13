#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito WIA 1.3
 Copyright (C) 2010
 Basado en WIA de Palumbo Roberto <palumborobertomail@gmail.com>
 Author: Mario Colque <mario@tuquito.org.ar>
 Tuquito Team! - www.tuquito.org.ar

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; version 3 of the License.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
"""

import os
import gtk
import time
import pynotify
import gettext
import commands
import threading

a = commands.getoutput('ps -A | grep tuquitoWia | wc -l')
if a >= '1':
	exit(0)

architecture = commands.getoutput('uname -a')
if architecture.find('x86_64') >= 0:
	import ctypes
	libc = ctypes.CDLL('libc.so.6')
	libc.prctl(15, 'tuquitoWia', 0, 0, 0)
else:
	import dl
	libc = dl.open('/lib/libc.so.6')
	libc.call('prctl', 15, 'tuquitoWia', 0, 0, 0)

# i18n
gettext.install('tuquito-wia', '/usr/share/tuquito/locale')

# Inicia Notificaciones
if not pynotify.init ('TUQUITO-WIA-Notify'):
	exit(1)

# Variables
lang = os.environ['LANG'][:5]
lang2 = lang[:2]
apps = []
appsold = []
icontype = ['.xpm','.png','.svg']
icondir = ['', '/usr/share/pixmaps/','/usr/share/icons/','/usr/share/icons/hicolor/scalable/apps/','/usr/share/icons/hicolor/48x48/apps/','/usr/share/icons/hicolor/22x22/apps/','/usr/share/icons/hicolor/32x32/apps/','/usr/share/icons/hicolor/16x16/apps/','/usr/share/app-install/icons/']
categories = ['%s » %s' % (_('Applications'), _('Accessories')),'Utility'],['%s » %s' % (_('Applications'), _('Education')),'Education'],['%s » %s' % (_('Applications'), _('Games')),'Game'],['%s » %s' % (_('Applications'), _('Graphics')),'Graphics'],['%s » %s' % (_('Applications'), _('Internet')),'Network'],['%s » %s' % (_('Applications'), _('Office')),'Office'],['%s » %s' % (_('Applications'), _('Programming')),'Development'],['%s » %s' % (_('Applications'), _('Sound & Video')),'AudioVideo'],['%s » %s' % (_('System'), _('Settings')),'Settings'],['%s » %s' % (_('Applications'), _('System Tools')),'System'],['%s » %s' % (_('System'), _('Administration')),'System;Settings'],['%s » %s' % (_('Applications'), _('Others')),'Other']

gtk.gdk.threads_init()

class SearchApp(threading.Thread):
	def __init__(self, path):
		threading.Thread.__init__(self)
		self.path = path

	def run(self):
		global apps, appsold
		for filename in os.listdir(self.path):
			if os.path.isfile(self.path + filename):
				apps.append(str(self.path + filename))
		selez = []

		if len(apps) != len(appsold):
			if len(appsold) > 0:
				x = 0
				while x < len(apps):
					nm = ''.join(appsold)
					if nm.find(apps[x]) == -1:
						selez.append('I|' + apps[x])
					x += 1
				x = 0
				while x < len(appsold):
					nm = ''.join(apps)
					if nm.find(appsold[x]) == -1:
						selez.append('E|' + appsold[x])
					x += 1
		appsold = []
		apps = []

		for filename in os.listdir(self.path):
			if os.path.isfile(self.path + filename):
				appsold.append(str(self.path + filename))
		for sele in selez:
			frase = sele.split('|')
			sel = frase[1]

			if frase[0] == 'I':
				name = _('New Installed Application')
				catname = ''
				image = '/usr/lib/tuquito/tuquito-wia/wia-add.png'
				f = open(sel,'r')
				for l in f.readlines():
					s = l.split('=')

					if (s[0].upper() == 'NAME') or (s[0].upper() == 'NAME[' + lang2.upper() + ']') or (s[0].upper() == 'NAME[' + lang.upper() + ']'):
						name = s[1].strip()

					if s[0].upper() == 'ICON':
						image = s[1].strip()

					if s[0].upper() == 'CATEGORIES':
						submenu = s[1].strip()
						for cat in categories:
							if submenu.find(cat[1]) != -1:
								catname = cat[0]
				f.close()

				if image.find('.') == -1:
					for dr in icondir:
						for ic in icontype:
							if os.path.exists(dr + image + ic) == True:
								image = dr + image + ic
								break
				else:
					for dr in icondir:
						if os.path.exists(dr + image) == True:
							image = dr + image
							break
				notify(name, _('This new application can be found at:') + '\n' + catname, image)

			if frase[0] == 'E':
				notify(_('Apps deleted found'), _('Tuquito confirm that application was deleted'), '/usr/lib/tuquito/tuquito-wia/wia-remove.png')
			os.system('aplay -q /usr/lib/tuquito/tuquito-wia/wia.wav &')
		autoRefresh = AutomaticRefreshThread(self.path)
		autoRefresh.start()

class AutomaticRefreshThread(threading.Thread):
	def __init__(self, path):
		threading.Thread.__init__(self)
		self.path = path

	def run(self):
		time.sleep(2)
		refresh = SearchApp(self.path)
		refresh.start()

def notify(top, sub, image):
	n = pynotify.Notification(top, sub, image)
	n.show()

#start
searchApp = SearchApp('/usr/share/applications/')
searchApp.start()
if os.path.exists('/usr/share/applications/kde4'):
	two.searchIn('/usr/share/applications/kde4/')
	two.start()
if os.path.exists('/usr/share/applications/kde'):
	three.searchIn('/usr/share/applications/kde/')
	three.start()
