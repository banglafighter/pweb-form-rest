from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "README.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = [
        'marshmallow==3.20.1',
        'apispec==6.3.0',
        'marshmallow-sqlalchemy'
    ]

    if env and env == "code":
        return dependency

    return dependency + ["ppy-common", "pweb-orm", "ppy-file-text"]


setup(
    name='pweb-form-rest',
    version='0.0.2',
    url='https://github.com/problemfighter/pweb-form-rest',
    license='Apache 2.0',
    author='Problem Fighter',
    author_email='problemfighter.com@gmail.com',
    description='Make Form & REST API convention, Validate request and produce response for PWeb application. It can produce Swagger API Documentation as well',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)
