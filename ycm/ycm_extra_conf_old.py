# This file is NOT licensed under the GPLv3, which is the license for the rest
# of YouCompleteMe.
#
# Here's the license text for this file:
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import os
import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
'-DUSE_CLANG_COMPLETER',
'-std=c++11',
'-I/home/vulder/hiwi/llvm/include/',
'-I/home/vulder/hiwi/llvm/tools/polly/include/',
'-I/home/vulder/hiwi/sqlite-autoconf-3080002/',
'-I/home/vulder/git/SchafkopfCounter/include/schafkopfcounter/',
'-I/home/vulder/git/c_cpp/c/include/',
'-I/home/vulder/git/c_cpp/cpp/include/',
'-I/home/vulder/git/TSQueryEx/lib/TSQueryAPI/include/TSQueryAPI/',
'-I/usr/local/include/',
'-I/home/vulder/plsremoveCServer/project/include/'
]

# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
#compilation_database_folder = '/home/simbuerg/Projekte/.ycm'
compilation_database_folder = '/home/vulder/.ycm'

def CollectDatabases( name ):
  dbName = 'compile_commands.json'
  dbsFound = []
  for (path, dirs, files) in os.walk(name):
    if dbName in files:
      dbsFound.append(path)
  return dbsFound

def LoadDatabases(dir):
  dbs = CollectDatabases(dir)
  compDbs = []
  for db in dbs:
    compDbs.append(ycm_core.CompilationDatabase(db))

  return compDbs

databases = LoadDatabases( compilation_database_folder )

def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )


def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  if not working_directory:
    return flags
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  return new_flags


def GetCompilationInfo (filename):
  if databases:
    for db in databases:
      compilation_info = db.GetCompilationInfoForFile(filename)
      if compilation_info:
        return compilation_info


def FlagsForFile( filename ):
  final_flags = None
  compilation_info = GetCompilationInfo(filename)

  if compilation_info:
    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ )
  
  if not final_flags:
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  return {
    'flags': final_flags,
    'do_cache': True
  }
