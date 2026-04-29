from setuptools import setup, find_packages

setup(
    name="sprout-lang",
    version="0.1.0",
    description="Sprout: a small, bytecode-compiled programming language",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "sprout=sprout.__main__:main",
        ],
    },
)
