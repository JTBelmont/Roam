import os
import roam.defaults
from qgis.core import QgsFeature, QgsFields, QgsField

def test_variables_are_expanded():
    os.environ['TESTVAR'] = 'MYVAR'
    default = "1 %TESTVAR% 2"
    outdefault = roam.defaults.default_value(default, None, None)
    assert outdefault == '1 MYVAR 2'
    del os.environ['TESTVAR']

def test_replaced_with_qgsexpression_simple_value():
    default = "[% 'testvalue' %]"
    outdefault = roam.defaults.default_value(default, None, None)
    assert outdefault == 'testvalue'

def test_replaced_with_qgsexpression_feature_attribute_lookup():
    feature = QgsFeature()
    fields = QgsFields()
    fields.append(QgsField('mycol'))
    feature.setFields(fields)
    feature['mycol'] = 'testvalue'
    default = '[% "mycol" %]'
    outdefault = roam.defaults.default_value(default, feature, None)
    assert outdefault == 'testvalue'

def test_value_with_expression_and_variable_are_expanded():
    os.environ['TESTVAR'] = 'MYVAR'
    default = "%TESTVAR% [% 'testvalue' %]"
    outdefault = roam.defaults.default_value(default, None, None)
    assert outdefault == 'MYVAR testvalue'
    del os.environ['TESTVAR']


def test_widget_default_returns_none_on_no_default():
    config = {}
    assert roam.defaults.widget_default(config, None, None) is None

def test_widget_default_returns_value_for_default():
    config = {'default': 'testvalue'}
    assert roam.defaults.widget_default(config, None, None) is 'testvalue'

