'''
=============================================
Script to create boilerplate for a new module
=============================================

* Module file
* Unit test script
* Documentation stub and index entry
'''
from contextlib import suppress
import pathlib, re

app_name = 'drytools'


def checked_module_path(module_name, test=False):
    rel_parts = ['tests' if test else app_name] + module_name.strip().split('.')
    name_template = 'test_{}.py' if test else '{}.py'
    rel_parts[-1] = name_template.format(rel_parts[-1])
    result = pathlib.Path('.').joinpath(*rel_parts)
    result.parent.mkdir(parents=True, exist_ok=True)
    for n_parts in range(1, len(rel_parts)):
        with suppress(FileExistsError):
            pathlib.Path('.').joinpath(*rel_parts[:n_parts]).joinpath('__init__.py').touch(exist_ok=False)
    return result


def as_heading(text, fill_char='=', overbar=True):
    bar = fill_char * len(text)
    lines = [bar] if overbar else []
    lines.extend([text, bar])
    return '\n'.join(lines)


module_template = '''
\'\'\'
{module_heading}
\'\'\'


if __name__ == '__main__':
    import doctest
    doctest.testmod()

'''

test_module_template = '''
\'\'\'
{test_module_heading}

Unit tests for {module_name}
\'\'\'

import unittest
from {module_location} import {module_short_name}

# From test_example.py:
#class Test_str_repeat(unittest.TestCase):
#    def setUp(self):
#        self.fun = example.str_repeat
#    def test_retval_equal(self):
#        for calc, retval in [(lambda: self.fun('a'), 'a'),
#                             (lambda: self.fun('abc', 0), ''),
#                            ]:
#            self.assertEqual(calc(), retval)

if __name__ == '__main__':
    unittest.main()

'''

doc_stub_template = '''
.. automodule:: {app_name}.{module_name}
  :members:
'''


def make_new_module(module_name):
    module_name = module_name.strip()
    module_parts = [app_name] + module_name.split('.')
    doc_source_path = pathlib.Path('./docs/source')
    context = {'module_path': checked_module_path(module_name, test=False),
               'test_module_path': checked_module_path(module_name, test=True),
               'module_name': module_name,
               'doc_stub_path': doc_source_path.joinpath('code_pages/{module_name}.rst'.format(**locals())),
               'module_heading': as_heading(module_name),
               'test_module_heading': as_heading('Unit tests for module {module_name}'.format(**locals())),
               'module_location': '.'.join(module_parts[:-1]),
               'module_short_name': module_parts[-1],
               'module_name': module_name,
               'app_name': app_name,
               }
    for mode, path_key, template in [('x', 'module_path', module_template),
                                     ('x', 'test_module_path', test_module_template),
                                     ('x', 'doc_stub_path', doc_stub_template),
                                    ]:
        with context[path_key].open(mode=mode) as out_stream:
            print(template.format(**context), file=out_stream)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Add a new empty module and assoicated files')
    parser.add_argument('module', help='Name of new module (can include package path.  eg: my_pkg.my_module)')
    args = parser.parse_args()
    make_new_module(args.module)
