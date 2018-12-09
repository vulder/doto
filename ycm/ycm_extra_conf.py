import os
import sys
import ycm_core

flags = [
    '-std=c++17',
    '-stdlib=libc++',
    '-Wall',
    '-I.',
    '-I/usr/include/c++/v1/',
    '-I/usr/include',
    # '-lstdc++',
]

# If you want to use more than one compilation database, put it in
# the compilation_database_folder. We will walk the directory recursively
# and gather all compile_commands.json files.
compilation_database_folder = '/home/vulder/.ycm'
dbName = 'compile_commands.json'
databases = None
SOURCE_EXTENSIONS = ['.cpp', '.cxx', '.cc', '.c', '.m', '.mm']
HEADER_EXTENSIONS = ['.h', '.hxx', '.hpp', '.hh' ]


def CollectDatabases(name):
    return [ path for (path, dirs, files) in os.walk(name) if dbName in files ]


def LoadDatabases(dir):
    cdb = dict()
    for db in CollectDatabases(dir):
        cdb[db] = ycm_core.CompilationDatabase(db)
    return cdb


def IsHeaderFile(filename):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in HEADER_EXTENSIONS


def DirectoryOfThisScript():
  return os.path.dirname(os.path.abspath(__file__))


def MakeRelativePathsInFlagsAbsolute(flags, working_directory):
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
    global SOURCE_EXTENSIONS
    global databases

    # If we don't have them yet, load them.
    if not databases:
        databases = LoadDatabases(compilation_database_folder)

    # We couldn't find any compilation database.
    if not databases:
        return None

    # Check for compilation info of headers
    if IsHeaderFile(filename):
        basename = os.path.splitext(filename)[0]
        for ext in SOURCE_EXTENSIONS:
            altFile = basename + ext
            if os.path.exists(altFile):
                cinfo = GetCompilationInfo(altFile)
                if cinfo and cinfo.compiler_flags_:
                    return cinfo

    # Find the right db
    for db in databases:
      cinfo = databases[db].GetCompilationInfoForFile(filename)
      if cinfo and cinfo.compiler_flags_:
        return cinfo


def FlagsForFile( filename ):
    final_flags = None
    cinfo = GetCompilationInfo(filename)

    # Query the DB
    if cinfo:
        final_flags = MakeRelativePathsInFlagsAbsolute(
        cinfo.compiler_flags_,
        cinfo.compiler_working_dir_ )

    # Use default flags
    if not final_flags:
        relative_to = DirectoryOfThisScript()
        final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

    return {
        'flags': final_flags,
        'do_cache': True
    }
