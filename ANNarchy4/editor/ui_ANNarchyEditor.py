# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ANNarchyEditor.ui'
#
# Created: Sat Feb  1 19:38:59 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ANNarchyEditor(object):
    def setupUi(self, ANNarchyEditor):
        ANNarchyEditor.setObjectName(_fromUtf8("ANNarchyEditor"))
        ANNarchyEditor.resize(1080, 624)
        ANNarchyEditor.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtGui.QWidget(ANNarchyEditor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_14 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setMinimumSize(QtCore.QSize(600, 0))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.views = MyTabWidget(self.splitter)
        self.views.setObjectName(_fromUtf8("views"))
        self.object_page = QtGui.QWidget()
        self.object_page.setObjectName(_fromUtf8("object_page"))
        self.verticalLayout_15 = QtGui.QVBoxLayout(self.object_page)
        self.verticalLayout_15.setObjectName(_fromUtf8("verticalLayout_15"))
        self.objects = CodeView(self.object_page)
        self.objects.setObjectName(_fromUtf8("objects"))
        self.verticalLayout_15.addWidget(self.objects)
        self.views.addTab(self.object_page, _fromUtf8(""))
        self.editor_page = QtGui.QWidget()
        self.editor_page.setMinimumSize(QtCore.QSize(0, 0))
        self.editor_page.setWhatsThis(_fromUtf8(""))
        self.editor_page.setObjectName(_fromUtf8("editor_page"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.editor_page)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.editor = GLNetworkWidget(self.editor_page)
        self.editor.setObjectName(_fromUtf8("editor"))
        self.verticalLayout_11.addWidget(self.editor)
        self.views.addTab(self.editor_page, _fromUtf8(""))
        self.env_page = QtGui.QWidget()
        self.env_page.setObjectName(_fromUtf8("env_page"))
        self.verticalLayout_16 = QtGui.QVBoxLayout(self.env_page)
        self.verticalLayout_16.setObjectName(_fromUtf8("verticalLayout_16"))
        self.environment = CodeView(self.env_page)
        self.environment.setObjectName(_fromUtf8("environment"))
        self.verticalLayout_16.addWidget(self.environment)
        self.views.addTab(self.env_page, _fromUtf8(""))
        self.params = QtGui.QWidget()
        self.params.setObjectName(_fromUtf8("params"))
        self.views.addTab(self.params, _fromUtf8(""))
        self.visualizer_page = QtGui.QWidget()
        self.visualizer_page.setObjectName(_fromUtf8("visualizer_page"))
        self.verticalLayout_13 = QtGui.QVBoxLayout(self.visualizer_page)
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.visualizer = VisualizerWidget(self.visualizer_page)
        self.visualizer.setObjectName(_fromUtf8("visualizer"))
        self.gridLayout_4 = QtGui.QGridLayout(self.visualizer)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gl_context = GLBaseWidget(self.visualizer)
        self.gl_context.setObjectName(_fromUtf8("gl_context"))
        self.gridLayout_4.addWidget(self.gl_context, 0, 0, 1, 1)
        self.verticalLayout_13.addWidget(self.visualizer)
        self.views.addTab(self.visualizer_page, _fromUtf8(""))
        self.complet_page = QtGui.QWidget()
        self.complet_page.setObjectName(_fromUtf8("complet_page"))
        self.verticalLayout_17 = QtGui.QVBoxLayout(self.complet_page)
        self.verticalLayout_17.setObjectName(_fromUtf8("verticalLayout_17"))
        self.complete = CodeView(self.complet_page)
        self.complete.setObjectName(_fromUtf8("complete"))
        self.verticalLayout_17.addWidget(self.complete)
        self.views.addTab(self.complet_page, _fromUtf8(""))
        self.special = QtGui.QStackedWidget(self.splitter)
        self.special.setMaximumSize(QtCore.QSize(16777215, 10))
        self.special.setObjectName(_fromUtf8("special"))
        self.propertiesPage1 = QtGui.QWidget()
        self.propertiesPage1.setObjectName(_fromUtf8("propertiesPage1"))
        self.special.addWidget(self.propertiesPage1)
        self.general = QtGui.QStackedWidget(self.splitter_2)
        self.general.setMinimumSize(QtCore.QSize(200, 0))
        self.general.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.general.setObjectName(_fromUtf8("general"))
        self.obj_tab = QtGui.QWidget()
        self.obj_tab.setObjectName(_fromUtf8("obj_tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.obj_tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_9 = QtGui.QLabel(self.obj_tab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout.addWidget(self.label_9)
        self.neur_general = NeuronListView(self.obj_tab)
        self.neur_general.setObjectName(_fromUtf8("neur_general"))
        self.verticalLayout.addWidget(self.neur_general)
        self.label_8 = QtGui.QLabel(self.obj_tab)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout.addWidget(self.label_8)
        self.syn_general = SynapseListView(self.obj_tab)
        self.syn_general.setObjectName(_fromUtf8("syn_general"))
        self.verticalLayout.addWidget(self.syn_general)
        self.general.addWidget(self.obj_tab)
        self.net_tab = QtGui.QWidget()
        self.net_tab.setObjectName(_fromUtf8("net_tab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.net_tab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.stackedWidget_2 = StackWidget(self.net_tab)
        self.stackedWidget_2.setObjectName(_fromUtf8("stackedWidget_2"))
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.page_4)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.label_17 = QtGui.QLabel(self.page_4)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.verticalLayout_9.addWidget(self.label_17)
        self.net_select = NetworkListView(self.page_4)
        self.net_select.setObjectName(_fromUtf8("net_select"))
        self.verticalLayout_9.addWidget(self.net_select)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem)
        self.label_14 = QtGui.QLabel(self.page_4)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.verticalLayout_9.addWidget(self.label_14)
        self.label_15 = QtGui.QLabel(self.page_4)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.verticalLayout_9.addWidget(self.label_15)
        self.label_16 = QtGui.QLabel(self.page_4)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout_9.addWidget(self.label_16)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem1)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.stackedWidget_2.addWidget(self.page_4)
        self.pop_view = QtGui.QWidget()
        self.pop_view.setObjectName(_fromUtf8("pop_view"))
        self.gridLayout_2 = QtGui.QGridLayout(self.pop_view)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_5 = QtGui.QLabel(self.pop_view)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.pop_view)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.pop_name = QtGui.QLineEdit(self.pop_view)
        self.pop_name.setReadOnly(False)
        self.pop_name.setObjectName(_fromUtf8("pop_name"))
        self.gridLayout_2.addWidget(self.pop_name, 0, 1, 1, 1)
        self.pop_size = QtGui.QLineEdit(self.pop_view)
        self.pop_size.setReadOnly(False)
        self.pop_size.setObjectName(_fromUtf8("pop_size"))
        self.gridLayout_2.addWidget(self.pop_size, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 2, 1, 1, 1)
        self.stackedWidget_2.addWidget(self.pop_view)
        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName(_fromUtf8("page_5"))
        self.gridLayout_3 = QtGui.QGridLayout(self.page_5)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_11 = QtGui.QLabel(self.page_5)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_3.addWidget(self.label_11, 0, 0, 1, 1)
        self.pre_name = QtGui.QLineEdit(self.page_5)
        self.pre_name.setAcceptDrops(False)
        self.pre_name.setObjectName(_fromUtf8("pre_name"))
        self.gridLayout_3.addWidget(self.pre_name, 0, 2, 1, 1)
        self.label_12 = QtGui.QLabel(self.page_5)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_3.addWidget(self.label_12, 1, 0, 1, 2)
        self.post_name = QtGui.QLineEdit(self.page_5)
        self.post_name.setAcceptDrops(False)
        self.post_name.setObjectName(_fromUtf8("post_name"))
        self.gridLayout_3.addWidget(self.post_name, 1, 2, 1, 1)
        self.label_13 = QtGui.QLabel(self.page_5)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_3.addWidget(self.label_13, 2, 0, 1, 1)
        self.target = QtGui.QLineEdit(self.page_5)
        self.target.setAcceptDrops(False)
        self.target.setObjectName(_fromUtf8("target"))
        self.gridLayout_3.addWidget(self.target, 2, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 443, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 3, 1, 1, 1)
        self.stackedWidget_2.addWidget(self.page_5)
        self.verticalLayout_4.addWidget(self.stackedWidget_2)
        self.general.addWidget(self.net_tab)
        self.env_tab = QtGui.QWidget()
        self.env_tab.setObjectName(_fromUtf8("env_tab"))
        self.general.addWidget(self.env_tab)
        self.par_tab = QtGui.QWidget()
        self.par_tab.setObjectName(_fromUtf8("par_tab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.par_tab)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_7 = QtGui.QLabel(self.par_tab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_5.addWidget(self.label_7)
        self.par_general = QtGui.QListView(self.par_tab)
        self.par_general.setObjectName(_fromUtf8("par_general"))
        self.verticalLayout_5.addWidget(self.par_general)
        self.general.addWidget(self.par_tab)
        self.vis_tab = QtGui.QWidget()
        self.vis_tab.setObjectName(_fromUtf8("vis_tab"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.vis_tab)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.vis_control = VisControlWidget(self.vis_tab)
        self.vis_control.setObjectName(_fromUtf8("vis_control"))
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.vis_control)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.groupBox = QtGui.QGroupBox(self.vis_control)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.grid_x_dim = QtGui.QLineEdit(self.groupBox)
        self.grid_x_dim.setObjectName(_fromUtf8("grid_x_dim"))
        self.horizontalLayout_2.addWidget(self.grid_x_dim)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.grid_y_dim = QtGui.QLineEdit(self.groupBox)
        self.grid_y_dim.setObjectName(_fromUtf8("grid_y_dim"))
        self.horizontalLayout_3.addWidget(self.grid_y_dim)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.change_grid = QtGui.QPushButton(self.groupBox)
        self.change_grid.setObjectName(_fromUtf8("change_grid"))
        self.verticalLayout_2.addWidget(self.change_grid)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_12.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.vis_control)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.pop_proj_select = QtGui.QComboBox(self.groupBox_2)
        self.pop_proj_select.setObjectName(_fromUtf8("pop_proj_select"))
        self.gridLayout.addWidget(self.pop_proj_select, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.param_select = QtGui.QComboBox(self.groupBox_2)
        self.param_select.setObjectName(_fromUtf8("param_select"))
        self.gridLayout.addWidget(self.param_select, 1, 1, 1, 1)
        self.verticalLayout_12.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(self.vis_control)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.plot_select = QtGui.QComboBox(self.groupBox_3)
        self.plot_select.setObjectName(_fromUtf8("plot_select"))
        self.horizontalLayout_4.addWidget(self.plot_select)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.plot_config = QtGui.QStackedWidget(self.groupBox_3)
        self.plot_config.setObjectName(_fromUtf8("plot_config"))
        self.plot_none = QtGui.QWidget()
        self.plot_none.setObjectName(_fromUtf8("plot_none"))
        self.plot_config.addWidget(self.plot_none)
        self.plot_1d = QtGui.QWidget()
        self.plot_1d.setObjectName(_fromUtf8("plot_1d"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.plot_1d)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_18 = QtGui.QLabel(self.plot_1d)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_5.addWidget(self.label_18)
        self.plot_1d_color = QtGui.QComboBox(self.plot_1d)
        self.plot_1d_color.setObjectName(_fromUtf8("plot_1d_color"))
        self.horizontalLayout_5.addWidget(self.plot_1d_color)
        self.horizontalLayout.addLayout(self.horizontalLayout_5)
        self.plot_config.addWidget(self.plot_1d)
        self.plot_2d = QtGui.QWidget()
        self.plot_2d.setObjectName(_fromUtf8("plot_2d"))
        self.plot_config.addWidget(self.plot_2d)
        self.verticalLayout_7.addWidget(self.plot_config)
        self.verticalLayout_12.addWidget(self.groupBox_3)
        spacerItem7 = QtGui.QSpacerItem(20, 166, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacerItem7)
        self.verticalLayout_8.addWidget(self.vis_control)
        self.general.addWidget(self.vis_tab)
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.page)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.compile_and_run = QtGui.QPushButton(self.page)
        self.compile_and_run.setObjectName(_fromUtf8("compile_and_run"))
        self.verticalLayout_6.addWidget(self.compile_and_run)
        self.general.addWidget(self.page)
        self.verticalLayout_14.addWidget(self.splitter_2)
        ANNarchyEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ANNarchyEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuConfig = QtGui.QMenu(self.menubar)
        self.menuConfig.setObjectName(_fromUtf8("menuConfig"))
        ANNarchyEditor.setMenuBar(self.menubar)
        self.actionOpen = QtGui.QAction(ANNarchyEditor)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionQuit = QtGui.QAction(ANNarchyEditor)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionSave = QtGui.QAction(ANNarchyEditor)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfig.menuAction())

        self.retranslateUi(ANNarchyEditor)
        self.views.setCurrentIndex(4)
        self.general.setCurrentIndex(4)
        self.stackedWidget_2.setCurrentIndex(0)
        self.plot_config.setCurrentIndex(1)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), ANNarchyEditor.close)
        QtCore.QObject.connect(self.compile_and_run, QtCore.SIGNAL(_fromUtf8("pressed()")), ANNarchyEditor.compile_and_run)
        QtCore.QObject.connect(self.editor, QtCore.SIGNAL(_fromUtf8("update_population(int,int)")), self.stackedWidget_2.update_population)
        QtCore.QObject.connect(ANNarchyEditor, QtCore.SIGNAL(_fromUtf8("initialize()")), self.stackedWidget_2.initialize)
        QtCore.QObject.connect(ANNarchyEditor, QtCore.SIGNAL(_fromUtf8("initialize()")), self.vis_control.initialize)
        QtCore.QObject.connect(ANNarchyEditor, QtCore.SIGNAL(_fromUtf8("initialize()")), self.visualizer.initialize)
        QtCore.QObject.connect(self.change_grid, QtCore.SIGNAL(_fromUtf8("pressed()")), self.vis_control.change_grid)
        QtCore.QObject.connect(self.vis_control, QtCore.SIGNAL(_fromUtf8("signal_change_grid(int,int)")), self.visualizer.change_grid)
        QtCore.QObject.connect(ANNarchyEditor, QtCore.SIGNAL(_fromUtf8("initialize()")), self.neur_general.initialize)
        QtCore.QObject.connect(self.neur_general, QtCore.SIGNAL(_fromUtf8("signal_show_template(int,QString)")), self.objects.set_code)
        QtCore.QObject.connect(self.views, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), self.general.setCurrentIndex)
        QtCore.QObject.connect(ANNarchyEditor, QtCore.SIGNAL(_fromUtf8("initialize()")), self.views.initialize)
        QtCore.QObject.connect(ANNarchyEditor, QtCore.SIGNAL(_fromUtf8("initialize()")), self.objects.initialize)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL(_fromUtf8("triggered()")), self.objects.save)
        QtCore.QObject.connect(self.syn_general, QtCore.SIGNAL(_fromUtf8("signal_show_template(int,QString)")), self.objects.set_code)
        QtCore.QObject.connect(ANNarchyEditor, QtCore.SIGNAL(_fromUtf8("initialize()")), self.syn_general.initialize)
        QtCore.QObject.connect(ANNarchyEditor, QtCore.SIGNAL(_fromUtf8("initialize()")), self.net_select.initialize)
        QtCore.QObject.connect(self.net_select, QtCore.SIGNAL(_fromUtf8("signal_show_network(QString)")), self.editor.show_network)
        QtCore.QObject.connect(self.plot_select, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.plot_config.setCurrentIndex)
        QtCore.QObject.connect(self.plot_1d_color, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.vis_control.change_color)
        QtCore.QMetaObject.connectSlotsByName(ANNarchyEditor)

    def retranslateUi(self, ANNarchyEditor):
        ANNarchyEditor.setWindowTitle(QtGui.QApplication.translate("ANNarchyEditor", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.views.setTabText(self.views.indexOf(self.object_page), QtGui.QApplication.translate("ANNarchyEditor", "Neuron / Synapses", None, QtGui.QApplication.UnicodeUTF8))
        self.views.setTabText(self.views.indexOf(self.editor_page), QtGui.QApplication.translate("ANNarchyEditor", "Network", None, QtGui.QApplication.UnicodeUTF8))
        self.views.setTabText(self.views.indexOf(self.env_page), QtGui.QApplication.translate("ANNarchyEditor", "Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.views.setTabText(self.views.indexOf(self.params), QtGui.QApplication.translate("ANNarchyEditor", "Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.views.setTabText(self.views.indexOf(self.visualizer_page), QtGui.QApplication.translate("ANNarchyEditor", "Visualizer", None, QtGui.QApplication.UnicodeUTF8))
        self.views.setTabText(self.views.indexOf(self.complet_page), QtGui.QApplication.translate("ANNarchyEditor", "CompleteScript", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("ANNarchyEditor", "Neurons", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("ANNarchyEditor", "Synapses", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("ANNarchyEditor", "Available networks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("ANNarchyEditor", "Select a population", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("ANNarchyEditor", "to get detailed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("ANNarchyEditor", "information", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ANNarchyEditor", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ANNarchyEditor", "Geometry", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("ANNarchyEditor", "Pre populaution", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("ANNarchyEditor", "Post population", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("ANNarchyEditor", "Target", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("ANNarchyEditor", "Loaded file(s):", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ANNarchyEditor", "Grid configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ANNarchyEditor", "x size", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_x_dim.setText(QtGui.QApplication.translate("ANNarchyEditor", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ANNarchyEditor", "y size", None, QtGui.QApplication.UnicodeUTF8))
        self.grid_y_dim.setText(QtGui.QApplication.translate("ANNarchyEditor", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.change_grid.setText(QtGui.QApplication.translate("ANNarchyEditor", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("ANNarchyEditor", "Data set", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ANNarchyEditor", "Pop/Proj", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("ANNarchyEditor", "Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("ANNarchyEditor", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ANNarchyEditor", "Plot Type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("ANNarchyEditor", "Color", None, QtGui.QApplication.UnicodeUTF8))
        self.compile_and_run.setText(QtGui.QApplication.translate("ANNarchyEditor", "Compile and Run", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("ANNarchyEditor", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuConfig.setTitle(QtGui.QApplication.translate("ANNarchyEditor", "Config", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("ANNarchyEditor", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setToolTip(QtGui.QApplication.translate("ANNarchyEditor", "Open a scrip", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(QtGui.QApplication.translate("ANNarchyEditor", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("ANNarchyEditor", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("ANNarchyEditor", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("ANNarchyEditor", "save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("ANNarchyEditor", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))

from mytabwidget import MyTabWidget
from StackWidget import StackWidget
from GLNetwork import GLNetworkWidget
from GLObjects import GLBaseWidget
from VisWidget import VisControlWidget, VisualizerWidget
from CodeView import CodeView
from ListView import NeuronListView, NetworkListView, SynapseListView
