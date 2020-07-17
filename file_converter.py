import subprocess
import requests
import json
import os
from ricecooker.utils.html import download_file


#m4v video download and conversions
DOWNLOADED_M4V_FILES_DIR = os.path.join("chefdata", "downloadedm4vs")
print(DOWNLOADED_M4V_FILES_DIR, 'DOWNLOADED_M4V_FILES_DIR')
if not os.path.exists(DOWNLOADED_M4V_FILES_DIR):
    os.makedirs(DOWNLOADED_M4V_FILES_DIR, exist_ok=True)
    print("m4v path created")

CONVERTED_MP4_FILES_DIR = os.path.join("chefdata", "convertedmp4s")
print(CONVERTED_MP4_FILES_DIR, 'CONVERTED_MP4_FILES_DIR')
if not os.path.exists(CONVERTED_MP4_FILES_DIR):
    os.makedirs(CONVERTED_MP4_FILES_DIR, exist_ok=True)
    print("mp4 path created")


#mpeg files download
DOWNLOADED_MPEG_FILES_DIR = os.path.join("chefdata", "downloadedmpeg")
print(DOWNLOADED_MPEG_FILES_DIR, 'DOWNLOADED_MPEG_FILES_DIR')
if not os.path.exists(DOWNLOADED_MPEG_FILES_DIR):
    os.makedirs(DOWNLOADED_MPEG_FILES_DIR, exist_ok=True)
    print("mpeg path created")

# Wav files download
DOWNLOADED_WAV_FILES_DIR = os.path.join("chefdata", "downloadedwavs")
print(DOWNLOADED_WAV_FILES_DIR, 'DOWNLOADED_WAV_FILES_DIR')
if not os.path.exists(DOWNLOADED_WAV_FILES_DIR):
    os.makedirs(DOWNLOADED_WAV_FILES_DIR, exist_ok=True)
    print("wav path created")

CONVERTED_MP3_FILES_DIR = os.path.join("chefdata", "convertedmp3s")
print(CONVERTED_MP3_FILES_DIR, 'CONVERTED_MP3_FILES_DIR')
if not os.path.exists(CONVERTED_MP3_FILES_DIR):
    os.makedirs(CONVERTED_MP3_FILES_DIR, exist_ok=True)
    print("mp3 path created")


# downloading and converting video files
def download_and_convert_m4v_file(m4v_url):
    """
    Kolibri VideoNode only support .mp4 files and not .m4v, so we must convert.
    """
    m4v_filename = m4v_url.split('/')[-1]  # e.g. something.wav
    m4v_path = os.path.join(DOWNLOADED_M4V_FILES_DIR, m4v_filename)
    print(m4v_path, 'm4v_path')

    # 1. DOWNLOAD M4V file
    download_file(m4v_url, DOWNLOADED_M4V_FILES_DIR)
    print("m4v downloaded")

    # 2. CONVERT
    mp4_filename = m4v_filename.replace('.m4v', '.mp4')
    mp4_path = os.path.join(CONVERTED_MP4_FILES_DIR, mp4_filename)
    print(mp4_filename, mp4_path)
    if not os.path.exists(mp4_path):
        try:
            command = ["ffmpeg", "-i", m4v_path, "-vcodec", "copy", "-acodec", "copy", mp4_path]
            subprocess.check_call(command)
            print("Successfully converted m4v file to mp4")
        except subprocess.CalledProcessError:
            print("Problem converting " + m4v_url)
            return None

    # Return path of converted mp4 file
    return mp4_path

def download_and_convert_png_file(png_url):
    """
    Kolibri VideoNode only support .mp4 files and not .m4v, so we must convert.
    """
    m4v_filename = png_url.split('/')[-1]  # e.g. something.wav
    m4v_path = os.path.join(DOWNLOADED_M4V_FILES_DIR, m4v_filename)
    print(m4v_path, 'm4v_path')

    # 1. DOWNLOAD M4V file
    download_file(png_url, DOWNLOADED_M4V_FILES_DIR)
    print("m4v downloaded")

    # 2. CONVERT
    mp4_filename = m4v_filename.replace('.png', '.mp4')
    mp4_path = os.path.join(CONVERTED_MP4_FILES_DIR, mp4_filename)
    print(mp4_filename, mp4_path)
    if not os.path.exists(mp4_path):
        try:
            command = ["ffmpeg", "-i", m4v_path, "-vcodec", "copy", "-acodec", "copy", mp4_path]
            subprocess.check_call(command)
            print("Successfully converted m4v file to mp4")
        except subprocess.CalledProcessError:
            print("Problem converting " + png_url)
            return None

    # Return path of converted mp4 file
    return mp4_path


def download_and_convert_wav_file(wav_url):
    """
    Kolibri AudioNode only support .mp3 files and not .wav, so we must convert.
    """
    wav_filename = wav_url.split('/')[-1]  # e.g. something.wav
    wav_path = os.path.join(DOWNLOADED_WAV_FILES_DIR, wav_filename)
    print("done3")

    # 1. DOWNLOAD
    download_file(wav_url, DOWNLOADED_WAV_FILES_DIR)
    print("don4")

    # 2. CONVERT
    mp3_filename = wav_filename.replace('.wav', '.mp3')
    mp3_path = os.path.join(CONVERTED_MP3_FILES_DIR, mp3_filename)
    print(mp3_filename, mp3_path)
    if not os.path.exists(mp3_path):
        try:
            command = ["ffmpeg", "-i", wav_path, "-acodec", "mp3", "-ac", "2",
                       "-ab", "64k", "-y", "-hide_banner", "-loglevel", "warning", mp3_path]
            subprocess.check_call(command)
            print("Successfully converted wav file to mp3")
        except subprocess.CalledProcessError:
            print("Problem converting " + wav_url)
            return None

    # Return path of converted mp3 file
    return mp3_path



def download_and_convert_mpeg_file(mpeg_url):
    """
    Kolibri AudioNode only support .mp3 files and not .mpeg, so we must convert.
    """
    mpeg_filename = mpeg_url.split('/')[-1]  # e.g. something.wav
    mpeg_path = os.path.join(DOWNLOADED_MPEG_FILES_DIR, mpeg_filename)
    print(mpeg_path, 'mpeg_path')

    # 1. DOWNLOAD
    download_file(mpeg_url, DOWNLOADED_MPEG_FILES_DIR)
    print("mpeg downloaded")

    # 2. CONVERT
    mp3_filename = mpeg_filename.replace('.mpeg', '.mp3')
    mp3_path = os.path.join(CONVERTED_MP3_FILES_DIR, mp3_filename)
    print(mp3_filename, mp3_path)
    if not os.path.exists(mp3_path):
        try:
            command = ["ffmpeg", "-i", mpeg_path, "-acodec", "mp3", "-ac", "2",
                       "-ab", "64k", "-y", "-hide_banner", "-loglevel", "warning", mp3_path]
            subprocess.check_call(command)
            print("Successfully converted mpeg file to mp3")
        except subprocess.CalledProcessError:
            print("Problem converting " + mpeg_url)
            return None

    # Return path of converted mp3 file
    return mp3_path
