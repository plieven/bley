from setuptools import setup

setup(
    name = "bley",
    version = "0.2-git",
    description = "intelligent greylisting daemon for postfix",
    author = "Evgeni Golov",
    author_email = "sargentd@die-welt.net",
    url = "http://bley.mx",
    license = "BSD",
    py_modules = ['bley', 'bleyhelpers', 'postfix'],
    scripts = ['bley', 'bleygraph'],
    zip_safe = False,
    install_requires=['Twisted-Core>=8.1.0', 'pyspf', 'psycopg2'],
    data_files = [('/etc/bley', ['bley.conf']), ('/usr/share/man/man1', ['bley.1'])]
)
