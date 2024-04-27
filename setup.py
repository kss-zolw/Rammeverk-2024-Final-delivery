from setuptools import setup, find_packages

setup(
    name='ScrapePyFramework',
    version='1.0.0',
    author='Kristoffer Snopestad Søderkvist',
    author_email='bass4nation@gmail.com & kristoss@hiof.no',
    description='ScrapePyFramework is a Python-based web scraping framework designed for efficiency and user-friendliness. '
    'Developed as part of a school exam for the "Framework" course at Østfold University College in Norway, this framework aims '
    'to simplify the process of data extraction from the internett.',    packages=find_packages(),
    install_requires=[
        "python_version == 3.12.3",
        "requests==2.31.0",
        "urllib3==2.2.1",
        "pytest==8.1.2",
        "beautifulsoup4==4.12.3"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12.3',
    ],
)
