from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='redapi',
    version='0.2.1',
    description='Redacted.ch API',
    long_description=readme,
    author='AgNitrate',
    author_email='agnitrate@protonmail.com',
    url='https://github.com/AgNitrate/redapi',
    license=license,
    install_requires = [
        "requests"
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    package_data = {
        '': ['*.txt']
    },
    zip_safe=True
)
