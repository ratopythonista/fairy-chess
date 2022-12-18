import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="fairy_chess",
    version="1.0.0",
    description="Teamfight Tactics Tournaments Building and Hosting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Rodrigo Guimarães Araújo",
    author_email="rodrigoara27@gmail.com",
    classifiers=[ 
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    packages=find_packages(exclude="tests"),
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=(here / "requirements.txt").read_text(encoding="utf-8").split("/n"),
    extras_require={
        "dev": ["black>=22.10.0", "pylama>=8.4.1"],
        "test": ["pytest>=7.2.0", "pytest-cov>=4.0.0"],
    },
)