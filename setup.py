from setuptools import setup, find_packages

setup(
    name="p3Logging",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pyjson5"],
    description="P3 Logging Module - simple add-on features to Python's logging module.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Paul Painter",
    url="https://github.com/ppainterpython/p3Logging",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="logging, development",
    python_requires=">=3.6",
)