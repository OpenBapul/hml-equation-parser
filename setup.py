from setuptools import setup
from codecs import open
from os import path

desc = 'Convert eqaution string in hml to latex string.'

try:
    import pypandoc
    # brew install pandoc, pip install pypandoc
    here = path.abspath(path.dirname(__file__))
    long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst')

except:
    long_description = desc

setup (
        name                    = 'hml_equation_parser',
        version                 = '1.0.12',
        packages                = ['hml_equation_parser'],
        package_data            = {'': ['*.json']},
        install_requires        = ['pypandoc'],
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
        description             = desc,
        long_description        = long_description,
    )
