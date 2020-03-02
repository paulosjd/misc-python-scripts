"""
A simple example of a custom importer which loads a module from a file whose data is valid Python.
Suppose within the specified location is a file called `foo` containing `bar = {'eggs': 'spam'}`
After appending an instance of the class to sys.meta_path:
`>>> import foo`
`>>> dir(foo)`
['__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'bar']
`>>> foo.bar`
{'eggs': 'spam'}
"""
import pathlib
import sys
import types


class TmpFinder:
    """ Class to find and load modules in the location `/home/username/Desktop/scripts/` """
    def __init__(self):
        self.tmp_prefix = pathlib.Path.home().joinpath('Desktop', 'scripts')

    def find_module(self, fullname, path=None):
        """ For simplicity, assume the given module is a top-level file module, not a directory based
        package or sub-package. Functionality involving 'path' (for subpackage imports and relative
        imports) is ignored in this case but is easy to add.
        """
        if self.tmp_prefix.joinpath(*fullname.split('.')).exists():
            # Return the loader object here, the same object in this case
            return self

    def load_module(self, fullname):
        """ If the module already exists in `sys.modules` we *must* use it. Skipped for brevity here.
        The loader must carry out certain things before executing code inside the module """
        if fullname in sys.modules:
            return
        location = self.tmp_prefix.joinpath(*fullname.split('.'))
        try:
            mod = types.ModuleType(fullname, 'This is the doc string for the module')
            mod.__file__ = '<tmp {}>'.format(location)
            mod.__name__ = fullname
            mod.__loader__ = self
            sys.modules[fullname] = mod
            with open(location, 'r') as f:
                exec(f.read(), mod.__dict__)
            return mod
        except Exception as e:
            if sys.modules.get(fullname):
                del sys.modules[fullname]
            raise e
