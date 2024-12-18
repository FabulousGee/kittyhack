import os
import threading
import time as tm
import logging
import random
from src.system import Gpio

# GPIO pin numbers and directions
OUTSIDE_PIR_GPIO_NUM = 536
OUTSIDE_PIR_GPIO_DIR = "in"
INSIDE_PIR_GPIO_NUM = 535
INSIDE_PIR_GPIO_DIR = "in"
OUTSIDE_POWER_GPIO_NUM = 517
OUTSIDE_POWER_GPIO_DIR = "out"
INSIDE_POWER_GPIO_NUM = 516
INSIDE_POWER_GPIO_DIR = "out"

# Create a Gpio instance
gpio = Gpio()

class Pir:
    def __init__(self, simulate_kittyflap=False):
        self.state_outside = 0  # 0 = no motion, 1 = motion detected
        self.state_inside = 0   # 0 = no motion, 1 = motion detected
        self.thread_lock = threading.Lock()
        self.simulate_kittyflap = simulate_kittyflap

    def init(self):
        """Enable both PIRs."""
        if self.simulate_kittyflap:
            logging.info("[PIR] Simulation mode enabled. PIRs are not powered on.")
        else:
            try:
                # Configure GPIO pins for PIRs
                gpio.configure(OUTSIDE_POWER_GPIO_NUM, OUTSIDE_POWER_GPIO_DIR)
                gpio.configure(INSIDE_POWER_GPIO_NUM, INSIDE_POWER_GPIO_DIR)
                gpio.configure(OUTSIDE_PIR_GPIO_NUM, OUTSIDE_PIR_GPIO_DIR)
                gpio.configure(INSIDE_PIR_GPIO_NUM, INSIDE_PIR_GPIO_DIR)

                # Power on the PIRs
                gpio.set(OUTSIDE_POWER_GPIO_NUM, 1)
                gpio.set(INSIDE_POWER_GPIO_NUM, 1)
            except Exception as e:
                logging.error(f"[PIR] Error initializing PIRs: {e}")
            else:
                logging.info("[PIR] PIRs initialized and powered on.")

    def read(self):
        """Continuously read the state of both PIRs and update shared states."""
        while True:
            try:
                if self.simulate_kittyflap:
                    # Simulate motion detection with 5% chance and keep the state active for 5-10 seconds
                    if self.state_outside == 0 and random.random() < 0.05:
                        state_outside = 1
                        threading.Timer(random.uniform(5, 10), lambda: self.update_state("OUTSIDE", 0)).start()
                    else:
                        state_outside = self.state_outside

                    if self.state_inside == 0 and random.random() < 0.05:
                        state_inside = 1
                        threading.Timer(random.uniform(5, 10), lambda: self.update_state("INSIDE", 0)).start()
                    else:
                        state_inside = self.state_inside
                else:
                    # No simulation, read actual PIR states
                    try:
                        state_outside = 1 - gpio.get(OUTSIDE_PIR_GPIO_NUM) # 0 -> motion, 1 -> no motion
                        state_inside = 1 - gpio.get(INSIDE_PIR_GPIO_NUM)   # 0 -> motion, 1 -> no motion
                    except:
                        # Ignore errors. Error logging is done in gpio.get()
                        pass

                # Log only changes in state
                if self.state_outside != state_outside:
                    if state_outside == 1:
                        logging.info(f"[PIR] OUTSIDE: Motion detected")
                    else:
                        logging.info(f"[PIR] OUTSIDE: No motion")

                if self.state_inside != state_inside:
                    if state_inside == 1:
                        logging.info(f"[PIR] INSIDE: Motion detected")
                    else:
                        logging.info(f"[PIR] INSIDE: No motion")

                with self.thread_lock:
                    self.state_outside = state_outside
                    self.state_inside = state_inside

            except Exception as e:
                logging.error(f"[PIR] Error reading PIR states: {e}")

            tm.sleep(0.2)

    def update_state(self, pir, state):
        """
        Thread-safe method to update the state of a PIR sensor.

        Args:
            pir (str): The identifier of the PIR sensor. Expected values are "OUTSIDE" or "INSIDE".
            state (bool): The new state of the PIR sensor. Typically True for active/motion detected, False for inactive/no motion.
        """
        with self.thread_lock:
            if pir == "OUTSIDE":
                self.state_outside = state
            elif pir == "INSIDE":
                self.state_inside = state

    def get_states(self):
        """
        Thread-safe method to read the current states of the PIRs.

        Returns:
            tuple: A tuple containing: state_outside, state_inside
                   (0 = no motion, 1 = motion detected)
        """
        with self.thread_lock:
            return self.state_outside, self.state_inside
