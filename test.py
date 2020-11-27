import time
import traceback
from decimal import Decimal

from Phidget22.Devices.DigitalOutput import *
from Phidget22.Phidget import *
from Phidget22.PhidgetException import *

# Declare any event handlers here. These will be called every time the associated event occurs.


def onAttach(self):
    print("Attach [" + str(self.getChannel()) + "]!")


def onDetach(self):
    print("Detach [" + str(self.getChannel()) + "]!")


def onError(self, code, description):
    print("Code [" + str(self.getChannel()) + "]: " + ErrorEventCode.getName(code))
    print("Description [" + str(self.getChannel()) + "]: " + str(description))
    print("----------")


def main():
    try:
        # Create your Phidget channels
        digitalOutput0 = DigitalOutput()
        digitalOutput1 = DigitalOutput()
        digitalOutput2 = DigitalOutput()
        digitalOutput3 = DigitalOutput()

        # Set addressing parameters to specify which channel to open (if any)
        digitalOutput0.setChannel(0)
        digitalOutput1.setChannel(1)
        digitalOutput2.setChannel(2)
        digitalOutput3.setChannel(3)

        # Assign any event handlers you need before calling open so that no events are missed.
        digitalOutput0.setOnAttachHandler(onAttach)
        digitalOutput0.setOnDetachHandler(onDetach)
        digitalOutput0.setOnErrorHandler(onError)
        digitalOutput1.setOnAttachHandler(onAttach)
        digitalOutput1.setOnDetachHandler(onDetach)
        digitalOutput1.setOnErrorHandler(onError)
        digitalOutput2.setOnAttachHandler(onAttach)
        digitalOutput2.setOnDetachHandler(onDetach)
        digitalOutput2.setOnErrorHandler(onError)
        digitalOutput3.setOnAttachHandler(onAttach)
        digitalOutput3.setOnDetachHandler(onDetach)
        digitalOutput3.setOnErrorHandler(onError)

        # Open your Phidgets and wait for attachment
        digitalOutput0.openWaitForAttachment(5000)
        digitalOutput1.openWaitForAttachment(5000)
        digitalOutput2.openWaitForAttachment(5000)
        digitalOutput3.openWaitForAttachment(5000)

        # Do stuff with your Phidgets here or in your event handlers.
        digitalOutput0.setDutyCycle(1)
        digitalOutput1.setDutyCycle(1)
        digitalOutput2.setDutyCycle(1)
        digitalOutput3.setDutyCycle(1)

        with open("keys.txt", "r") as timing_file:
            try:
                state_str = timing_file.read(2)
                last_state = False
                elapsed_time = Decimal("0.00")
                while state_str:
                    state = bool(int(state_str[-1:]))
                    if state != last_state:
                        if state:
                            digitalOutput0.setDutyCycle(1)
                            digitalOutput1.setDutyCycle(1)
                            digitalOutput2.setDutyCycle(1)
                            digitalOutput3.setDutyCycle(1)
                        else:
                            digitalOutput0.setDutyCycle(0)
                            digitalOutput1.setDutyCycle(0)
                            digitalOutput2.setDutyCycle(0)
                            digitalOutput3.setDutyCycle(0)
                    print("                        ", end="\r")
                    print(f"State: {state}\tTime: {elapsed_time}", end="\r")
                    time.sleep(0.02)
                    elapsed_time += Decimal("0.02")
                    state_str = timing_file.read(2)
                    last_state = state
            except (Exception, KeyboardInterrupt):
                pass

        # Close your Phidgets once the program is done.
        digitalOutput0.close()
        digitalOutput1.close()
        digitalOutput2.close()
        digitalOutput3.close()

    except PhidgetException as ex:
        # We will catch Phidget Exceptions here, and print the error informaiton.
        traceback.print_exc()
        print("")
        print(
            "PhidgetException "
            + str(ex.code)
            + " ("
            + ex.description
            + "): "
            + ex.details
        )


main()
