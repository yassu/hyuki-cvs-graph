from setuptools import setup
from hyuki_graph import __VERSION__

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
]

setup(
    name='hyuki-cvs-graph',
    version=__VERSION__,
    description='view graph for working log',
    # long_description=open('README.rst').read(),
    author='Yassu',
    author_email='mathyassu@gmail.com',
    url='https://github.com/yassu/hyuki-cvs-graph',
    classifiers=classifiers,
    entry_points="""
       [console_scripts]
       hyuki-graph = hyuki_graph.hyuki_graph:main
    """,
)

