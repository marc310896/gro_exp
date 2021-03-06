
import setuptools

setuptools.setup(
    name="gro_exp",
    version="0.0.3",
    description='description',
    author='Marc Hoegler',
    author_email='marc.hoegler@icvt.uni-stuttgart.de',
    classifiers=[],
    python_requires='>=3.5',
    license_files = ('LICENSE'),
    url='https://github.com/marc310896/utils',
    download_url='https://github.com/marc310896/utils/archive/refs/tags/0.0.1.tar.gz',
    install_requires=['numpy', 'pandas', 'seaborn', 'xlrd'],
    include_package_data=True,
    packages=setuptools.find_packages(),
)
