import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrenaper",
    version="0.0.10",
    author="Damian Sastre",
    author_email="author@example.com",
    description="Python implementation of Argentina's RENAPER API service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tagercito/pyrenaper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["attrs==21.2.0",
                      "certifi==2021.5.30",
                      "chardet==4.0.0",
                      "idna==2.10",
                      "iniconfig==1.1.1",
                      "packaging==20.9",
                      "Pillow==8.2.0",
                      "pluggy==0.13.1",
                      "py==1.10.0",
                      "pyparsing==2.4.7",
                      "pytest==6.2.4",
                      "requests==2.25.1",
                      "toml==0.10.2",
                      "urllib3==1.26.5",
                      "zxing",
                      "coverage"],
    include_package_data=True,
    packages=['pyrenaper'],
    python_requires=">=3.8",
)

