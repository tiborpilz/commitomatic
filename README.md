[![DeepSource](https://deepsource.io/gh/tiborpilz/commitomatic.svg/?label=active+issues&show_trend=true&token=HXOj050y_0e28wz3hpVDSbg6)](https://deepsource.io/gh/tiborpilz/commitomatic/?ref=repository-badge)
[![DeepSource](https://deepsource.io/gh/tiborpilz/commitomatic.svg/?label=resolved+issues&show_trend=true&token=HXOj050y_0e28wz3hpVDSbg6)](https://deepsource.io/gh/tiborpilz/commitomatic/?ref=repository-badge)

# Commitomatic

Commitomatic is a command-line tool that uses the OpenAI GPT-Codex to generate commit messages based on a git diff.

## Dependencies

### Nix

Commitomatic uses [Nix](https://nixos.org/) to manage dependencies. You need to have Nix installed to build and run Commitomatic.

### OpenAI API key

Commitomatic uses the OpenAI API to generate commit messages. You need to have an OpenAI API key to use Commitomatic. You can create one [here](https://beta.openai.com/). Note that you need to be signed up to OpenAI to use the API.

Commitomatic reads the OpenAI API key from the `OPENAI_API_KEY` environment variable. You can set it in your shell configuration file.

## Running Commitomatic

To run Commitomatic, you need to have a git repository with staged changes. You can then run Commitomatic with the following command:

```bash
nix run github:tiborpilz/commitomatic
```

Commitomatic will then generate a commit message based on the staged changes and open your editor to let you edit the commit message. AFter you save and close the editor, Commitomatic will commit the staged changes using the commit message.
