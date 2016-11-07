import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import time

#
# QtMixinTest
#

class QtMixinTest(ScriptedLoadableModule):
  def __init__(self, parent):
    parent.title = "QtMixinTest" # TODO make this more human readable by adding spaces
    parent.categories = ["Testing.TestCases"]
    parent.dependencies = []
    parent.contributors = ["Johan Andruejol (Kitware)"]
    parent.helpText = """
    This is a self test that tests the piping of two CLIs through python
    """
    parent.acknowledgementText = """""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['QtMixinTest'] = self.runTest

  def runTest(self):
    tester = QtMixinTestTest()
    tester.runTest()

#
# QtMixinTest
#

class QtMixinTestWidget(ScriptedLoadableModuleWidget, slicer.util.QtWidgetMixin):
  def __init__(self, parent = None, auto_setup=True):
    ScriptedLoadableModuleWidget.__init__(self, parent)
    slicer.util.QtWidgetMixin.__init__(self)

    if auto_setup:
      self.setup()

  def setup(self):
    moduleName = 'QtMixinTest'
    scriptedModulesPath = os.path.dirname(slicer.util.modulePath(moduleName))
    path = os.path.join(scriptedModulesPath, 'Resources', 'UI', moduleName + '.ui')

    self.Widget = self.loadUI(path)
    self.layout.addWidget(self.Widget)

#
# QtMixinTestLogic
#

class QtMixinTestLogic(ScriptedLoadableModuleLogic):
  def __init__(self):
    ScriptedLoadableModuleLogic.__init__(self)

#
# TwoCLIsInARowTestLogic
#

class QtMixinTestTest(ScriptedLoadableModuleTest):

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.test_loadUI()
    self.test_get()

  def test_loadUI(self):
    mixinWidget = QtMixinTestWidget(auto_setup=False)

    # Try to load a UI that does not exist silently
    self.assertIsNone(mixinWidget.loadUI('does/not/exists.ui', fail_silently=True))

    # Try to load a UI that does not exist a catch exception
    caughtException = False
    try:
      mixinWidget.loadUI('still/does/not/exists.ui')
    except AssertionError:
      caughtException = True
    self.assertTrue(caughtException)

    # Correct path
    caughtException = False
    try:
      mixinWidget.setup()
    except AssertionError:
      caughtException = True
    self.assertFalse(caughtException)

  def test_get(self):
    mixinWidget = QtMixinTestWidget(auto_setup=False)

    # Try with nothing (widget isn't setup)
    caughtException = False
    try:
      mixinWidget.get('QtMixinTest_Label')
    except AssertionError:
      caughtException = True
    self.assertTrue(caughtException)

    mixinWidget.setup()

    # Try to get a widget that exists
    label = mixinWidget.get('QtMixinTest_Label')
    self.assertIsNotNone(label, qt.QLabel)
    self.assertEqual(label.text, 'My custom UI')

    # Try to get a widget that does not exists
    caughtException = False
    try:
      mixinWidget.get('Unexistant_Label')
    except AssertionError:
      caughtException = True
    self.assertTrue(caughtException)
