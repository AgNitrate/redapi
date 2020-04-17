import setuptools
with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name='redapi',
    version='0.2.1',
    author='AgNitrate',
    author_email='agnitrate@protonmail.com',
    description='Redacted.ch API',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/AgNitrate/redapi',
    license=license,
    install_requires = [
        "requests"
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
