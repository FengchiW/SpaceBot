import discord
from discord.ext.commands import Context
from pytesseract import image_to_string
from PIL import Image
import numpy as np
import cv2
from urllib.request import Request, urlopen
from io import BytesIO
import validators
from itertools import chain
from discord import Embed
import re

from util.logging import log, LogLevel


async def text_from_image(ctx: Context, img_url: str):
    try:
        # make sure the url provided is valid (this will always be true for direct attachments)
        if not validators.url(img_url):
            await ctx.send(":x: **The provided URL is invalid.**")
            return
        else:
            await ctx.send(":globe_with_meridians: **Valid URL. Checking image...**", delete_after=100)
        # send a request for the image from the given url
        req = Request(img_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                      'Chrome/50.0.2661.102 Safari/537.36'})
        # pull byte data from the requested URL
        response = urlopen(req).read()
        # read that in as a PIL image
        img: Image = Image.open(BytesIO(response))
        # in order: convert to grayscale, gaussian blur, then apply an adaptive thresholding procedure
        opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        lower_yellow = np.array([30, 120, 180])
        upper_yellow = np.array([30, 255, 255])
        blur = cv2.GaussianBlur(opencv_img, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(opencv_img, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

        img = Image.fromarray(cv2.cvtColor(opencv_img, cv2.COLOR_GRAY2RGB))
        img_binary = BytesIO()
        img.save(img_binary, 'PNG')
        img_binary.seek(0)

        pre_text1 = image_to_string(opencv_img).split("\n")
        pre_text2 = list(chain.from_iterable([i.split(",") for i in pre_text1]))[1:]
        text = [x.lower().strip() for x in pre_text2]

        channel = ctx.author.voice.channel

        tobeparsed = ""

        channelmembernames = [member.display_name.lower() for member in channel.members]

        for player in text:
            res = [(name.find(player) > 0) for name in channelmembernames]
            if any(res):
                continue
            else:
                tobeparsed += player + ", "
        
        if text != "":
            embed=Embed(title="Hey %s" % (ctx.message.author.display_name), description="The following users from /who are not in **__your__** voice channel:\n `%s`" % (tobeparsed), color=0x2ffef7)
            await ctx.send(embed=embed)
        else:
            await ctx.send(":clipboard: **This image contains no text.**")
    except IOError as e:
        await ctx.send(":x: **The provided file or URL is not an image.**")
        await log(e.__str__())
    except Exception as e:
        await log("An exception occurred while executing this command.", LogLevel.WARN)
        await log(e.__str__())
