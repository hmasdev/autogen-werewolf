# Werewolf Game with `autogen`

## Requirements

- `docker`
- OpenAI API Key
  - [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

## How to Use

### Preparation

1. Create `.env` file
2. Set `OPENAI_API_KEY`:

   ```text
   OPENAI_API_KEY=HERE_IS_YOUR_OPENAI_API_KEY
   ```

### Enjoy a Werewolf Game

The simple use is as follows:

```bash
docker compose run werewolf python -m werewolf
```

In this case, you are an observer.
If you want to join a game, use the flag `-h` or `--include-human`:

```bash
docker compose run werewolf python -m werewolf -h
```

You can see all options with `--help` option as follows:

```bash
$ docker compose run werewolf python -m werewolf --help
Usage: werewolf.py [OPTIONS]

Options:
  -n, --n-players INTEGER         The number of players. Default is 6.
  -w, --n-werewolves INTEGER      The number of werewolves. Default is 2.
  -k, --n-knight INTEGER          The number of knights. Default is 1.
  -f, --n-fortune-teller INTEGER  The number of fortune tellers. Default is 1.
  -t, --n-turns-per-day INTEGER   The number of turns per day. Default is 2.
  -s, --speaker-selection-method ESPEAKERSELECTIONMETHOD
                                  The method to select a speaker. Default is round_robin.
  -h, --include-human             Whether to include human or not.
  -o, --open-game                 Whether to open game or not.
  -l, --log TEXT                  The log file name. Default is werewolf%Y%m%d%H%M%S.log
  -m, --model TEXT                The model name. Default is gpt-3.5-turbo-16k.
  --sub-model TEXT                The sub-model name. Default is gpt-3.5-turbo-instruct.
  --help                          Show this message and exit.
```

## LICENSE

[MIT](https://github.com/hmasdev/autogen-werewolf/tree/main/LICENSE)

## Authors

- [hmasdev](https://github.com/hmasdev)

## Reference


- Autogen: [https://github.com/microsoft/autogen](https://github.com/microsoft/autogen)
- Click: [https://github.com/pallets/click](https://github.com/pallets/click)
- LangChain: [https://github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- python-dotenv: [https://github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)
- Werewolf Game (in Japanese): [https://ja.wikipedia.org/wiki/%E4%BA%BA%E7%8B%BC%E3%82%B2%E3%83%BC%E3%83%A0](https://ja.wikipedia.org/wiki/%E4%BA%BA%E7%8B%BC%E3%82%B2%E3%83%BC%E3%83%A0)
