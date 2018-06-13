# halp-encoding
Did you know that Python has a quite awesome help utility that works for all
kinds of stuff like keywords and modules? You can enter the interactive help
utility by simply typing `help()` in a prompt.

A beginnner asked on chat.freenode.nets lovely channel ##learnpython, why his
command, `help(lambda)`, did not work. This is because `lambda` is a keyword
that cannot be used like this, so the interpreter throws a `SyntaxError` back.
For fun I decided to write a codec where this is possible, only for the
help function (or rather, only for any callable you decide to name help :D)

`halp.py` adds the `halp` codec when loaded so you can `# coding=halp`. This
allows lines like:

``` python
help(if)
help(except)
```

The best way to see it in action is to read `example.py`, fire up an
interpreter and do:

``` python
>>> import halp
>>> import example
```
