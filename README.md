# ABAP Keywords Bot

This bot was inspired by a discussion on Mastodon about the ABAP programming language as well as by they
[@monkeyislandbot](https://social.tchncs.de/@monkeyislandbot) developed by [Oli](https://social.tchncs.de/@oli).

## Prerequisites

_I'm using https://mastodon.social in the examples but of course you can and should pick the instance of your choice._

## Tools

You will need the following tools installed and configured

- Python >= 3.9
- Serverless (https://www.serverless.com/)
- AWS CLI (and a working AWS account, obviously)

## Test locally

- Create a new application on your instance of choice (https://mastodon.social/settings/applications)
- Make sure you have the `write:statuses` scope activated
- Clone and `pipenv install --dev`

```
sls invoke local -function bot --verbose \
 -param access_token=<your application acess token> \
 -param api_url=https://mastodon.social/api/v1/
```

## Deploy to AWS

As seen above, the bot requires two parameters, `access_token` and `api_url`, that are mapped to environment variables by the framework.
These can either be passed using command line parameters (`-param`) or configured in the serverless dashboard of the app.

Somehow I didn't get the [Serverless Python Requirements](https://www.serverless.com/plugins/serverless-python-requirements/)
to work with my version of `pipenv`. After creating the `requiremtens.txt` manually using `pipenv requirements > requirements.txt` the deployment with
`serverless deploy` succeeded. This takes some time so get
green tea 🍵 or beer 🍺 in the meantime.
