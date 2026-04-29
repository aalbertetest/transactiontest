from setuptools import setup, find_packages

setup(
    name="localsearch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.3.0",
        "beautifulsoup4>=4.12.0",
        "markdown>=3.5.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": ["pytest>=7.4.0", "pytest-cov>=4.1.0"],
    },
    entry_points={
        "console_scripts": [
            "localsearch=cli:main",
        ]
    },
    python_requires=">=3.9",
)
