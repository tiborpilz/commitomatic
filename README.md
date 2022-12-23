[![DeepSource](https://deepsource.io/gh/tiborpilz/commitomatic.svg/?label=active+issues&show_trend=true&token=HXOj050y_0e28wz3hpVDSbg6)](https://deepsource.io/gh/tiborpilz/commitomatic/?ref=repository-badge)
[![DeepSource](https://deepsource.io/gh/tiborpilz/commitomatic.svg/?label=resolved+issues&show_trend=true&token=HXOj050y_0e28wz3hpVDSbg6)](https://deepsource.io/gh/tiborpilz/commitomatic/?ref=repository-badge)

# Commitomatic

Commitomatic is a command-line tool that uses the OpenAI ChatGPT bot to generate commit messages based on a git diff.

The queries are adjustable to customize the given commit message style.

Under the hood, it uses [acheong08's reverse engineered ChatGPT API](https://github.com/acheong08/ChatGPT) to interface with the OpenAI chatbot.

## Getting started

To build or run Commitomatic you will need to have [Nix](https://nixos.org/nix/) with flakes enabled installed on your system.

Once you have Nix installed, you can use the following command to run commitomatic:

``` sh
nix run github:tiborpilz/commitomatic
```

To authenticate with OpenAI you'll need to add your OpenAI (Auth0) user credentials in a `config.json` file. You can either use `username` and `password`:

``` json
{
  "username": "[my_username]",
  "password": "[my_password]"
}
```

or a `session_token`, which you can obtain by visiting `https://chat.openai.com/api/auth/session` while logged in to OpenAi. Simply copy the `accessToken`.

1.

``` json
{
  "session_token": "[accessToken]"
}
```
