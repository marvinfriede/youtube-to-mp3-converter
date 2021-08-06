#!/bin/env python3

# SIMPLE YOUTUBE MP3 DOWNLOADER USING PYTUBE
#
# 
# install pytube with: python -m pip install git+https://github.com/pytube/pytube

import os
import shutil
import sys
import re
import argparse

try:
  from pytube import YouTube
  from pytube.exceptions import RegexMatchError
except ModuleNotFoundError as e:
  print("The module 'pytube' was not found. Install via python -m pip install git+https://github.com/pytube/pytube")
  sys.exit()



destination = "~/Musik"

# argparser
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-v", "--verbose",
                    help="Print information of YouTube stream.", action="store_true")
parser.add_argument(
    "-h", "--help", help="How to use.", action="help")
flags = parser.parse_args()


class InvalidUrlError(Exception):
  """Raised when url is not a valid youtube url."""
  pass


def cleanDestinationPath(path):
  if path.startswith("~"):
    path = path.replace("~", os.path.expanduser("~"))
  return path

def cleanTitle(yt):
  title = yt.title.replace("'", "")  # remove apostroph (breaks renaming)
  title = re.sub(r"[\(\[].*?[\)\]]", "", title)  # remove (...) and [...]
  title = title.rstrip()  # remove trailing white spaces
  title = title.title()  # capitalize only first letter
  title += ".mp3"
  return title


def printInfo(yt):
  print("\nTitle: ", yt.title)
  print("Number of views: ", yt.views)
  print("Length of video: ", yt.length, "seconds")
  print("Ratings: ", yt.rating)
  print("Description: {}\n".format(yt.description.replace("\n","|")))


def main():
  global destination, flags

  # get urls for download from "urls.txt"
  dir_path = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(dir_path, "urls.txt")


  f = open(file_path, "r")
  for line in f.readlines():
    if not line.startswith("#") and not line.startswith("!"):
      
      # download
      try:
        url = line.rstrip()
        if not url.startswith("https://www.youtube"): raise InvalidUrlError

        # get stream from YouTube
        print("Retrieving video...")
        yt = YouTube(url)
        audio = yt.streams.get_audio_only()
        
        # print info
        if flags.verbose: printInfo(yt)

        print("Downloading...")

        # setup title and destination path
        title = cleanTitle(yt)
        destination = cleanDestinationPath(destination)

        # download
        audio.download(output_path=destination, filename=title)
        
        # print finishing info with title
        print("Download of '{}' completed.\n".format(title))

      # handle some exceptions
      except FileNotFoundError as e:
        print("FileNotFoundError: {}".format(e))
        sys.exit()

      # invalid urls
      except InvalidUrlError:
        print(f"'{url}' is not a valid url. Skipping...\n")
        continue
      except RegexMatchError:
        print(f"'{url}' is not a valid url. Skipping...\n")
        continue

      # raised if folder with same name as mp3 file in destination folder
      except IsADirectoryError:
        deletePath = os.path.join(destination, title)
        print("Error: Folder with same name detected ({})".format(deletePath))

        doRemove = input("Delete and try again? ")
        if doRemove == "y" or doRemove == "yes" or doRemove == "j":
          shutil.rmtree(deletePath, ignore_errors=True)
          audio.download(output_path=destination, filename=title)
          print("Download of '{}' completed.\n".format(title))
        continue

  # clean up
  f.close()
  print("Exiting...")


if __name__ == "__main__":
  main()
