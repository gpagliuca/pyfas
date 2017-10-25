from distutils.core import setup

setup(
    name='pyfas',
    version='0.3.1',
    author='Giuseppe Pagliuca',
    author_email='giuseppe.pagliuca@gmail.com',
    packages=['pyfas'],
    url='https://github.com/gpagliuca/pyfas.git',
    license='LICENSE.txt',
    description='Toolbox for Flow Assurance engineers',
    install_requires=[
        'numpy',
        'scipy',
        'ipython',
        'jupyter',
        'xlrd',
        'pandas',
        'matplotlib',
        'pytest',
        'openpyxl',
        'quantities',
    ]
)
