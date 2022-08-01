"""Call pytest from a setup.py script.
"""

import distutils.cmd
import distutils.command.build_py
import distutils.command.sdist
from distutils.core import setup
import distutils.file_util
import distutils.log
from glob import glob
import os
from pathlib import Path
from stat import ST_ATIME, ST_MTIME, ST_MODE, S_IMODE
import string
import distutils_pytest
try:
    import setuptools_scm
    version = setuptools_scm.get_version()
except (ImportError, LookupError):
    try:
        import _meta
        version = _meta.__version__
    except ImportError:
        distutils.log.warn("warning: cannot determine version number")
        version = "UNKNOWN"

docstring = __doc__
doclines = docstring.strip().split("\n")

class copy_file_mixin:
    """Distutils copy_file() mixin.

    Inject a custom version version of the copy_file() method that
    does some substitutions on the fly into distutils command class
    hierarchy.
    """
    Subst_srcs = {"distutils_pytest.py"}
    Subst = {'DOC': docstring, 'VERSION': version}
    def copy_file(self, infile, outfile,
                  preserve_mode=1, preserve_times=1, link=None, level=1):
        if infile in self.Subst_srcs:
            infile = Path(infile)
            outfile = Path(outfile)
            if outfile.name == infile.name:
                distutils.log.info("copying (with substitutions) %s -> %s",
                                   infile, outfile.parent)
            else:
                distutils.log.info("copying (with substitutions) %s -> %s",
                                   infile, outfile)
            if not self.dry_run:
                st = infile.stat()
                try:
                    outfile.unlink()
                except FileNotFoundError:
                    pass
                with infile.open("rt") as sf, outfile.open("wt") as df:
                    df.write(string.Template(sf.read()).substitute(self.Subst))
                if preserve_times:
                    os.utime(str(outfile), (st[ST_ATIME], st[ST_MTIME]))
                if preserve_mode:
                    outfile.chmod(S_IMODE(st[ST_MODE]))
            return (str(outfile), 1)
        else:
            return distutils.file_util.copy_file(infile, outfile,
                                                 preserve_mode, preserve_times,
                                                 not self.force, link,
                                                 dry_run=self.dry_run)

class meta(distutils.cmd.Command):
    description = "generate meta files"
    user_options = []
    meta_template = '''
__version__ = "%(version)s"
'''
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        values = {
            'version': self.distribution.get_version(),
        }
        with Path("_meta.py").open("wt") as f:
            print(self.meta_template % values, file=f)

class sdist(copy_file_mixin, distutils.command.sdist.sdist):
    def run(self):
        self.run_command('meta')
        super().run()
        subst = {
            "version": self.distribution.get_version(),
            "url": self.distribution.get_url(),
            "description": self.distribution.get_description(),
            "long_description": self.distribution.get_long_description(),
        }
        for spec in glob("*.spec"):
            with Path(spec).open('rt') as inf:
                with Path(self.dist_dir, spec).open('wt') as outf:
                    outf.write(string.Template(inf.read()).substitute(subst))

class build_py(copy_file_mixin, distutils.command.build_py.build_py):
    def run(self):
        self.run_command('meta')
        super().run()



setup(
    name = "distutils-pytest",
    version = version,
    description = doclines[0],
    long_description = "\n".join(doclines[2:]),
    author = "Rolf Krahl",
    author_email = "rolf@rotkraut.de",
    url = "https://github.com/RKrahl/distutils-pytest",
    license = "Apache-2.0",
    py_modules = ["distutils_pytest"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
    cmdclass = {'build_py': build_py, 'sdist': sdist, 'meta': meta},
)
