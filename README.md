# ABAP Keywords Bot

This bot was inspired by a discussion on Mastodon about the ABAP programming
language as well as by they
[@monkeyislandbot](https://social.tchncs.de/@monkeyislandbot) developed by
[Oli](https://social.tchncs.de/@oli).

## Prerequisites

_I'm using [mastodon.social](https://mastodon.social) in the examples
but of course you can and should pick the instance of your choice._

## Tools

You will need the following tools installed and configured

- Python >= 3.10
- Poetry

## Usage

First, the ABAP keywords list needs to be generated using
`build_keywords_list.py`. Next, the bot be run using `bot.py`. Alternatively,
the shell script `bot.sh` can be used to schedule the bot e.g. using `cron`.
