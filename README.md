# microdot

Large dotfiles with maximal opinions, used only be me.


## Colors

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
