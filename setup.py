import pathlib
from setuptools import setup
# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
setup(
      name='War',
      version='0.0.1',
      description='Simulates the card game War',
      url='github.com/cameronabrams/War',
      author='Cameron F. Abrams',
      author_email='cfa22@drexel.edu',
      license='MIT',
      packages=['war'],
      include_package_data=True
)