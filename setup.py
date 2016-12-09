from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='inet',
      version='0.1',
      description='Innovation Network Expansion Tool (INET).',
      long_description=readme(),
      url='http://github.com/nestauk/inet',
      author='James Gardiner',
      author_email='james.gardiner@nesta.org.uk',
      license='APACHEV2.0',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
      ],
      download_url='https://github.com/nesta/inet/tarball/0.1',
      classifiers=[
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
      ])
