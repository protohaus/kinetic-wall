import grp
import os
import pwd
import time

import keyboard

HISTORY = {}
RUN_LOOP = True
A_PRESSED = False


def key_recording(e):
    global A_PRESSED
    if e.name == "a":
        if e.event_type == keyboard.KEY_DOWN:
            A_PRESSED = True
        else:
            A_PRESSED = False


if __name__ == "__main__":
    path = "keys.txt"
    with open("keys.txt", "w") as file:
        remove = keyboard.hook(key_recording)
        try:
            print("Press ctrl+c key to exit")
            while RUN_LOOP:
                if A_PRESSED:
                    file.write(" 1")
                else:
                    file.write(" 0")
                time.sleep(0.02)
        except KeyboardInterrupt:
            pass
        finally:
            uid = pwd.getpwnam("moritz").pw_uid
            gid = grp.getgrnam("moritz").gr_gid
            os.chown(path, uid, gid)

