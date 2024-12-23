import zipfile
import configparser
import json
import datetime
import os

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.zip_file = zipfile.ZipFile(zip_path, 'r')
        self.current_path = []

    def ls(self):
        path = '/'.join(self.current_path)
        files = self.zip_file.namelist()
        items = []
        for f in files:
            if f.startswith(path):
                relative_path = f[len(path):].lstrip('/')
                if '/' in relative_path:
                    dir_name = relative_path.split('/')[0]
                    if dir_name not in items:
                        items.append(dir_name + '/')
                else:
                    items.append(relative_path)
        return items

    def cd(self, directory):
        if directory == '..':
            if self.current_path:
                self.current_path.pop()
        else:
            full_path = '/'.join(self.current_path + [directory]) + '/'
            if any(f.startswith(full_path) for f in self.zip_file.namelist()):
                self.current_path.append(directory)
            else:
                print(f"Directory '{directory}' not found")

    def read_file(self, file_path):
        full_path = '/'.join(self.current_path + [file_path])
        with self.zip_file.open(full_path) as f:
            return f.read().decode('utf-8')

    def tac(self, file_path):
        content = self.read_file(file_path)
        return content[::-1]

class ShellEmulator:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        print(f"Config read from: {config_path}")
        print(f"Config sections: {self.config.sections()}")
        print(f"Config items in DEFAULT: {self.config.items('DEFAULT')}")

        if 'DEFAULT' not in self.config:
            raise KeyError("Section 'DEFAULT' not found in config file")

        if 'vfs_path' not in self.config['DEFAULT']:
            raise KeyError("Key 'vfs_path' not found in 'DEFAULT' section of config file")

        self.vfs = VirtualFileSystem(self.config['DEFAULT']['vfs_path'])
        self.log_file = self.config['DEFAULT']['log_path']
        self.history = []
        self.hostname = self.config['DEFAULT']['computer_name']

    def log_action(self, action):
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'action': action
        }
        self.history.append(log_entry)
        with open(self.log_file, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')

    def run(self):
        while True:
            command = input(f"{self.hostname}:{'/'.join(self.vfs.current_path)}$ ")
            self.log_action(command)
            if command == 'exit':
                break
            elif command.startswith('ls'):
                print(self.vfs.ls())
            elif command.startswith('cd'):
                _, directory = command.split(' ', 1)
                self.vfs.cd(directory)
            elif command == 'uname':
                print(self.hostname)
            elif command.startswith('tac'):
                _, file_path = command.split(' ', 1)
                try:
                    print(self.vfs.tac(file_path))
                except KeyError as e:
                    print(f"Configuration error: {e}")
            elif command == 'history':
                for entry in self.history:
                    print(entry)

if __name__ == '__main__':
    try:
        emulator = ShellEmulator('config.ini')
        emulator.run()
    except KeyError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
