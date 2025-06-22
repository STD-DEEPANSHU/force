# Multi-Channel Force-Subscribe Telegram Bot 🤖

This bot forces new group members to join **multiple Telegram channels** before they can chat.

Built with **Pyrogram**. Ready to deploy on **Heroku** in 1 click.

---

## 🚀 Features

- ✅ Force users to join multiple channels
- 🔁 Recheck button: “I've Joined All”
- 🔇 Mute until joined
- 📦 Deploy to Heroku
- 🧬 `/clone` command for self-replication

---

## ⚙️ Environment Variables

| Variable       | Description                                 |
|----------------|---------------------------------------------|
| `API_ID`       | From https://my.telegram.org                |
| `API_HASH`     | From https://my.telegram.org                |
| `BOT_TOKEN`    | From @BotFather                             |
| `FORCE_CHANNELS` | Space-separated usernames (e.g. `@ch1 @ch2`) |

---

## 💻 Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/STD-DEEPANSHU/force)

> 🔁 Replace `yourusername/yourrepo` with your GitHub repo link.

---

## 🧬 Clone Feature

Once deployed, anyone can DM your bot and type `/clone` to deploy their own version.

---

## 👨‍💻 Built With

- Python 3.10
- Pyrogram
- tgcrypto

---

## 📄 License

MIT License — Use it, fork it, remix it. Just don’t sell it without love.
