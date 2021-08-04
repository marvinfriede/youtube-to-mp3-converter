# /usr/bin/env python3.8

# SIMPLE YOUTUBE MP3 DOWNLOADER USING PYTUBE
#
# 
# install pytube with: python3.8 -m pip install git+https://github.com/Zeecka/pytube@fix_1060#egg=pytube
# this version fixes 'HTTP Error 410: Gone' (3.8.2021)

import os
import sys
import re
from pytube import YouTube
from pytube.exceptions import RegexMatchError


destination_path = "/home/marvin/Musik"


def doDownload(url):
  try:
    print("Retrieving video...")

    yt = YouTube(url)
    audio = yt.streams.get_audio_only()
    # printInfo(yt)

    print("Downloading...")

    # download the audio and temporarily save in 'curr'
    title = cleanTitle(yt)
    curr = audio.download(filename=title)

    # move file to destination path
    destination = os.path.join(destination_path, title)
    os.replace(curr, destination)

    # print finishing info with title
    print("Download of '{}' completed.\n".format(title))

  # handle some exceptions
  except FileNotFoundError as e:
    print("FileNotFoundError: {}".format(e))
    sys.exit()
  except RegexMatchError as e:
    print(f"'{url}' is not a valid url. Exiting...")
    sys.exit()
  except Exception as e:
    print("Error: {}".format(e))
    sys.exit()


def cleanTitle(yt):
  title = yt.title.replace("'", "")  # remove apostroph (breaks renaming)
  title = re.sub(r"[\(\[].*?[\)\]]", "", title)  # remove (...) and [...]
  title = title.rstrip()  # remove trailing white spaces
  title = title.title()  # capitalize only first letter
  title += ".mp3"
  return title


def printInfo(yt):
  print("Title: ", yt.title)
  print("Number of views: ", yt.views)
  print("Length of video: ", yt.length, "seconds")
  print("Description: ", yt.description)
  print("Ratings: ", yt.rating)


def main():
  # get urls for download from "urls.txt"
  dir_path = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(dir_path, "urls.txt")

  # open file, read lines and close
  f = open(file_path, "r")
  for line in f.readlines():
    if not line.startswith("#") and not line.startswith("!"):
      url = line.rstrip()
      doDownload(url)
  f.close()

  print("Exiting...")


if __name__ == "__main__":
  main()
