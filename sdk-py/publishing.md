## Quick guide on how to publish a new version of the package to PyPi

1. Update the version in `pyproject.toml` file (on line 4) to the new version you want to publish.
   Follow semantic versioning (e.g., 1.0.0, 1.1.0, 2.0.0).
2. Update the `CHANGELOG.md` file with the new version and the changes made since the last version.
   Follow the format in the existing changelog entries.
3. Commit the changes to your version control system (e.g., git).
4. Make sure you have the latest version of PyPA's `build` and `twine` installed:
   ```sh
   python3 -m pip install --upgrade build twine
   ```
5. Now run this command from the same directory where pyproject.toml is located:
    ```sh
   python3 -m build
   ```
   This command should output a lot of text and once completed should generate two files in the dist directory:
   ```dist/
   ├── example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
   └── example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz
   ```
6. Now run Twine to upload all the archives under ```dist```:
   ```sh
   python3 -m twine upload  dist/*
   ```
7. Follow the prompts to enter your PyPi API token.
8. Afterward, you should see your new version available on PyPi: https://pypi.org/project/OuterRail/, 
   where it is advisable to check that the package can be ```pip install```-ed correctly.

> **_Note_**: More detailed instructions can be found in the official 
> [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

### TLDR script:
```sh
   python3 -m pip install --upgrade build twine &&
   python3 -m build &&
   python3 -m twine upload  dist/*
```