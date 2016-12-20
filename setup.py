from setuptools import setup

setup (
        name                    = 'hml_equation_parser',
        version                 = '1.0.1',
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
    )
