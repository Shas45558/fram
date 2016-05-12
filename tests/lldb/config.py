'''LLDB-Renderscript test suite configuration file.

This file contains the default test suite config which will be used in the
case a developer did not supply a custom one.'''

import os

class Config(object):
    '''Test suite configuration object.

    The Config class is used by the test suite to abstract the specifics of a
    user's local setup.  This config can be overridden by specifying a custom
    config on the command line.'''
    # pylint: disable=no-self-use

    @property
    def adb_path(self):
        '''Path to android debug bridge on the host.'''
        return 'adb'

    @property
    def host_port(self):
        '''Specify host port which lldb-server will be forwarded to.

        Specify the starting host port number that lldb-server (on the target)
        will be forwarded to on the host. Each successive test will increment
        onwards from this initial port.'''
        return 1234

    @property
    def device_port(self):
        '''Specify the port number that lldb-server (on the device) listens on.

        When lldb-server is spawned on the device it will listen on this port.
        Each successive test will increment onwards from this port.'''
        return 1234

    @property
    def lldb_server_path_device(self):
        '''Path to the lldb-server executable on the device.'''
        return '/data/lldb-server'

    @property
    def lldb_server_path_host(self):
        '''Path to the lldb-server executable on host (if using -run-emu).'''
        return 'lldb-server'

    @property
    def aosp_product_path(self):
        '''The path to the "out" folder of the AOSP repository.'''
        return os.getenv('ANDROID_PRODUCT_OUT')

    @property
    def log_file_path(self):
        '''The path to the folder where the log file will be placed.'''
        return os.path.join(os.getcwd(), 'LLDBTestsuiteLog.txt')

    @property
    def results_file_path(self):
        '''Output folder where junit results.xml file will be placed.'''
        return os.path.join(os.getcwd(), 'results.xml')

    @property
    def lldb_path(self):
        '''The path to lldb executable on the host.'''
        return 'lldb'

    @property
    def blacklist(self):
        '''Provide a test blacklist for skipping specific tests.

        To specify the blacklist from the command line the following can be
        used: --blacklist test1.py test2.py ...'''
        return []

    @property
    def verbose(self):
        '''Flag to indicate whether to store extra output in the logs.'''
        return False

    @property
    def device(self):
        '''Specify the device id of the device to run on.

        When multiple devices or emulators are present, a specific device to
        use while testing can be indicated here.'''
        return os.environ.get('ANDROID_SERIAL', None)

    @property
    def timeout(self):
        '''Timeout period for a single command, expressed in seconds'''
        return 60 * 15

    @property
    def emu_cmd(self):
        '''The command line for the emulator (if using -run-emu).'''
        return os.path.join(os.path.dirname(__file__), '..', '..', '..', '..',
                            'prebuilts', 'android-emulator', 'linux-x86_64',
                            'emulator')