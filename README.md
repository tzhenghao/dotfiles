# Introduction

[![Build Status](https://travis-ci.org/tzhenghao/dotfiles.svg?branch=master)](https://travis-ci.org/tzhenghao/dotfiles)
[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

Here are some of my software development configurations.
They are all in their original file formats as I want them to be short, simple and easy to refer to. Enjoy!

## Configurations For:
1. Vim (`.vimrc`)
2. Bash (`.bashrc`)
3. Zsh (`.zshrc`)
4. Tmux (`.tmux.conf`)
5. Git (`.gitconfig`)
6. Alacritty (`alacritty.yml`)
7. `.Xmodmap` - swaps Control and Caps Lock keys


## **OS Specific Settings**

### **Ubuntu**

Setting Night Light/Shift feature intensity:

```bash
gsettings set org.gnome.settings-daemon.plugins.color night-light-temperature 5000
```

Disable mouse acceleration:

```bash
xset m 0 0
```

```bash
gsettings set org.gnome.desktop.peripherals.keyboard repeat-interval 30
gsettings set org.gnome.desktop.peripherals.keyboard delay 270
```

### **MacOS**

Make sure Homebrew is installed!

Key repeat: fast

Delay until repeat: shortest

### **iOS**

Key repeat: 0.05sec

Delay until repeat: 0.20sec