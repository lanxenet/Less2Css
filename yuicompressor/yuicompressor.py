import os

def get_yui_compressor_cmd(source_type, source, target):
	here = os.path.abspath(os.path.dirname(__file__))
	compressor = os.path.join(here, "yuicompressor-2.4.6.jar")
	return ["java", "-jar", compressor, "--type", source_type, "--charset", "utf-8", "-v", source, ">", target]