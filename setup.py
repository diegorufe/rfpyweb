import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="rfpyweb",  # Replace with your own username
    version="0.0.1",
    author="Diego Ruiz",
    author_email="diegorufe@gmail.com",
    description="Library utilities for web flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegorufe/rfpyweb",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
