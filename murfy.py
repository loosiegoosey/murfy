#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by Albion von Darx ♈

__author__ = 'Albion von Darx'
#__name__ = 'MuRFY - Music Right For You'

import sys, os, ConfigParser, shutil
from PyQt4.QtGui import *
from PyQt4.QtCore import *


def config(*args, **kwargs):
	cp = ConfigParser.ConfigParser()
	cfgdir = os.path.expanduser(os.path.join('~','.murfy'))
	cfgfile = os.path.join(cfgdir,'murfy.cfg')
	if not os.path.exists(cfgfile):
		if not os.path.exists(cfgdir):
			os.makedirs(cfgdir)
		shutil.copyfile('default.cfg', cfgfile)
	cp.readfp(open(cfgfile))
	if kwargs.has_key('v'):
		cp.set(kwargs['s'], kwargs['o'], kwargs['v'])
		cp.write(open(cfgfile, 'w'))
	else:
		return cp.get(kwargs['s'], kwargs['o'])

if __name__ == '__main__':
	os.chdir(os.path.dirname(__file__))
	from gui import Main
	app = QApplication(sys.argv)
	w_main = Main()
	w_main.show()
	sys.exit(app.exec_())