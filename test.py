import os

print("file")
print(__file__)

print("os.path.dirname(__file__)")
print(os.path.dirname(__file__))

print("os.path.abspath(os.path.dirname(__file__))")
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

print('-'*50)
print(os.path.join(basedir,'data.sqlite'))
