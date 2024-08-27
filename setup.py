from setuptools import setup, find_packages

# Read the contents of README.md for long description
try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''  # Fallback if README.md is not found

setup(
    name='promptdb',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
        'requests',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'promptdb=promptdb.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['config.json'],  # Ensure the config file is included
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI app for querying a MySQL database using natural language and ChatGPT.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mattlickess/promptdb',  # Update with your GitHub repository URL
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)
