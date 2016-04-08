=========== Pyfas - FA tools ===========

Pyfas is a python toolbox for flow assurance engineers.

The tool is mainly meant to process OLGA files, OLGA is a transient pipeline
simulator, standard de facto of the industry. OLGA has both input and output
files available as text files, thus this is mainly a parsing library.

At this moment in time the toolbox contains specific classes for tpl (trends at
a specific location) ppl (profile results function of the position and of the
time) and tab (look-up tables of the PVT properties) files with dedicated
methods and some minor utilities like the PI_read function.

While some python knowledge is required to really make use of all the
functionalities, some pre-defined notebooks can be of help to execute single
specific tasks (like dumping all the trends or profiles in an excel
spreadsheet). For these notebooks no python knowledge is required.

These utilities have been written for OLGA (version > 6.X) tpl and ppl files
but will be extended to Compas if and when something similar (output files)
will be available

Live demo here (no installation required)
http://mybinder.org/repo/gpagliuca/pyfas

Installation ======== pip install pyfas

Examples ========

Examples and howto are provided in the notebook folder


