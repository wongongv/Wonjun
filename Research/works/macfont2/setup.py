from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ["sys","os","pyqtgraph","PyQt4","PyQt4.Qt"], excludes = ["PyQt4.uic"])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, targetName = 'CIVET')
]

setup(name='CIVET',
      version = '1.0',
      description = 'TASEP',
      options = dict(build_exe = buildOptions),
      executables = executables)
