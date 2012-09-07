# LESS compiler for Sublime Text 2 in windows
# http://www.cnblogs.com/tangoboy/
# Licensed under the WTFPL

import os, sys, subprocess, functools, sublime, sublime_plugin

package_name = 'lessc'


def get_lessc_cmd(source, target):
	here = os.path.abspath(os.path.dirname(__file__))
	return ['@cscript', '//nologo', os.path.join(here, 'lessc.wsf'), source, target]