from distutils.core import setup

setup (
        name                    = 'hml_equation_parser',
        version                 = '1.0.0',
        py_modules              = ['hml_equation_parser'],
        packages                = ['hml_equation_parser'],
        package_data            = {'hml_equation_parser': ['*.json']},
        include_package_data    = True,
        author                  = 'Hyeongseok.Oh.Hulk',
        author_email            = 'snuboy89@gmail.com',
        url                     = "",
        description             = 'Convert eqaution sring in hml to latex string.',
    )
