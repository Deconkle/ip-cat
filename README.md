# ip-cat
Ip cat is a python based webserver that returns an image along with the IP information of the requesting host.

This was built for the [Media Player](https://github.com/samuelmaddock/gm-mediaplayer) Garry's Mod addon.

When using Media Players, any url can be requested - even your own. That image will then be sent to every client who has the media player active. 

The images get created in memory, and are never saved to disk meaning we're not leaking anyone's IP address because that's like, not cool man!!

Write your ipinfo api key to a ``IP_KEY`` enviornment variable (e.x ``SET IP_KEY=xxxxxxx``)

# Requirements
- [ipinfo.io](https://ipinfo.io) API key (free)
- A domain name you can host under (Script is configured for cloudflare hosts)
- A cat (not required)

# Cat in action
![image](https://user-images.githubusercontent.com/24526230/190531489-0805ef7c-fba0-4e15-ab57-1e5b7bd79d88.png)
