from distutils.core import setup

setup(
    name='pyfas',
    version='0.1.5',
    author='Giuseppe Pagliuca',
    author_email='giuseppe.pagliuca@gmail.com',
    packages=['pyfas'],
    url='https://github.com/gpagliuca/pyfas.git',
    license='LICENSE.txt',
    description='Toolbox for FA engineers',
    install_requires=[
        'numpy',
        'scipy',
        'ipython',
        'jupyter',
        'xlrd',
        'pandas',
        'matplotlib',
        'pytest',
        'quantities',
        'openpyxl',
    ]
)
