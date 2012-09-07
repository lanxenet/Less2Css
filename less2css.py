from os import path
import sublime, sublime_plugin
import subprocess
import re
import os
import threading

from lessc import get_lessc_cmd
from yuicompressor import get_yui_compressor_cmd

class BaseCall(threading.Thread):
    def __init__(self, source_type, source):
        self.result = None
        self.error = None
        self.cmd = self.build_cmd(source_type, source)
        super(BaseCall, self).__init__(self)

    def build_cmd(self, source_type, source):
        pass

    def exec_process(self):
        if not self.cmd:
            self.error = True
            self.result = 'Less2Css Error: cmd null!'

        p = subprocess.Popen(self.cmd, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while True:
            try:
              stdout, stderr = p.communicate()
            except ValueError:
              break

            #remove control characters  
            out = stderr.decode("ascii")
            out = re.sub('\033\[[^m]*m', '', out)
            self.result = out
            break

    def run(self):
      print '###cmd: ', self.cmd
      try:          
        self.exec_process()
      except Exception as e:
        self.error = True
        self.result += str(e)
      print '###result:', self.result

class LessCompilerCall(BaseCall):
  def build_cmd(self, source_type, source):
      path, ext = os.path.splitext(source)
      target = path + '.css'
      here = os.path.dirname(__file__)
      return get_lessc_cmd(source, target)

class YuiCompilerCall(BaseCall):
  def build_cmd(self, source_type, source):
      path, ext = os.path.splitext(source)
      source = path + '.css'
      target = path + '.min.css'
      return get_yui_compressor_cmd(source_type, source, target)


#define methods to convert css, either the current file or all
class LessToCss:
  def __init__(self, view):
    self.view = view

  def get_processes(self, source_type, source):
    processes = [LessCompilerCall(source_type, source)]
    settings = sublime.load_settings('less2css.sublime-settings')
    if settings.get("compress"):
      processes += [YuiCompilerCall(source_type, source)]

    return processes

  def convertOne(self, file=""):

    #get the current file & its css variant
    if file == "":
      fn = self.view.file_name().encode("utf_8")
    else:
      fn = file

    print file

    out = ''
    processes = self.get_processes('css', fn)
    for process in processes:
      process.start()
      out + str(process.result)
    return out


############################
##### SUBLIME COMMANDS #####
############################

#single less file
class LessToCssCommand(sublime_plugin.TextCommand):
  def run(self, text):
    l2c = LessToCss(self.view)
    fn = self.view.file_name().encode("utf_8")
    
    if fn.find(".less") > -1:
      sublime.status_message("Compiling .less files...")
      resp = l2c.convertOne("")

      if resp != "":
        sublime.error_message(resp)
      else:
        sublime.status_message(".less file compiled successfully")

#listener to current less file
class LessToCssSave(sublime_plugin.EventListener):
  def on_post_save(self, view):
    view.run_command("less_to_css")