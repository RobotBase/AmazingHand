from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="amazingctrl",
    version="0.1.0",
    author="AmazingHand",
    author_email="support@amazinghand.com",
    description="A Python SDK for controlling the Amazing Hand",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/AmazingHandSDK", # 你可以之后修改为你的github地址
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[
        "rustypot",
        "numpy",
    ],
)
