import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name='SurvSet',
    version='0.2.5',    
    description='SurvSet package',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/ErikinBC/SurvSet',
    author='Erik Drysdale',
    author_email='erikinwest@gmail.com',
    license='MIT',
    packages=['SurvSet'],
    package_data={'SurvSet': ['_datagen/*','_datagen/output/*','_datagen/figures/*']},
    include_package_data=True,
    install_requires=['numpy', 'pandas'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ],
)

