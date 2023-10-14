# microdot

My preferred defaults.  Not really dotfiles but they end up being the same thing.

I have accounts on multiple computers and they should be configured to have almost identical
behaviour with only a few local differences between them.  The _microdot_ repo factors out
the config which is the same across all machines and places it alongside logic to deploy
those files to a local system.

Most pieces of software let me configure them in two places:
* `/etc/foorc` for system defaults
* `~/.config/foorc` for my personal config

Most pieces of software allow you to source other config files from
the main config file.  _microdot_ inserts itself into my local
dotfiles by adding hooks like `source <path>` or `include <path>`, annotated with
comments so that it can find them again later.

This gives an extra level of config for each piece of software
supported by microdot:
* `/etc/foorc` for system defaults
* `~/.config/microdot/foorc` for my generic, cross-host config
* `~/.config/foorc` for my config _specific to this machine_

For example, my `~/.bashrc` on a server where I want to use UTC ends up looking like this:

```sh
-----BEGIN MICRODOT-----
source /home/edwardspeyer/.config/microdot/bash/bashrc
-----END MICRODOT-----

export TZ=UTC
```


## Note: Colors

Most colors seem to come in three shades: regular, bright, and dismal.  In
particular, some colors only show up in their dismal forms when using fish via
ssh:

                       bryellow
                yellow |      fish_color_quote
    kitty       |      |      |
        local   CECB00 FFFD00 CECB00
        ssh     CECB00 FFFD00 878700*
    Terminal.app
        local   AFAD24 ECEC15 AFAD24
        ssh     AFAD24 ECEC15 A09F25*


In the 256 ANSI color palette, these yellows are `color3`, `color11`, and
`color100`.  The best fix for this is probably to tell fish to avoid these
colors altogehter, but it might also be a better general solution to remove all
dismal colors from kitty's color palette.


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
