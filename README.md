
# Discord and Telegram Mirror/Repinger 
These two different scripts allow you to read messages coming into any Telegram or Discord channel via an account for the respective social, and forward them to another Discord channel via webhook.

I made this script for a little project I needed to do, there is no support for videos on Telegram and of files on Discord (other than images or videos) because it was not useful to me, but it can be easily implemented.

On this basis one can easily make several projects or perhaps even just change the webhook for another platform.

[![Watch the video](https://i.imgur.com/mEQ4NcZ.png)](https://www.youtube.com/watch?v=A8x83WgsiBM)

# Table of contents

- [Disclaimer](#disclaimer)
- [Installation](#installation)
- [Discord](#discord)
    - [How to get an account token](#how-to-get-an-account-token)
    - [Confirguartion](#configuration)
    - [Run](#run)
- [Telegram](#telegram) 
    - [Confirguartion](#configuration)
    - [Run](#run)
- [Contributing](#contributing)
- [Contact me](#contact-me)

## Disclaimer
What this script does is against Discord's TOS (and I guess Telegram's as well). They were made for informational purposes only and I take no responsibility for their use.

# Installation

```
py -m pip install -r requirements.txt
```

# Discord

[(Back to top)](#table-of-contents)

Through a Discord account token you can reping any message to any server where the account has access. 
It currently supports any type of message or webhook.

## How to get an account token.
Go to the discord webapp and open the Chrome console

`CTRL + SHIFT + J` on Windows/Linux

`CMD + Option + J` on Mac
```js
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
```
Paste this script and you will have the token.
![image](https://i.imgur.com/MOK1YNB.png)
I don't think it's necessary to say that it gives total access to your account so it doesn't have to be shared with anyone.
When you reset the password it will change.

## Configuration
Inside the file ./discord_repinger/settings.yaml enter the token of the account to be used and as in the example the [ids of the channels](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) to be monitored with respective webhook to send them to.
Keep in mind that the account it is monitoring must have access to read the channels you want to monitor.
![image](https://i.imgur.com/fabvrnY.png)

## Run

```
cd ./discord_repinger/
py main.py
```

# Telegram

[(Back to top)](#table-of-contents)

Via some [app's access tokens](https://core.telegram.org/api/obtaining_api_id), you can do the same thing as Discord.
![image](https://i.imgur.com/EZywKkO.png)

## Configuration
Inside the file ./telegram_repinger/settings.yaml enter your app ids and telegram hashes. 

Unlike Discord, Telegram doesn't give you direct access to image urls, so I implemented Imgur so you can upload them online first and then send them via Discord Webhook. If you wish to send them, within the same file enter your client id and secret [from the Imgur apis](https://api.imgur.com/oauth2/addclient).

Having done that as Discord just enter the list of Discord [channels](https://github.com/GabrielRF/telegram-id#web-channel-id)/Discordwebhooks to monitor/to send the messages to and you will be ready. 
Keep in mind that the account that is monitoring must have access to read the channels you want to monitor.

![image](https://i.imgur.com/KyKqVBN.png)

## Run

```
cd ./telegram_repinger/
py main.py
```
On first startup you may need to confirm the number by text message.

# Contributing

[(Back to top)](#table-of-contents)

Your contributions are always welcome!

# Contact me

[Mail](mailto:glizzykingdreko@protonmail.com) | [Twitter](https://twitter.com/glizzykingdreko)