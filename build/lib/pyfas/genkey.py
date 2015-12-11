import re
from string import Template


class Genkey:
    def __init__(self, fname):
        self.fname = fname
        with open(self.fname) as fobj:
            self.template = Template(fobj.read())
            fobj.seek(0)
            self.variables = re.findall("\$\w*", fobj.read())

    def write_genkey(self, values, new_name="new_case.genkey"):
        genkey = self.template.substitute(values)
        with open(new_name, "w") as fobj:
            fobj.write(genkey)
