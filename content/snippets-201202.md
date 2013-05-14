Date: 2012-02-29
Title: Snippets of February 2012
Slug: snippets-201202
Category: Blog
Tags: git, python, vim, snippets

Naturally, as a developer I learn new awesome things almost every day.
I thought it might be a good idea to keep track of all those small Ah-Ha!
moments and release a snippets post every month.

# Global .gitignore

When I wanted to contribute code to
[Pelican](https://github.com/ametaireau/pelican) I naively added
``.ropeproject`` to that repo's ``.gitignore`` file. As a result, I was told in
the codereview that I should not pollute other project's ``.gitignore`` files
with unrelated stuff but rather use a global ``.gitignore`` file instead. How
could I not know about this until now?!?

Just add the following code to your .gitconfig:

    ::text
    [core]
    excludesfile = $HOME/.gitignore_global

Then create the ``.gitignore_global`` file and put stuff inside that your
editors of choice might produce.

# Better Omni Completion in Vim

So I finally got the ``hjkl`` keys for movement into my muscle memory. Now it
annoys me that I have to use the arrow keys when I want to browse through the
various options that the code completion suggests. There is a vimbit for that:

    ::text
    set completeopt=longest,menuone

    " found here: http://stackoverflow.com/a/2170800/70778
    function! OmniPopup(action)
        if pumvisible()
            if a:action == 'j'
                return "\<C-N>"
            elseif a:action == 'k'
                return "\<C-P>"
            endif
        endif
        return a:action
    endfunction
    inoremap <silent><C-j> <C-R>=OmniPopup('j')<CR>
    inoremap <silent><C-k> <C-R>=OmniPopup('k')<CR>

# Vimbits

Speaking of vimbits: [vimbits.com](http://vimbits.com/) recently flew through
my Twitter stream. I spent an hour there. As a result my ``.vimrc`` just
exploded with all kinds of awesomeness.

# Showing git branch in prompt

I thought that I was typing ``git branch`` way too often (actually I type
``git br``, of course).

    ::text
    export PS1='\w\[\033[31m\]$(__git_ps1 "(%s)") \[\033[01;34m\]$\[\033[00m\] '

Hint: In order for this to work, you need to install git via Homebrew on OSX.
