import platform
path_sep = '\\' if platform.system()=="Windows" else '/'

IDE_COMMAND = "code"

"""Python"""
# SRC_FILE_EXTENSION = ".py"
# COMPILE_COMMAND_TEMPLATE = None
# RUN_COMMAND_TEMPLATE = 'python3 "{src_path}"'

"""C++"""
SRC_FILE_EXTENSION = ".cc"
COMPILE_COMMAND_TEMPLATE = 'c++ "{src_path}" -o "{question_path}.o"'
RUN_COMMAND_TEMPLATE = f'.{path_sep}"{{question_path}}.o"'

"""Java"""
# SRC_FILE_EXTENSION = ".java"
# COMPILE_COMMAND_TEMPLATE = "javac {src_path}"
# RUN_COMMAND_TEMPLATE = "java {question_path}"
