#  encoding:  utf-8
from distutils.core import setup
from setuptools import find_packages

# from distutils.core import setup
setup(
    name="easytf",
    version="1.0",
    packages=find_packages(),
    zip_safe=False,
    description="egg test demo.",
    long_description="egg test demo, haha.",
    author="liang tingyu",
    author_email="Liangty1@lenovo.com",
    license="GPL",
    keywords=("tf", "egg"),
    platforms="any",
    url="",
)
# packages = find_packages(exclude=['rpc.*', 'util.*', 'lenovotf.*']),
# packages=['rpc', 'util', 'lenovotf', 'rpc.worker', 'rpc.central'],
