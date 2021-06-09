from setuptools import setup
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='augmentedbondingcurve',
    version=get_version("augmentedbondingcurve/__init__.py"),
    description='Python implementation of the Bancor automated Market Maker',
    url='https://github.com/CommonsBuild/augmented-bonding-curve-model',
    author='YGG Anderson',
    author_email='example@example.com',
    license='',
    packages=['augmentedbondingcurve'],
    install_requires=['numpy', 
                      'bokeh',
                      'cadCAD',
                      'holoviews',
                      'hvplot',
                      'matplotlib',
                      'panel',
                      'param',
                      'pandas',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',      
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
