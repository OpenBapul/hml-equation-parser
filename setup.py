from setuptools import setup
from codecs import open
from os import path
import pypandoc

here = path.abspath(path.dirname(__file__))
# brew install pandoc, pip install pypandoc
long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst')

setup (
        name                    = 'hml_equation_parser',
        version                 = '1.0.3',
        py_modules              = ['hml_equation_parser'],
        packages                = ['hml_equation_parser'],
        package_data            = {'hml_equation_parser': ['*.json']},
        include_package_data    = True,
        author                  = 'Hyeongseok.Oh.hulk',
        author_email            = 'snuboy89@gmail.com',
        url                     = "https://github.com/OpenBapul/hml-equation-parser",
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.5',
        ],
        description             = 'Convert eqaution string in hml to latex string.',
        long_description        = long_description,
    )
