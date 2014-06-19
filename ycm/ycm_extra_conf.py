import os
import sys
import ycm_core

flags = [
'-std=c++11',
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
# compilation_database_folder = '/home/simbuerg/Projekte/.ycm'
compilation_database_folder = '/home/vulder/.ycm'
dbName = 'compile_commands.json'

def CollectDatabases( name ):
  dbsFound = []
  for (path, dirs, files) in os.walk(name):
    if dbName in files:
      dbsFound.append(path)
  return dbsFound

def LoadDatabases(dir):
  dbs = CollectDatabases(dir)
  compDbs = []
  for db in dbs:
    cdb = ycm_core.CompilationDatabase(db)
    if cdb.DatabaseSuccessfullyLoaded():
        tempfile.write(" Added: " + db + "\n")
        compDbs.append({
            "name": db,
            "db": cdb
            })

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
    for dbInfo in databases:
      compilation_info = dbInfo["db"].GetCompilationInfoForFile(filename)
      num_flags = len(compilation_info.compiler_flags_)
      if num_flags > 0:
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
