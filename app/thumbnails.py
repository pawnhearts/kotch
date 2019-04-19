import asyncio
import json
import os.path

from .settings import Settings

settings = Settings()


def get_extension(path):
    return os.path.splitext(path)[1].lstrip('.').lower()


def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]


async def ffprobe(path):
    proc = await asyncio.create_subprocess_exec(
        'ffprobe', '-print_format', 'json', '-show_format', '-show_streams', path,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    if not await proc.wait():
        raise Exception("Corrupt video file")
    stdout = await proc.stdout.read()
    return json.loads(stdout.decode('utf-8'))


async def get_video_size(path):
    streams = await ffprobe(path)
    try:
        x = streams['format']['duration'].split('.')
        x[-1] = x[-1][:2]
        if int(x[0]) <= 59:
            duration = ('.').join(x) + 's'
        else:
            m, s = divmod(int(x[0]), 60)
            duration = '{0}:{1}'.format(m, s)
    except KeyError:
        duration = None
    for stream in streams['streams']:
        if stream['codec_name'] in settings.video_codecs:
            return stream['width'], stream['height'], duration
    raise Exception("Corrupt video file")


async def get_image_size(path):
    proc = await asyncio.create_subprocess_exec(
        'identify', '-format', '%m,%w,%h ', path,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    if not await proc.wait():
        raise Exception("Corrupt video file")
    format, width, height = await proc.stdout.read().decode('utf-8').split(' ')[0].split(',')
    width, height = int(width), int(height)
    if format not in settings.image_codecs:
        raise Exception('Corrupt image file')
    return width, height


async def make_thumbnail(path):
    duration = None
    ex = 'jpg'
    if path.split('.')[-1].lower() == 'png':
        ex = 'png'
    tname = "files/{0}_.{1}".format(get_basename(path), ex)
    if get_extension(path) in settings.image_extensions:
        width, height = await get_image_size(path)
        if width > 6000 or height > 6000:
            raise Exception("Image too large")
        scale = min(float(settings.thumbnail_size[0]) / width, float(settings.thumbnail_size[1]) / height, 1.0)
        twidth = int(scale * width)
        theight = int(scale * height)
        tsize = '%sx%s!' % (twidth, theight)
        proc = await asyncio.create_subprocess_exec(
            'convert', path + '[0]', '-thumbnail', tsize, '-strip', tname,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        if not await proc.wait():
            raise Exception("Corrupt image file")
        return tname, width, height, duration
    elif get_extension(path) in settings.video_extensions:
        width, height, duration = await get_video_size(path)
        scale = min(float(settings.thumbnail_size[0]) / width, float(settings.thumbnail_size[1]) / height, 1.0)
        twidth = int(scale * width)
        theight = int(scale * height)
        tsize = '%sx%s' % (twidth, theight)
        proc = await asyncio.create_subprocess_exec(
            'ffmpeg', '-i', path, '-y', '-s', tsize, '-vframes', '1', '-f', 'image2', '-c:v', 'mjpeg', tname,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        if not await proc.wait():
            raise Exception("Corrupt video file")
        return tname, width, height, duration
    elif get_extension(path) in settings.audio_extensions:
        return '', 0, 0, None
    else:
        raise Exception("Format not supported")

