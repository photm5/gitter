# gitter

#### An IRC-bot for broadcasting changes to git repositories.

This project uses the [push analyzer][1] library.

[1]: https://github.com/shak-mar/push_analyzer

## try it out!

#### requirements

* python 3
* git

#### cloning

Make sure to recursively clone (because of submodules):

```
git clone https://github.com/shak-mar/gitter.git --recursive
```

## configuration

* [`plugins/git/config.py`][2] lets you configure everything related with
  `push_analyzer`.
* [`plugins/irc/config.py`][3] lets you configure everything irc related.

[2]: https://github.com/shak-mar/gitter/blob/master/plugins/git/config.py
[3]: https://github.com/shak-mar/gitter/blob/master/plugins/irc/config.py

## dynamic reloading

gitter's plugin manager allows you to dynamically reload any plugin while the
bot is running. To try it out, just edit the irc config file and tell gitter in
irc:

    gitter, reload irc.config

gitter will now end the irc session, reload the config file, and start the
session again. If you changed the channel, it will join the new channel.

## licensing

This project is [licensed under MIT (Expat)][4]

[4]: https://github.com/shak-mar/packman/blob/gamelogic/LICENSE
