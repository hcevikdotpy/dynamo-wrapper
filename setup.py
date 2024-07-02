from setuptools import setup, find_packages

setup(
    name="dynamo-wrapper",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "boto3>=1.17.0",
        "botocore>=1.20.0",
    ],
    extras_require={
        'dev': [
            'moto>=2.0.0',
            'pytest>=6.0.0',
        ],
    },
    author="Huseyin Cevik",
    author_email="huseyin.cevik@outlook.de",
    description="A PyMongo-like wrapper for DynamoDB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hcevikGA/dynamo-wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)