from setuptools import find_packages
from setuptools import setup


setup(
    name='report2sqaaas-plugin-json_not_empty',
    version='1.0.0',
    description='Output validator for the json tool',
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
            'json_not_empty = report2sqaaas_plugins_json_not_empty.main:JsonNotEmptyValidator',
        ],
    },
)
