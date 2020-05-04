from __future__ import print_function

import os

import rosparam
import rospy
from python_qt_binding.QtCore import Qt
from python_qt_binding.QtWidgets import (QFormLayout, QLabel, QLineEdit,
                                         QVBoxLayout, QWidget)
from qt_gui.plugin import Plugin


class ROSParamPlugin(Plugin):

    def __init__(self, context):
        super(ROSParamPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('ROSParamPlugin')

        # Create QWidget
        self._widget = QWidget()
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)

        self._widget.setLayout(self._layout)

        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (' (%d)' % context.serial_number()))

        context.add_widget(self._widget)

        self._form = QFormLayout()
        self._layout.addLayout(self._form)

        self._params_map = {}
        self.add_params()

        rospy.Timer(rospy.Duration(0.1), self.update_loop)

    def add_params(self):
        for param in sorted(rosparam.list_params('')):
            label = QLabel(param)
            line = QLineEdit(param)
            line.textChanged.connect(lambda text: self.set_param(param, text))
            self._form.addRow(label, line)
            self._params_map[param] = line
            self.update_param(param)

    def set_param(self, param, value):
        if value != "":
            rosparam.set_param(param, value)

    def update_param(self, param):
        value = rosparam.get_param(param)
        widget = self._params_map[param]

        if type(value) != str:
            value = str(value)

        if widget.text() != value:
            widget.setText(value)

    def update_loop(self, evt):
        for a in self._params_map.keys():
            self.update_param(a)

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    # def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog