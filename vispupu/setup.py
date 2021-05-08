import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='vispupu',
    url='https://github.com/sscihz/vispupu',
    author='SSIHZ(sheke hunzi)',
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'numpy', 'statsmodels','re','matplotlib'],
    version='0.0.1',
    license='MIT',
    description='Simple Visualization Tool for Social Science',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)