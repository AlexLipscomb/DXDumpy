import rtmidi

class DXHelper:
    def get_available_midi_ports(self):
        midiin = rtmidi.MidiIn()
        available_ports = midiin.get_ports()

        port_names = []

        for i in range(len(available_ports)):
            port_names.append(available_ports[i])
            print(f'{i}: \'{available_ports[i]}\'')

        return port_names

    def dump(self, args):
        midiin = rtmidi.MidiIn()
        available_ports = midiin.get_ports()

        target_port = args[0]
        target_file = args[1]

        try:
            target_port = int(target_port)
            if target_port > len(available_ports) - 1 or target_port < 0:
                print("Port is out of range. Available ports:")
                self.get_available_midi_ports()
                return
            
        except ValueError:
            port_found = False
            for i in range(len(available_ports)):
                if available_ports[i] == target_port:
                    target_port = i
                    port_found = True
                    break

            if not port_found:
                print("Port not found.")
                self.get_available_midi_ports()
                return

        midiin.open_port(target_port)
        midiin.ignore_types(sysex=False)
        print(f"Listening on {target_port}: {available_ports[target_port]}")

        while True:
            # Only received when MIDI SYS INFO is ON
            self._request_dump(target_port)

            msg = midiin.get_message()

            if msg and self._is_sysex(msg[0]):
                if not self._is_yamaha(msg[0]):
                    print("Connected synth is not made by Yamaha. Quitting...")
                    midiin.close_port()
                    break

                if self._save_syx_file(target_file, msg[0]):
                    print(f"Dumped successfully to {target_file}.syx")
                else:
                    print("Something went wrong.")

                midiin.close_port()
                break


    def export(self, args):
        midiout = rtmidi.MidiOut()
        available_ports = midiout.get_ports()

        target_port = args[0]
        target_file = args[1]


        try:
            target_port = int(target_port)
            if target_port > len(available_ports) - 1 or target_port < 0:
                print("Port is out of range. Available ports:")
                self.get_available_midi_ports()
                return
            
        except ValueError:
            port_found = False
            for i in range(len(available_ports)):
                if available_ports[i] == target_port:
                    target_port = i
                    port_found = True
                    break

            if not port_found:
                print("Port not found.")
                self.get_available_midi_ports()
                return

        loadedSysXData = self._load_syx_file(target_file)

        if loadedSysXData is None:
            print("Couldn't load sysex data")
            return

        if not self._is_sysex(loadedSysXData):
            print("Loaded data isn't sysex. Quitting...")
            return
        
        try:
            midiout.open_port(target_port)
            midiout.send_message(loadedSysXData)
            print("Successfully exported sysex")
        except:
            print("Something went wrong.")
            return

    def _load_syx_file(self, path: str):
        try:
            with open(path, 'rb') as sysXFile:
                return list(sysXFile.read())
        except:
            return None

    def _save_syx_file(self, path:str, contents):
        try: 
            with open(f'{str(path)}.syx', 'wb') as sysXFile:
                sysXFile.write(bytes(contents))
                return True
        except:
            return False

    def _is_yamaha(self, data):
        if data[1] == 0x43:
            return True
        return False

    def _is_sysex(self, data):
        if data[0] == 0xF0 and data[-1] == 0xF7:
            return True
        return False

    def _request_dump(self, port):
        midiout = rtmidi.MidiOut()
        midiout.open_port(port)

        midiout.send_message([
            0xF0,
            0x43,
            0x20, 
            0x4,
            0xF7
        ])
        midiout.close_port()