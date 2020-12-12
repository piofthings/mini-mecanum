#!/usr/bin/env python3
import picamera
import time
from timeit import default_timer as timer

def write_pgm(filename, w, h, data):
    with open(filename, 'wb') as f:
        f.write("P5\n{:d} {:d}\n255\n".format(w, h).encode('utf8'))
        f.write(data)

def process_bytearray(data, w, h, stretch=True, thresh=True):
    if stretch:
        y = 0
        while y < h:
            row = memoryview(data)[y*w:(y+1)*w]
            minval = 255
            maxval = 0

            for val in row:
                if val < minval:
                    minval = val
                if val > maxval:
                    maxval = val

            diff = maxval - minval

            factor = 1
            if diff != 0:
                factor = 255/diff

            x = 0
            for val in row:
                val = int((val - minval) * factor)
                if thresh:
                    if val > 128:
                        val = 255
                    else:
                        val = 0
                    row[x] = val
                else:
                    row[x] = val
                x = x + 1
            y = y + 1

    # Note that this could be combined into the stretch step above (just
    # threshold before assigning the stretched value back) to save a full
    # iteration of the image if really necessary
    #if thresh:
        # y = 0
        # while y < h:
        #     row = memoryview(data)[y*w:(y+1)*w]
        #     x = 0
        #     for val in row:
        #         if val > 128:
        #             val = 255
        #         else:
        #             val = 0
        #         row[x] = val
        #         x = x + 1
        #     y = y + 1

w = 32
h = 32
save = False
stretch = True
threshold = True
with picamera.PiCamera(resolution='{:d}x{:d}'.format(w, h), framerate=30) as camera:
    data = bytearray(b'\0' * (w * (h*2)))

    camera.start_preview()
    # Wait for 3A to settle
    time.sleep(3)
    start = timer()
    prev = start
    i = 0
    for foo in camera.capture_continuous(data, 'yuv', use_video_port=True):
        i = i + 1

        if save:
            # Save original
            write_pgm("captures/out_{:d}.pgm".format(i), w, h, data)

        proc_start = timer()
        process_bytearray(data, w, h, stretch=stretch, thresh=threshold)
        proc_time = timer() - proc_start

        if save:
            # Save result
            write_pgm("captures/out_proc_{:d}.pgm".format(i), w, h, data)

        now = timer()
        t = now - prev
        #print("Frame time: {}, processing took: {}".format(t, proc_time))
        prev = now

        if now - start > 3:
            print("{:d} frames in {}, {} fps".format(i, now - start, i / (now - start)))
            camera.stop_preview()
            exit(0)