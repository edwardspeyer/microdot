# microdot

My preferred defaults.  Not really dotfiles but they end up being the same
thing.

I have accounts on multiple computers and they should be configured to have
almost identical behaviour with only a few local differences between them.  The
_microdot_ repo factors out the config which is the same across all machines
and places it alongside logic to deploy those files to a local system.

Most Unix software is configured in two places:
* `/etc/foorc` for system defaults
* `~/.config/foorc` for my personal config

Most will also allow you to source one config file from another.
_microdot_ uses this feature to insert itself into my local dotfiles by adding hooks like
`source <path>` or `include <path>`, annotated with comments so that it can
find them again later.

This gives an extra level of config for each piece of software supported by
microdot:
* `/etc/foorc` for system defaults
* `~/.config/microdot/foorc` for my generic, cross-host config
* `~/.config/foorc` for my config _specific to this machine_

For example, my `~/.bashrc` on a server where I want to use UTC ends up looking
like this:

```sh
# -----BEGIN MICRODOT-----
source /home/edwardspeyer/.config/microdot/bash/bashrc
# -----END MICRODOT-----

export TZ=UTC
```

## Modules

```
# My favourite fonts
microdot.fonts

# My gpg key stubs
microdot.gnupg

# Dotfile hooks
microdot.hooks

# My favourite debian and python packages
microdot.packages.debian
microdot.packages.python

# Build some things from source
microdot.packages.source.delta
microdot.packages.source.fish
microdot.packages.source.i3
microdot.packages.source.tmux

# More complex config
microdot.terminfo
microdot.thunderbird
microdot.x11
```


## References

* [`bufexplorer`](https://github.com/jlanzarotta/bufexplorer)
* [`fzf.vim`](https://github.com/junegunn/fzf.vim)
* [`fzf`](https://github.com/junegunn/fzf)
* [`goyo.vim`](https://github.com/junegunn/goyo.vim)
* [`nerdtree`](https://github.com/preservim/nerdtree)
* [`vim-gnupg`](https://github.com/jamessan/vim-gnupg)
* [`vim-lsp-settings`](https://github.com/mattn/vim-lsp-settings)
* [`vim-lsp`](https://github.com/prabirshrestha/vim-lsp)
* [`vim-plug`](https://github.com/junegunn/vim-plug)
