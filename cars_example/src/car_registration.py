#!/usr/bin/env python3
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. It is provided for educational
# purposes and is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import collections
import pickle
import socket
import struct
import sys
import Console


Address = ["localhost", 9653]


CarTuple = collections.namedtuple("CarTuple", "seats mileage owner")


class SocketManager:

    def __init__(self, address):
        self.address = address


    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        return self.sock


    def __exit__(self, *ignore):
        self.sock.close()
        


def main():
    if len(sys.argv) > 1:
        Address[0] = sys.argv[1]
    call = dict(c=get_car_details, l=get_license_list, m=change_mileage, o=change_owner,
                n=new_registration, s=stop_server, q=quit)
    menu = ("(C)ar List (L)icenses Edit (M)ileage  Edit (O)wner  (N)ew car  "
            "(S)top server  (Q)uit")
    valid = frozenset("clmonsq")
    previous_myLicense = None
    while True:
        action = Console.get_menu_choice(menu, valid, "c", True)
        previous_myLicense = call[action](previous_myLicense)

def get_license_list(*ignore):
    ok, data = handle_request("GET_LICENSE_LIST")
    for i, mylicense in enumerate(data):
        print "--{0}--\t".format(mylicense),
        if (i+1)%5 == 0:
            print "\n"
    print "\n"


def retrieve_car_details(previous_myLicense):
    myLicense = Console.get_string("License", "license",
                                 previous_myLicense) 
    if not myLicense:
        return previous_myLicense, None
    myLicense = myLicense.upper()
    # quito un *data y ponto data = 
    ok, data = handle_request("GET_CAR_DETAILS", myLicense)
    if not ok:
        print(data[0])
        return previous_myLicense, None
    return myLicense, CarTuple(*data)


def get_car_details(previous_myLicense):
    myLicense, car = retrieve_car_details(previous_myLicense)
    if car is not None:
        print("License: {0}\nSeats:   {1[0]}\nMileage: {1[1]}\n"
              "Owner:   {1[2]}".format(myLicense, car))
    return myLicense


def change_mileage(previous_myLicense):
    myLicense, car = retrieve_car_details(previous_myLicense)
    if car is None:
        return previous_myLicense
    mileage = Console.get_integer("Mileage", "mileage",
                                  car.mileage, 0)
    if mileage == 0:
        return myLicense
    # quito un *data y ponto data = 
    ok, data = handle_request("CHANGE_MILEAGE", myLicense, mileage)
    if not ok:
        print(data[0])
    else:
        print("Mileage successfully changed")
    return myLicense


def change_owner(previous_myLicense):
    myLicense, car = retrieve_car_details(previous_myLicense)
    if car is None:
        return previous_myLicense
    owner = Console.get_string("Owner", "owner", car.owner)
    if not owner:
        return myLicense
    # quito un *data y ponto data = 
    ok, data = handle_request("CHANGE_OWNER", myLicense, owner)
    if not ok:
        print(data[0])
    else:
        print("Owner successfully changed")
    return myLicense


def new_registration(previous_myLicense):
    myLicense = Console.get_string("License", "license") 
    if not myLicense:
        return previous_myLicense
    myLicense = myLicense.upper()
    seats = Console.get_integer("Seats", "seats", 4, 0)
    #if not (1 < seats < 10):
    #    return previous_myLicense
    mileage = Console.get_integer("Mileage", "mileage", 0, 0)
    owner = Console.get_string("Owner", "owner")
    #if not owner:
    #    return previous_myLicense
    # quito un *data y ponto data = 
    ok, data = handle_request("NEW_REGISTRATION", myLicense, seats,
                               mileage, owner)
    if not ok:
        print(data[0])
    else:
        print("Car {0} successfully registered".format(myLicense))
    return myLicense


def quit(*ignore):
    sys.exit()


def stop_server(*ignore):
    handle_request("SHUTDOWN", wait_for_reply=False)
    sys.exit()


def handle_request( *items, **kwargs):
    wait_for_reply=kwargs.pop('wait_for_reply', True)
    SizeStruct = struct.Struct("!I")
    data = pickle.dumps(items, 0)
    
    try:
        with SocketManager(tuple(Address)) as sock:
            sock.sendall(SizeStruct.pack(len(data)))
            sock.sendall(data)
            if not wait_for_reply:
                return

            size_data = sock.recv(SizeStruct.size)
            size = SizeStruct.unpack(size_data)[0]
            result = bytearray()
            while True:
                data = sock.recv(4000)
                if not data:
                    break
                result.extend(data)
                if len(result) >= size:
                    break
        return pickle.loads(result)
    except socket.error as err:
        print("{0}: is the server running?".format(err))
        sys.exit(1)


main()
