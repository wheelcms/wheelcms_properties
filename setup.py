from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='wheelcms_properties',
      version=version,
      description="Extendible properties for WheelCMS types",
      long_description=open("README.md").read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ivo van der Wijk',
      author_email='wheelcms@in.m3r.nl',
      url='http://github.com/wheelcms/wheelcms_properties',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytest',
          'mock',
      ],
      entry_points={
      },

      )

