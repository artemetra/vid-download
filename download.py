import requests
import os
import subprocess
import sys

domain = 'https://cfvod.kaltura.com/hls/p/1674401/sp/167440100/serveFlavor/entryId/1_fmyw2q7s/v/1/ev/4/flavorId/1_0dvpd0pe/name/a.mp4/'
# segment format: seg-{num}-v1-a1.ts
dir = "D:\\test\\vid-download\\results\\"

def download_directly() -> None:
    i = 1
    while True:
        result = requests.get(domain + f"seg-{i}-v1-a1.ts")
        if result.ok:
            with open(dir + f"seg-{i}.ts", 'wb') as f:
                f.write(result.content)
            print(f"Video seg-{i}.ts downloaded successfully! Size: {len(result.content)/1000} KB")
            i += 1
        else:
            print(f"FAIL: Response returned {result.status_code} at index {i}, exiting.")
            break

def ffmpeg_download() -> None:
    i = 1
    queue = dir + "queue.txt"
    if os.path.exists(queue): os.remove(queue)
    while True:
        result = requests.get(domain + f"seg-{i}-v1-a1.ts")
        if result.ok:
            with open(queue, 'a') as f:
                f.write(f"file '{result.url}'\n")
            i += 1
        else:
            break
    
    # ffmpegres = subprocess.run(f'ffmpeg -f concat -safe 0 -i queue.txt copy output.mp4', 
    #                 shell = True,
    #                 stdout=subprocess.PIPE,
    #                 stderr=subprocess.PIPE)
    os.system(f'ffmpeg -f concat -safe 0 \
                -protocol_whitelist file,http,https,tcp,tls,crypto \
                -i queue.txt \
                output.mp4')


if __name__ == '__main__':
    os.chdir(dir)
    ffmpeg_download()