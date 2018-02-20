from setuptools import setup, find_packages

setup(
    name='sqlalchemy-dst',
    description='SQLAlchemy Dictionary Serialization Tools.',
    keywords='sqlalchemy python dict serialize tool',
    version='1.0.1',
    url='https://github.com/yarbshk/sqlalchemy-dst',
    author='Yuriy Rabeshko',
    author_email='george.rabeshko@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    install_requires=[
        'sqlalchemy>=0.9.4'
    ]
)
