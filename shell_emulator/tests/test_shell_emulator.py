import pytest
from shell_emulator import ShellEmulator, VirtualFileSystem

@pytest.fixture
def emulator():
    return ShellEmulator('config.ini')

def test_ls(emulator):
    assert 'file1.txt' in emulator.vfs.ls()
    assert 'dir1/' in emulator.vfs.ls()

def test_cd(emulator):
    emulator.vfs.cd('dir1')
    assert emulator.vfs.current_path == ['dir1']
    emulator.vfs.cd('..')
    assert emulator.vfs.current_path == []

def test_uname(emulator):
    assert emulator.hostname == 'ASUS'

def test_tac(emulator):
    content = emulator.vfs.tac('file1.txt')
    assert content == 'denepo 1elif'

def test_history(emulator):
    emulator.log_action('test command')
    assert len(emulator.history) == 1
    assert emulator.history[0]['action'] == 'test command'
