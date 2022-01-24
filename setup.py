import setuptools


setuptools.setup(
    name="utils",
    version="0.0.1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=['numpy','pandas','seaborn'],
    include_package_data=True,
)
