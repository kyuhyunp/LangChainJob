# LangChainJob

## Issues and Solution

### ModuleNotFoundError: No module named 'apt_pkg' after python upgrade to version 3.10
```
sudo apt upgrade
```
caused

```
ModuleNotFoundError: No module named 'apt_pkg'
```
after upgrading python to version 3.10

### Solution

Removing the alternative I had added to point python3 to python3.10
```
sudo update-alternatives --remove-all python3
```

```
sudo apt-get install python3.10-dev python3.10-venv
```

Fixing the symlink to point at 3.10
```
sudo ln -sf /usr/bin/python3.10 /usr/bin/python3
```

symlink is simply a shortcut to another file.
