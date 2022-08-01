"""Call pytest from a distutils setup.py script.
"""

import sys
import os
import os.path
import setuptools
import setuptools.dist
from distutils.spawn import spawn

__version__ = "0.1"


class _tmpchdir:
    """Temporarily change the working directory.
    """
    def __init__(self, wdir):
        self.savedir = os.getcwd()
        self.wdir = wdir
    def __enter__(self):
        os.chdir(self.wdir)
        return os.getcwd()
    def __exit__(self, type, value, tb):
        os.chdir(self.savedir)


class build_test(setuptools.Command):
    """Dummy.  This command is called at the beginning of test after
    build.  It does nothing, but it can be overridden by custom code
    in setup.py to build the test environment.
    """
    description = "set up test environment"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        pass


class test(setuptools.Command):

    description = "run the tests"
    user_options = [
        ('build-lib=', None, "build directory for modules"),
        ('build-scripts=', None, "build directory for scripts"),
        ('skip-build', None,
         "skip rebuilding everything (for testing/debugging)"),
        ('test-args=', None, "extra arguments to pass to pytest"),
    ]
    boolean_options = ['skip-build']

    def initialize_options(self):
        self.build_lib = None
        self.build_scripts = None
        self.skip_build = 0
        self.test_args = None

    def finalize_options(self):
        self.set_undefined_options('build', 
                                   ('build_lib', 'build_lib'), 
                                   ('build_scripts', 'build_scripts'))

    def run(self):
        if not self.skip_build:
            self.run_command('build')
            self.run_command('build_test')

        # Add build_lib to the module search path to make sure the
        # built packages can be imported by the tests.  Manipulate
        # both, sys.path to affect the current running Python, and
        # os.environ['PYTHONPATH'] to affect subprocesses spawned by
        # the tests.
        build_lib = os.path.abspath(self.build_lib)
        sys.path.insert(0,build_lib)
        try:
            # if PYTHONPATH is already set, prepend build_lib.
            os.environ['PYTHONPATH'] = "%s:%s" % (build_lib,
                                                  os.environ['PYTHONPATH'])
        except KeyError:
            # no, PYTHONPATH was not set.
            os.environ['PYTHONPATH'] = build_lib

        # Set build_scripts in the environment so that tests are able
        # to find and execute them.
        build_scripts = os.path.abspath(self.build_scripts)
        os.environ['BUILD_SCRIPTS_DIR'] = build_scripts

        # Do not create byte code during test.
        sys.dont_write_bytecode = True
        os.environ['PYTHONDONTWRITEBYTECODE'] = "1"

        # Must change the directory, otherwise modules in the cwd
        # would override the one from build_lib.  Alas, there seem to
        # be no way to tell Python not to put the cwd in front of
        # $PYTHONPATH in sys.path.
        testcmd = [sys.executable, "-m", "pytest"]
        if self.test_args:
            testcmd.extend(self.test_args.split())
        if self.dry_run:
            testcmd.append("--collect-only")
        with _tmpchdir("tests"):
            spawn(testcmd)


# Hack: put our command classes in priority, overriding the built-in
# command classes from setuptools if needed.  Yes, this *is* evil.
# But it is in self-defense.
cmdclass = dict(build_test=build_test, test=test)

_orig_dist_get_command_class = setuptools.dist.Distribution.get_command_class
def _patched_get_command_class(self, command):
    """A patched version of get_command_class(), putting some commands
    from distutils_pytest in priority.
    """
    if command in self.cmdclass:
        return self.cmdclass[command]
    if command in cmdclass:
        self.cmdclass[command] = cmdclass[command]
        return self.cmdclass[command]
    return _orig_dist_get_command_class(self, command)
setuptools.dist.Distribution.get_command_class = _patched_get_command_class
