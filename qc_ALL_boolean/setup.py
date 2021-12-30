from setuptools import find_packages
from setuptools import setup


setup(
    name='report2sqaaas-plugin-boolean',
    version='1.0.0',
    description='Output validator for the boolean tool',
    author='Pablo Orviz',
    author_email='orviz@ifca.unican.es',
    url='http://github.com/eosc-synergy/sqaaas-reporting-plugins',
	# For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Plugins',
        'Development Status :: 3 - Alpha',
    ],
    packages=find_packages(),
    entry_points={
        'sqaaas.validators': [
            'boolean = report2sqaaas_plugins_boolean.main:BooleanValidator',
        ],
    },
)
