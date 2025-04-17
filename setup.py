from setuptools import setup, find_packages

long_description = ""
with open("README.md", "r", encoding="utf-8") as f:
    contents = f.readlines()
    for line in contents:
        if "user-attachments/assets" not in line:
            long_description += line

setup(
    name="llamashell",
    version="0.0.3",
    author="Ashraff Hathibelagal",
    description="A powerful shell that's powered by a locally running LLM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hathibelagal-dev/llamashell",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[ 
        "transformers>=4.49.0",
        "torch",
        "huggingface_hub",
        "requests",
        "prompt_toolkit",
        "dnspython"
    ],
    entry_points={
        "console_scripts": [
            "llamashell=llamashell.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="ai shell llm llama qwen localllama terminal linux macos",
    project_urls={
        "Source": "https://github.com/hathibelagal-dev/llamashell",
        "Tracker": "https://github.com/hathibelagal-dev/llamashell/issues",
    },
)
