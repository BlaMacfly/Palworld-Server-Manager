from setuptools import setup, find_packages

setup(
    name="palworld-server-manager",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pillow",
    ],
    entry_points={
        "console_scripts": [
            "palworld_manager=palworld_manager:main",
        ],
    },
    package_data={
        "": ["Icon_256.png"],
    },
    author="Palworld Server Manager Team",
    author_email="contact@example.com",
    description="Interface graphique pour gérer un serveur Palworld",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/palworld-server-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
    ],
)
