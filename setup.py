from setuptools import setup, find_packages

setup(
    name="mytwofa",
    version="0.1.0",
    author="Sakchart Ngamluan",
    author_email="kcommerce@gmail.com",
    description="A simple desktop 2FA TOTP Authenticator with Tkinter",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kcommerce/mytwofa",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "mytwofa = mytwofa.myTwoFA:main",  # requires main() wrapper in myTwoFA.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.7",
)
