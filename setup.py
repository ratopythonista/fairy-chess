import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="fairy-chess",
    version="0.1.0",
    description="Teamfight Tactics Tournaments Building and Hosting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    author="A. Random Developer",
    author_email="rodrigoara27@gmail.com",
    classifiers=[ 
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="sample, setuptools, development",
    packages=find_packages(where="fairy_chess"), 
    python_requires=">=3.9",
    install_requires=(here / "fairy_chess/requirements.txt").read_text(encoding="utf-8").split("/n"),
    extras_require={
        "dev": ["black>=22.10.0", "pylama>=8.4.1"],
        "test": ["pytest>=7.2.0", "pytest-cov>=4.0.0"],
    },
    data_files=[("templates", ["templates"])],
)