from setuptools import find_packages, setup

setup(
    name="report2sqaaas-plugin-fairEva",
    version="1.14.0",
    description="Output validator for the fairEva tool",
    author="Pablo Orviz <orviz@ifca.unican.es>, Fernando Aguilar <aguilarf@ifca.unican.es>",
    url="http://github.com/eosc-synergy/sqaaas-reporting-plugins",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General " "Public License v3 or later (GPLv3+)",
        "Environment :: Plugins",
        "Development Status :: 3 - Alpha",
    ],
    packages=find_packages(),
    entry_points={
        "sqaaas.validators": [
            "fairEva = report2sqaaas_plugins_fairEva.main:fairEva",
        ],
    },
)
