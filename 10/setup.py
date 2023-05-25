from distutils.core import setup, Extension

setup(name='cjson',
      version='1.0.0',
      author='Adam Rashi',
      description='My own simple JSON parser and serializer',
      ext_modules=[Extension('cjson', sources=['cjson.c'])])
