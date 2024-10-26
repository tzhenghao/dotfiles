# Introduction

[![Build Status](https://travis-ci.org/tzhenghao/dotfiles.svg?branch=master)](https://travis-ci.org/tzhenghao/dotfiles)
[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

Here are some of my software development configurations.
They are all in their original file formats as I want them to be short, simple and easy to refer to. Enjoy!

## Configurations For

1. Vim (`.vimrc`)
2. Neovim (`neovim/`)
3. Bash (`.bashrc`)
4. Zsh (`.zshrc`)
5. Tmux (`.tmux.conf`)
6. Git (`.gitconfig`)
7. Alacritty (`alacritty.toml`) - add to `~/.config/alacritty/alacritty.toml`
8. `.Xmodmap` - swaps Control and Caps Lock keys

## OS Specific Settings

### Ubuntu

Setting Night Light/Shift feature intensity:

```bash
gsettings set org.gnome.settings-daemon.plugins.color night-light-temperature 5000
```

#### Disabling mouse acceleration

```bash
xset m 0 0
```

```bash
gsettings set org.gnome.desktop.peripherals.keyboard repeat-interval 30
gsettings set org.gnome.desktop.peripherals.keyboard delay 270
```

### MacOS

Make sure the following packages are installed:

1. [vim-plug](https://github.com/junegunn/vim-plug)
2. [Homebrew](https://brew.sh)
3. [fzf](https://github.com/junegunn/fzf)
    - Also add fzf shell integration (see `fzf.zsh` file)

#### Key repeat

fast

#### Delay until repeat

shortest

#### Disabling mouse acceleration

```bash
defaults read .GlobalPreferences com.apple.mouse.scaling
defaults write .GlobalPreferences com.apple.mouse.scaling -1
```

#### Mac Terminal App color settings

![Mac Terminal App color settings](images/mac-terminal-app-color-settings.png)

![Mac Terminal App keyboard settings](images/mac-terminal-app-keyboard-settings.png)

#### MacOS Stage Manager settings

1. Open a new "Desktop" then right click on Finder -> Options -> Assign To -> All Desktops

#### Vim for VSCode

Enable key repeats:

```bash
defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false
```

Change Caps Lock key to Control: \
*System Preferences -> Keyboard -> Modifier Keys -> change Caps Lock to Control*

### iOS

Key repeat: 0.05sec

Delay until repeat: 0.20sec
