# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/0xcharlo/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/0xcharlo/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for make.fun's "Post a GTA 6 meme on X" bounty: the make.fun ghost as a Florida Man on a Vice City beach at sunset — because GTA 6 isn't a game, it's a Florida documentary. The ghost is drawn by hand in the logo's own style (white body, thick black outline, sparkle eyes, magenta star coin) and worked into the scene, with a "VICE CITY / make.fun" beach sign beside it. The picture was drawn with Python and Pillow (`draw_meme.py`, using the official ghost mark from the make.fun press kit as the design reference); the post text to go with it is in `POST_TEXT.txt`.

The meme is posted on X from [@Hendry_ARCH](https://x.com/Hendry_ARCH) and this repository hands in the post's address in `POST.json`. An AI judge compares the posts two at a time, and the top 50 share $500.

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7n8phv37&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
