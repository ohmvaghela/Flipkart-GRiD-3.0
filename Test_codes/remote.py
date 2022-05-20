from pynput.keyboard import Key, Listener
import time
import serial



class teleop:
    def __init__(self):
        self.rot_speed = 5
        self.fw_speed = 5
        self.my_communicator = serial.Serial('COM6', 9600)
        self.botID = "11"

    def update_speed(self,key):
        try:
            if key.char == 'i':
                self.fw_speed += 1
                print("increased forward speed")

            elif key.char == 'k':
                self.fw_speed -= 1
                print("decreased forward speed")

            elif key.char == 'l':
                self.rot_speed += 1
                print("increased rot speed")

            elif key.char == 'j':
                self.rot_speed -= 1
                print("decreadsed rot speed to")
            else:
                print(f"Pressed Invalid key for update speed:{key.char}")
            
            if self.rot_speed > 31:
                self.rot_speed = 31
            if self.fw_speed > 31:
                self.fw_speed = 31
            if self.rot_speed < 0:
                self.rot_speed = 0
            if self.fw_speed < 0:
                self.fw_speed = 0
            print(f"rotational_speed is:{self.fw_speed}, forward speed is:{self.rot_speed}")

        except:
            print("exception in update speed")
            return False

    def on_press(self,key):
        # passer = self.my_communicator.readline()
        # print(f"passer string is{passer}")
        self.command_string = ""
        self.update_command(key)
        self.update_speed(key)
        self.pack_commands()
        self.send_msg()
        incomming = self.my_communicator.readline()
        print(f"Incomming string is:{bytes(incomming,'utf-8')}")
        self.my_communicator.flush()

    def update_command(self,key):
        print('{0} pressed'.format(
            key))
        if key == Key.esc:
            return
        self.command_string = '111110'
        if key.char == 's':
            self.command_string = '000'
            print('stop')
        elif key.char == 'a':
            self.command_string = '111'
            print('anticlock wise')

        elif key.char == 'd':
            self.command_string = '101'
            print('clockwise')

        elif key.char == 'w':
            self.command_string = '100'
            # self.command_string = '111010'
            print('forward')

        elif key.char == 'x':
            self.command_string = '001'    
            print('dumping')

        else:
            print(f"Command didnt update, character found is:{key.char}")


        self.command_string = self.command_string + str(0)



    def pack_commands(self):
        binary_string = self.botID + self.command_string + bin(self.fw_speed)[2:] + bin(self.rot_speed)[2:]
        self.msg = int(binary_string, 2)

        #
        # rot_speed_string = "{0:0>5}".format(self.rot_speed)
        # fw_speed_string = "{0:0>5}".format(self.fw_speed)
        # self.msg = self.command_string + fw_speed_string + rot_speed_string
        # self.msg = bytes(self.msg,'utf-8')
        print(f"generated command is :{self.msg}")

    def on_release(self,key):
        print('{0} release'.format(
            key))
        # self.command_string = '111100'+str(0)     s
        self.msg = int(self.botID + "0000000000000",2)     
        print('command ended')
        # msg = bytes(command_string,'utf-8')
        # my_communicator.write(msg)
        if key == Key.esc:
            # Stop listener
            return False

    def send_msg(self):
        self.my_communicator.write(self.msg)

# Collect events until released
my_teleop = teleop()

with Listener(
        on_press=my_teleop.on_press,
        on_release=my_teleop.on_release,
        ) as listener:
    listener.join()


