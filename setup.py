from setuptools import setup, find_packages

setup(
    name="canvas-download",
    version="0.1",
    description="Package to download files from canvas",
    url="#",
    author="emzoo",
    install_requires=["canvasapi", "colorama", "PyInquirer", "PyYAML", "python-dotenv"],
    author_email="",
    packages=["canvasdownload"],
    entry_points="""
        [console_scripts]
        canvas=canvasdownload.main:main
    """,
    zip_safe=False,
)
