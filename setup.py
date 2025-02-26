from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRITPION = fh.read()

with open('requirements.txt') as fi:
    REQUIRE = [
        line.strip() for line in fi.readlines()
        if not line.startswith('#')
    ]

setup(
    name='fibonacci-API',
    author="Georgios Papoutsakis",
    author_email='g.papoutsakis86@gmail.com',
    version="0.0.1",
    description="REST API for retrieving fibonacci numbers.",
    long_description=LONG_DESCRITPION,
    long_description_content_type="text/markdown",
    license='Apache',
    install_requires=REQUIRE,
    extras_require={'tests': ['pytest', 'pytest-asyncio',
                              'flake8', 'pytest-mock',
                              'requests', 'httpx']},
    data_files=[('src', ['requirements.txt'])],
    packages=find_packages('src'),
    package_dir={'': 'src'}
)