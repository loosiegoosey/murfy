#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by Albion von Darx ♈

__author__ = 'Albion von Darx'
__name__ = 'MuRFY - GUI'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os  # , re, fnmatch
#from xml.dom.minidom import *
from murfy import config


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.set_window()
        self.define_actions()
        self.set_menu_sb()
        self.set_layout()
        self.set_systray()

    def set_window(self):  # Just some basic window parameters
        self.setWindowTitle('MuRFY - Music Right For You')
        self.resize(800, 600)
        self.setWindowIcon(QIcon('icons%sGuitarist++.png' % os.sep))

    def define_actions(self):  # Connecting actions to signals comming from objects
        self.a_quit = QAction(QIcon('icons%squit.svg' % os.sep), 'Exit', self)              # Exit
        self.a_quit.setShortcut('Esc')
        self.connect(self.a_quit, SIGNAL('triggered()'), SLOT('close()'))

        self.a_open = QAction(QIcon('icons%sopen.svg' % os.sep), 'Open', self)              # Open
        self.a_open.setShortcut('ctrl+o')
        self.connect(self.a_open, SIGNAL('triggered()'), SLOT('close()'))

        self.a_tags = QAction(QIcon('icons%stag_edit.svg' % os.sep), 'Tags', self)          # Edit tags
        self.a_tags.setShortcut('Ins')
        self.connect(self.a_tags, SIGNAL('triggered()'), SLOT('close()'))

        self.a_skin = QAction(QIcon('icons%sskin.svg' % os.sep), 'Theme', self)             # Change theme
        self.connect(self.a_skin, SIGNAL('triggered()'), SLOT('close()'))

        self.a_prefs = QAction(QIcon('icons%sproperties.svg' % os.sep), 'Preferences', self)# Preferences
        self.a_prefs.setShortcut('F12')
        self.connect(self.a_prefs, SIGNAL('triggered()'), SLOT('close()'))

        self.a_help = QAction(QIcon('icons%shelp.svg' % os.sep), 'Help', self)              # Help
        self.a_help.setShortcut('F1')
        self.connect(self.a_help, SIGNAL('triggered()'), self.help)

        self.a_about = QAction(QIcon('icons%sinfo.svg' % os.sep), 'About', self)            # About
        self.a_about.setShortcut('F2')
        self.connect(self.a_about, SIGNAL('triggered()'), self.about)

        self.a_showhide = QAction(QIcon('icons%stheme.svg' % os.sep), 'Hide', self)         # Show or hide main window
        self.connect(self.a_showhide, SIGNAL('triggered()'), self.show_hide)

    def set_menu_sb(self):  # Adds a menu and a status bar
        self.m_main = self.menuBar()

        m_file = self.m_main.addMenu('File')
        m_file.addAction(self.a_open)
        m_file.addAction(self.a_quit)

        m_edit = self.m_main.addMenu('Edit')
        m_edit.addAction(self.a_tags)
        m_edit.addAction(self.a_skin)
        m_edit.addAction(self.a_prefs)

        m_help = self.m_main.addMenu('Help')
        m_help.addAction(self.a_help)
        m_help.addAction(self.a_about)

        self.sb = self.statusBar()
        self.sb.showMessage('No song playing')

    def set_layout(self):  # Placement of elements and maybe skinning (in da future, 'nough said), stay tuned

        self.cw = QWidget(self)                                 # Central Widget
        self.setCentralWidget(self.cw)

        self.b_prev = QToolButton(self)                         # Previous button
        self.b_prev.setAutoRaise(True)
        self.b_prev.setFixedSize(48, 48)
        self.b_prev.setIcon(QIcon('icons%sprevious.svg' % os.sep))
        self.b_prev.setIconSize(QSize(32, 32))

        self.b_play = QToolButton(self)                         # Play button
        self.b_play.setAutoRaise(True)
        self.b_play.setFixedSize(48, 48)
        self.b_play.setIcon(QIcon('icons%splay.svg' % os.sep))
        self.b_play.setIconSize(QSize(48, 48))

        self.b_next = QToolButton(self)                         # Next button
        self.b_next.setAutoRaise(True)
        self.b_next.setFixedSize(48, 48)
        self.b_next.setIcon(QIcon('icons%snext.svg' % os.sep))
        self.b_next.setIconSize(QSize(32, 32))

        self.b_fav = QToolButton(self)                          # The Last.fm favourite button
        self.b_fav.setAutoRaise(True)
        self.b_fav.setFixedSize(48, 48)
        self.b_fav.setIcon(QIcon('icons%sfavourite.svg' % os.sep))
        self.b_fav.setIconSize(QSize(32, 32))

        self.l_past = QLabel()                                  # Time from the start
        self.l_past.setText('00:00')

        self.l_future = QLabel()                                # Time to the end
        self.l_future.setText('00:00')

        self.spacer = QLabel()                                  # It has to be something there

        self.pb = QSlider()                                     # ProgressBar
        self.pb.setOrientation(Qt.Horizontal)

        self.lay_pb = QGridLayout()                             # ProgressBar + times layout
        self.lay_pb.setSpacing(0)
        self.lay_pb.setMargin(0)
        self.lay_pb.addWidget(self.l_past, 0, 0)
        self.lay_pb.addWidget(self.spacer)
        self.lay_pb.addWidget(self.l_future, 0, 2, Qt.AlignRight)
        self.lay_pb.addWidget(self.pb, 1, 0, 1, 3)
        self.lay_pb.setColumnStretch(0, 1)

        self.vol = QDial()                                      # Volume control
        self.vol.setFixedSize(48, 48)

        self.lay_tb = QHBoxLayout()                             # ToolBar layout
        self.lay_tb.setSpacing(0)
        self.lay_tb.setMargin(0)
        self.lay_tb.addWidget(self.b_prev)
        self.lay_tb.addWidget(self.b_play)
        self.lay_tb.addWidget(self.b_next)
        self.lay_tb.addWidget(self.b_fav)
        self.lay_tb.addLayout(self.lay_pb)
        self.lay_tb.addWidget(self.vol)


        #_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_    ▲ ToolBar ▲     _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_#
        #_-_-_-_-_-_-_-_-_-_-_-_-_-_    ▼ Drag'n'Drop area ▼    _-_-_-_-_-_-_-_-_-_-_-_-_-_#


        self.tree = QTreeView()                               # TreeView
        mod_fs = QFileSystemModel()
        path = config(s = 'GUI', o = 'path')
        #path = '/'
        mod_fs.setRootPath(path)
        mod_fs.index(path)
        mod_fs.setNameFilters(['*.ogg','*.mp3','*.aac','*.mid','*.flac'])
        self.tree.setModel(mod_fs)
        self.tree.setSelectionMode(3)
        self.tree.setDragEnabled(True)
        self.tree.setRootIndex(mod_fs.index(path))
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setIndentation(16)

        self.i_filter = QLineEdit()                             # text field for filtering and stream path input

        self.b_stream = QToolButton(self)                       # Accept stream path from self.i_filter
        self.b_stream.setAutoRaise(True)
        self.b_stream.setFixedSize(32, 32)
        self.b_stream.setIcon(QIcon('icons%snet_stream.svg' % os.sep))
        self.b_stream.setIconSize(QSize(32, 32))


        self.lay_tree = QGridLayout()                           # TreeView area layout
        self.lay_tree.setSpacing(0)
        self.lay_tree.setMargin(0)
        self.lay_tree.addWidget(self.i_filter, 0, 0)
        self.lay_tree.addWidget(self.b_stream, 0, 1)
        self.lay_tree.addWidget(self.tree, 1, 0, 1, 2)
        self.lay_tree.setColumnStretch(0, 1)

        self.w_tree = QWidget()                                 # TreeView area
        self.w_tree.setLayout(self.lay_tree)

        self.pl = QTableWidget()                                # Playlist

        self.lay_split = QSplitter()                            # Splitter for TreeView and Playlist
        self.lay_split.addWidget(self.w_tree)
        self.lay_split.addWidget(self.pl)
        self.lay_split.setSizes([100, 200])


        self.lay_cw = QVBoxLayout()                             # vertical layout of central widget
        self.lay_cw.setSpacing(0)
        self.lay_cw.setMargin(0)
        self.lay_cw.addLayout(self.lay_tb)
        self.lay_cw.addWidget(self.lay_split, 1)
        self.cw.setLayout(self.lay_cw)

    def help(self):  # This just can't absent here
        QMessageBox.information(self, "Help", "No help here for now, sorry. =(", QMessageBox.Ok)

    def about(self):  # If you want some support just contact me whenever
        QMessageBox.information(self, "About", '<qt><strong>MuRFY - Music Right For You</strong><br /><br />Support:<br /><a href = "mailto://twiguard@user.sf.com">Twiguard at sf.com</a><br />or<br /><a href = "http://www.twitter.com/Twiguard_CZ">Twitter</a></qt>', QMessageBox.Ok)

    def show_hide(self):
        if self.isHidden():
            self.a_showhide.setText('Hide')
            self.show()
        else:
            self.a_showhide.setText('Show')
            self.hide()

    def set_systray(self):  # Create a SysTray icon with menu
        self.m_systray = QMenu()
        self.m_systray.addAction(self.a_open)
        self.m_systray.addAction(self.a_showhide)
        self.m_systray.addSeparator()
        self.m_systray.addAction(self.a_quit)

        self.systray = QSystemTrayIcon()
        self.systray.setIcon(QIcon('icons%sGuitarist++.png' % os.sep))
        self.systray.setContextMenu(self.m_systray)
        self.systray.show()
