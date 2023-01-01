from setuptools import setup

setup(
    name='qpatch',
    version='1.0.0',
    py_modules=['qpatch'],
    install_requires=[
        'Click',
        'sgtpyutils',
    ],
    entry_points='''
        [console_scripts]
        qpatch=qpatch:qpatch
    ''',
)
