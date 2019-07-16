from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dasher",
    description="Generate interactive plotly dash dashboards in an instant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="dashboard plotly dash prototyping fast",
    url="https://github.com/mfaafm/dasher",
    license="MIT",
    author="Martijn Arts",
    author_email="m.arts@gmx.net",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3",
    install_requires=[
        "dash",
        "dash-core-components",
        "dash-html-components",
        "dash-bootstrap-components>=0.6",
    ],
)
