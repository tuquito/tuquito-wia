#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito WIA 1.2
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

import pygame, os, time, pynotify, gettext

# i18n
gettext.install('tuquito-wia', '/usr/share/tuquito/locale')

# Inicia Notificaciones
if not pynotify.init ('TUQUITO-WIA-Notify'):
	exit(1)

#-Variables
lang = os.environ['LANG'][:5]
lang2 = lang[:2]
icontype = ['.xpm','.png','.svg']
icondir = ['', '/usr/share/pixmaps/','/usr/share/icons/','/usr/share/icons/hicolor/scalable/apps/','/usr/share/icons/hicolor/48x48/apps/','/usr/share/icons/hicolor/22x22/apps/','/usr/share/icons/hicolor/32x32/apps/','/usr/share/icons/hicolor/16x16/apps/','/usr/share/app-install/icons/']
categories = ['%s » %s' % (_('Applications'), _('Accessories')),'Utility'],['%s » %s' % (_('Applications'), _('Education')),'Education'],['%s » %s' % (_('Applications'), _('Games')),'Game'],['%s » %s' % (_('Applications'), _('Graphics')),'Graphics'],['%s » %s' % (_('Applications'), _('Internet')),'Network'],['%s » %s' % (_('Applications'), _('Office')),'Office'],['%s » %s' % (_('Applications'), _('Programming')),'Development'],['%s » %s' % (_('Applications'), _('Sound & Video')),'AudioVideo'],['%s » %s' % (_('System'), _('Settings')),'Settings'],['%s » %s' % (_('Applications'), _('System Tools')),'System'],['%s » %s' % (_('System'), _('Administration')),'System;Settings'],['%s » %s' % (_('Applications'), _('Others')),'Other']

class SearchApp:
	def __init__(self):
		self.apps = []
		self.appsold = []

	def searchIn(self, path):
		global icondir, icontype, categories
		for filename in os.listdir(path):
			if os.path.isfile(path + filename):
				self.apps.append(str(path + filename))
		selez = []

		if len(self.apps) != len(self.appsold):
			if len(self.appsold) > 0:
				x = 0
				while x < len(self.apps):
					nm = ''.join(self.appsold)
					if nm.find(self.apps[x]) == -1:
						selez.append('I|' + self.apps[x])
					x += 1
				x = 0
				while x < len(self.appsold):
					nm = ''.join(self.apps)
					if nm.find(self.appsold[x]) == -1:
						selez.append('E|' + self.appsold[x])
					x += 1
		self.appsold = []
		self.apps = []

		for filename in os.listdir(path):
			if os.path.isfile(path + filename):
				self.appsold.append(str(path + filename))
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

			pygame.mixer.music.play()

class Tempo:
	def get_time(self):
		return self.time

	def __init__(self):
		self.time = 0

	def run(self):
		self.time += 1
		if self.time > 50:
			self.time = 0
		time.sleep(0.1)

def notify(top, sub, image):
	n = pynotify.Notification(top, sub, image)
	n.show()

def main_loop():
	while True:
		tm.run()
		if tm.get_time() == 9:
			one.searchIn('/usr/share/applications/')
			if os.path.exists('/usr/share/applications/kde4') == True:
				two.searchIn('/usr/share/applications/kde4/')
			if os.path.exists('/usr/share/applications/kde') == True:
				three.searchIn('/usr/share/applications/kde/')

pygame.init()
pygame.mixer.music.load('/usr/share/sounds/wia.wav')
one = SearchApp()
two = SearchApp()
three = SearchApp()
tm = Tempo()
main_loop()
