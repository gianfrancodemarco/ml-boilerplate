from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    version='0.1.0',
    description='A Python ML boilerplate based on Cookiecutter Data Science, providing support for data versioning (DVC), experiment tracking, Model&Dataset cards, etc.',
    author='Gianfranco Demarco',
    license='',
)
