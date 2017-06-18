from setuptools import setup, find_packages


def fetch_version(fname):
    result = '0.0.0'
    ptn = "__version__ = '"
    with open(fname) as fin:
        for line in fin:
            if line.startswith(ptn):
                result = line.rstrip()[len(ptn):-1]
                break
    return result


setup(
    name='noqalign',
    version=fetch_version('noqalign/noqalign.py'),
    description="put and align 'noqa F401' block comments",
    packages=find_packages(exclude=['test']),
    test_suite='test',
    author="Ariya ISIHARA",
    url="https://github.com/AriyaISIHARA",
    entry_points=dict(
        console_scripts='noqalign = noqalign:main'
    )
)
