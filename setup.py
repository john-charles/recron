from distutils.core import setup

setup(name='recron',
    version='1.0',
    packages=[
        'librecron',
        'librecron.util'
    ],
    scripts= [
        "recron",
        "recrond",
        "recron-launch"
    ]
)