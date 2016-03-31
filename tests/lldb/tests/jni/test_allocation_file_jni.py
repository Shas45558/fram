'''Module that contains the test TestAllocationFileJNI.'''

from harness.test_base_remote import TestBaseRemote
import os

class TestAllocationFileJNI(TestBaseRemote):
    '''Tests saving an allocation of a JNI apk to disk and reloading it.'''

    def get_bundle_target(self):
        '''Return string with name of bundle executable to run.

        Returns:
            A string containing the name of the binary that this test can be run
            with.
        '''
        return 'JNIAllocations'

    def test_case(self, _):
        '''Run the lldb commands that are being tested.

        Raises:
            TestFail: One of the lldb commands did not provide the expected
            output.
        '''
        self.try_command('language renderscript kernel breakpoint all enable',
                         ['Breakpoints will be set on all kernels'])

        self.try_command('process continue',
                         ['resuming',
                          'stopped',
                          'stop reason = breakpoint'])

        # Binary file of int2 allocation
        file_int2 = self.get_tmp_file_path()

        self.try_command('language renderscript allocation save 12 ' +
                         file_int2,
                         ["Allocation written to file '%s'" % file_int2])

        # Check file was created
        self.test_assert(os.path.isfile(file_int2))

        # Load the file we just created, to assert the allocation contents are
        # the same
        self.try_command('language renderscript allocation load 12 ' +
                         file_int2,
                         ["Contents of file '%s' read into allocation 12" %
                          file_int2])
        os.remove(file_int2)

        self.try_command('language renderscript allocation dump 12',
                         ['(0, 0, 0) = {0 1}',
                          '(1, 0, 0) = {2 3}',
                          '(2, 0, 0) = {4 5}',
                          '(3, 0, 0) = {6 7}',
                          '(4, 0, 0) = {8 9}',
                          '(5, 0, 0) = {10 11}',
                          '(6, 0, 0) = {12 13}',
                          '(7, 0, 0) = {14 15}',
                          '(8, 0, 0) = {16 17}',
                          '(9, 0, 0) = {18 19}',
                          '(10, 0, 0) = {20 21}',
                          '(11, 0, 0) = {22 23}'])

        self.try_command('breakpoint del 1',
                         ['1 breakpoints deleted'])

        # Hit second kernel
        self.try_command('process continue',
                         ['resuming',
                          'stopped',
                          'stop reason = breakpoint'])

        # Binary file of uint allocation
        file_uint = self.get_tmp_file_path()

        self.try_command('language renderscript allocation save 28 ' +
                         file_uint,
                         ["Allocation written to file '%s'" % file_uint])

        # Check file was created
        self.test_assert(os.path.isfile(file_uint))

        # Test loading file into allocation with an incompatible type 'short'
        self.try_command('language renderscript allocation load 7 ' + file_uint,
                         ["Contents of file '%s' read into allocation 7" %
                          file_uint,
                          "Warning: Mismatched Element sizes",
                          "Warning: Mismatched Types",
                          "Warning: Mismatched allocation sizes"])

        # Check result of size inconsistency, mapping 4-byte unsigned to 2-byte
        # int
        self.try_command('language renderscript allocation dump 7',
                         ['(0, 0, 0) = 0',
                          '(1, 0, 0) = 0',
                          '(2, 0, 0) = 1',
                          '(3, 0, 0) = 0',
                          '(4, 0, 0) = 2',
                          '(5, 0, 0) = 0',
                          '(6, 0, 0) = 3',
                          '(7, 0, 0) = 0',
                          '(8, 0, 0) = 4',
                          '(9, 0, 0) = 0',
                          '(10, 0, 0) = 5',
                          '(11, 0, 0) = 0',
                          '(12, 0, 0) = 6',
                          '(13, 0, 0) = 0',
                          '(14, 0, 0) = 7',
                          '(15, 0, 0) = 0',
                          '(16, 0, 0) = 8',
                          '(17, 0, 0) = 0',
                          '(18, 0, 0) = 9',
                          '(19, 0, 0) = 0',
                          '(20, 0, 0) = 10',
                          '(21, 0, 0) = 0',
                          '(22, 0, 0) = 11',
                          '(23, 0, 0) = 0'])

        self.try_command('breakpoint del 2',
                         ['1 breakpoints deleted'])

        # Hit third kernel
        self.try_command('process continue',
                         ['resuming',
                          'stopped',
                          'stop reason = breakpoint'])

        # Test that uint allocation has been squared by square_kernel
        self.try_command('language renderscript allocation dump 28',
                         ['(0, 0, 0) = 0',
                          '(1, 0, 0) = 1',
                          '(2, 0, 0) = 4',
                          '(3, 0, 0) = 9',
                          '(4, 0, 0) = 16',
                          '(5, 0, 0) = 25',
                          '(6, 0, 0) = 36',
                          '(7, 0, 0) = 49',
                          '(8, 0, 0) = 64',
                          '(9, 0, 0) = 81',
                          '(10, 0, 0) = 100',
                          '(11, 0, 0) = 121',
                          '(12, 0, 0) = 144',
                          '(13, 0, 0) = 169',
                          '(14, 0, 0) = 196',
                          '(15, 0, 0) = 225',
                          '(16, 0, 0) = 256',
                          '(17, 0, 0) = 289',
                          '(18, 0, 0) = 324',
                          '(19, 0, 0) = 361',
                          '(20, 0, 0) = 400',
                          '(21, 0, 0) = 441',
                          '(22, 0, 0) = 484',
                          '(23, 0, 0) = 529'])

        # Load uint allocation from save before square_kernel had been run
        self.try_command('language renderscript allocation load 28 ' +
                         file_uint,
                         ["Contents of file '%s' read into allocation 28" %
                          file_uint])
        os.remove(file_uint)

        # Check contents are back to original
        self.try_command('language renderscript allocation dump 28',
                         ['(0, 0, 0) = 0',
                          '(1, 0, 0) = 1',
                          '(2, 0, 0) = 2',
                          '(3, 0, 0) = 3',
                          '(4, 0, 0) = 4',
                          '(5, 0, 0) = 5',
                          '(6, 0, 0) = 6',
                          '(7, 0, 0) = 7',
                          '(8, 0, 0) = 8',
                          '(9, 0, 0) = 9',
                          '(10, 0, 0) = 10',
                          '(11, 0, 0) = 11',
                          '(12, 0, 0) = 12',
                          '(13, 0, 0) = 13',
                          '(14, 0, 0) = 14',
                          '(15, 0, 0) = 15',
                          '(16, 0, 0) = 16',
                          '(17, 0, 0) = 17',
                          '(18, 0, 0) = 18',
                          '(19, 0, 0) = 19',
                          '(20, 0, 0) = 20',
                          '(21, 0, 0) = 21',
                          '(22, 0, 0) = 22',
                          '(23, 0, 0) = 23'])
