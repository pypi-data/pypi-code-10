
#   Package structure:
#       pynrfjprog:
#           __init__.py         -   Module definition file
#           API.py              -   Python wrappers around NRFJPROG DLL functions.
#           Hex.py              -   Provides a way to parse a hex file in order to program it into the device using API.write().
#           JLink.py            -   Provides a function to find the latest Segger JLinkARM.dll installed in the PC.


#    Note:
#        Please look in the nrfjprogdll.h file provided with the tools for a more elaborate 
#        description of the API functions.

# Imports from future that make python 2 behave as python 3.

from __future__ import division
from __future__ import print_function
from builtins import int

import sys
import os
import ctypes
from enum import IntEnum, unique

try:
    from . import JLink
except Exception:
    import JLink

py2 = sys.version_info[0] == 2
py3 = sys.version_info[0] == 3

DEBUG_OUTPUT = False

 
@unique
class DeviceFamily(IntEnum):
    """Wraps device_family_t values from nrfjprogdll.h """
    NRF51              = 0
    NRF52              = 1

@unique
class DeviceVersion(IntEnum):
    """Wraps device_version_t values from nrfjprogdll.h"""
    UNKNOWN                   = 0
    NRF51_XLR1                = 1
    NRF51_XLR2                = 2
    NRF51_XLR3                = 3
    NRF51_L3                  = 4
    NRF51_XLR3P               = 5
    NRF51_XLR3LC              = 6
    NRF52_FP1_MPW3            = 7
    NRF52_FP1                 = 8
    
@unique
class NrfjprogdllErr(IntEnum):
    """Wraps nrfjprogdll_err_t values from nrfjprogdll.h"""
    SUCCESS                                     =  0
    OUT_OF_MEMORY                               = -1 
    INVALID_OPERATION                           = -2
    INVALID_PARAMETER                           = -3
    INVALID_DEVICE_FOR_OPERATION                = -4
    EMULATOR_NOT_CONNECTED                      = -10
    CANNOT_CONNECT                              = -11
    LOW_VOLTAGE                                 = -12
    NO_EMULATOR_CONNECTED                       = -13
    NVMC_ERROR                                  = -20
    NOT_AVAILABLE_BECAUSE_PROTECTION            = -90
    JLINKARM_DLL_NOT_FOUND                      = -100
    JLINKARM_DLL_COULD_NOT_BE_OPENED            = -101
    JLINKARM_DLL_ERROR                          = -102
    JLINKARM_DLL_TOO_OLD                        = -103
    NRFJPROG_SUB_DLL_NOT_FOUND                  = -150
    NRFJPROG_SUB_DLL_COULD_NOT_BE_OPENED        = -151
    NOT_IMPLEMENTED_ERROR                       = -255

@unique    
class ReadbackProtection(IntEnum):
    """Wraps readback_protection_status_t values from nrfjprogdll.h"""
    NONE                       = 0
    REGION_0                   = 1
    ALL                        = 2
    BOTH                       = 3

@unique
class Region0Source(IntEnum):
    """Wraps region_0_source_t values from nrfjprogdll.h"""
    NO_REGION_0                = 0
    FACTORY                    = 1
    USER                       = 2
    
@unique
class RamPower(IntEnum):
    """Wraps ram_power_status_t values from nrfjprogdll.h"""
    OFF                    = 0
    ON                     = 1

@unique
class CpuRegister(IntEnum):
    """Wraps cpu_registers_t values from jlinkarm_nrfjprogdll.h"""
    R0                        = 0
    R1                        = 1
    R2                        = 2
    R3                        = 3
    R4                        = 4
    R5                        = 5
    R6                        = 6
    R7                        = 7
    R8                        = 8
    R9                        = 9
    R10                       = 10
    R11                       = 11
    R12                       = 12
    R13                       = 13
    R14                       = 14
    R15                       = 15
    XPSR                      = 16
    MSP                       = 17
    PSP                       = 18
    

class APIError(Exception):
    """Subclass for reporting errors."""

    def __init__(self, err_str, err_code=None):
        """Constructs a new object and saves the err_code in addition to the message err_str."""
        super(Exception, self).__init__(err_str)
        self.err_code = err_code

    @classmethod
    def from_nrfjprog_err(cls, err_code):
        """Creates a new APIError with a string describing the given err_code value."""
        if err_code in [member.value for name, member in NrfjprogdllErr.__members__.items()]:
            return APIError("An error was reported by NRFJPROG DLL: %d ('%s')." % (err_code, NrfjprogdllErr(err_code).name), err_code)
        
        return APIError(("An error was reported by NRFJPROG DLL: %d." % err_code), err_code)


class API(object):
    """Provides simplified access to the nrfjprog.dll API."""

    # A copy of NRFJPROG.DLL must be found in the working directory for the API to work.
    
    _DEFAULT_JLINK_SPEED_KHZ            = 2000
    

    class DLLFunction(object):
        """Wrapper for calls into a DLL via ctypes."""

        _LOG_CB = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
        _NRFJPROG_ERROR = ctypes.c_int32


        def __init__(self, key, restype, argtypes):
            """Creates a wrapper for the functional with the given symbol of a DLL."""
            self._key = key
            self._restype  = restype
            self._argtypes = argtypes
            self._callbacks= []


        def set_lib(self, lib):
            """Configures the parameters for this wrapper's function."""
            if (self._key is not None):
                self._lib = lib
                self._lib[self._key].restype  = self._restype
                self._lib[self._key].argtypes = self._argtypes
                del(self._callbacks[:])


        def __call__(self, *args):
            """Casts the given arguments into the expected types and then calls this wrapper's function."""
            params = []

            if (self._key is None):
                raise APIError('Object construction cannot be called without a valid symbol.')

            for i in range(0, len(args)):
                if (args[i] is not None):
                    param = self._argtypes[i](args[i])
                else:
                    param = self._argtypes[i]()

                params.append(param)
                if (self._LOG_CB == self._argtypes[i]):
                    self._callbacks.append(param)

            if (self._restype is not None):
                return self._lib[self._key](*params)
            else:
                self._lib[self._key](*params)


    _DLL_FUNCTIONS = {
                    'dll_version':                      DLLFunction( 'dll_version', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint8)]),
                    
                    'open_dll':                         DLLFunction( 'open_dll', DLLFunction._NRFJPROG_ERROR, [ctypes.c_char_p, DLLFunction._LOG_CB, ctypes.c_uint32]),

                    'close_dll':                        DLLFunction( 'close_dll', None, None),

                    'enum_emu_snr':                     DLLFunction( 'enum_emu_snr', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]),

                    'is_connected_to_emu':              DLLFunction( 'is_connected_to_emu', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_bool)]),   
                    
                    'connect_to_emu_with_snr':          DLLFunction( 'connect_to_emu_with_snr', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32]),                                               

                    'connect_to_emu_without_snr':       DLLFunction( 'connect_to_emu_without_snr', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]), 

                    'disconnect_from_emu':              DLLFunction( 'disconnect_from_emu', DLLFunction._NRFJPROG_ERROR, None),                    
                    
                    'recover':                          DLLFunction( 'recover', DLLFunction._NRFJPROG_ERROR, None),
                    
                    'is_connected_to_device':           DLLFunction( 'is_connected_to_device', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_bool)]),   
                    
                    'connect_to_device':                DLLFunction( 'connect_to_device', DLLFunction._NRFJPROG_ERROR, None),                                               
                    
                    'readback_protect':                 DLLFunction( 'readback_protect', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]),

                    'readback_status':                  DLLFunction( 'readback_status', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'read_region_0_size_and_source':    DLLFunction( 'read_region_0_size_and_source', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32)]),

                    'sys_reset':                        DLLFunction( 'sys_reset', DLLFunction._NRFJPROG_ERROR, None),
                    
                    'pin_reset':                        DLLFunction( 'pin_reset', DLLFunction._NRFJPROG_ERROR, None),
                    
                    'disable_bprot':                    DLLFunction( 'disable_bprot', DLLFunction._NRFJPROG_ERROR, None),

                    'erase_all':                        DLLFunction( 'erase_all', DLLFunction._NRFJPROG_ERROR, None),

                    'erase_page':                       DLLFunction( 'erase_page', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]),

                    'erase_uicr':                       DLLFunction( 'erase_uicr', DLLFunction._NRFJPROG_ERROR, None),                                                   

                    'write_u32':                        DLLFunction( 'write_u32', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_bool]),

                    'read_u32':                         DLLFunction( 'read_u32', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'write':                            DLLFunction( 'write', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.c_bool]),

                    'read':                             DLLFunction( 'read', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32]),
                    
                    'is_halted':                        DLLFunction( 'is_halted', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_bool)]),   
                    
                    'halt':                             DLLFunction( 'halt', DLLFunction._NRFJPROG_ERROR, None),   
                    
                    'run':                              DLLFunction( 'run', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32]),
                    
                    'go':                               DLLFunction( 'go', DLLFunction._NRFJPROG_ERROR, None),   
                    
                    'is_ram_powered':                   DLLFunction( 'is_ram_powered', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32) , ctypes.POINTER(ctypes.c_uint32)]),   

                    'power_ram_all':                    DLLFunction( 'power_ram_all', DLLFunction._NRFJPROG_ERROR, None),   
                    
                    'unpower_ram_section':              DLLFunction( 'unpower_ram_section', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32]),   
                    
                    'read_cpu_register':                DLLFunction( 'read_cpu_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'write_cpu_register':               DLLFunction( 'write_cpu_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint32, ctypes.c_uint32]),
                    
                    'read_device_version':              DLLFunction( 'read_device_version', DLLFunction._NRFJPROG_ERROR, [ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'read_debug_port_register':         DLLFunction( 'read_debug_port_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'write_debug_port_register':        DLLFunction( 'write_debug_port_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint8, ctypes.c_uint32]),
                    
                    'read_access_port_register':        DLLFunction( 'read_access_port_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint8, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32)]),
                    
                    'write_access_port_register':       DLLFunction( 'write_access_port_register', DLLFunction._NRFJPROG_ERROR, [ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint32]),
                }

    def __init__(self, device_family, jlink_arm_dll_path=None, log_str_cb=None):
        """The log_str_cb callback can be used to receive log and error information. These callbacks should expect to
        receive a string as the only parameter and do not need to return anything."""
        # Decode the family of devices to use
        self._device_family = self._decode_enum(device_family, DeviceFamily)
        if self._device_family is None:
            raise APIError('Parameter device_family must be of type int, str or DeviceFamily enumeration.')
            
        # Obtain the path to JLINKARM.dll
        self._jlink_arm_dll_path = None
        if jlink_arm_dll_path is None:
            jlink_arm_dll_path = JLink.find_latest_dll()
            if jlink_arm_dll_path is None:
                raise APIError('Could not locate a JLinkARM.dll in the default SEGGER installation path.')
        else:
            if not self._is_string(jlink_arm_dll_path):
                raise APIError('Parameter jlink_arm_dll_path must be the path to JLinkARM.dll in str type.')
        if py2:
            self._jlink_arm_dll_path = os.path.abspath(jlink_arm_dll_path)
        elif py3:
            self._jlink_arm_dll_path = os.path.abspath(jlink_arm_dll_path.encode('ascii'))

        # Obtain the possible logging callback function
        if log_str_cb is not None:
            if not hasattr(log_str_cb, '__call__'):
                raise APIError('Parameter log_str_cb is not callable.')
        elif DEBUG_OUTPUT:
            log_str_cb = lambda x: self._debug_print(x, '[NRFJPROG DLL LOG]')                    
        self._log_str_cb            = log_str_cb
        
        # Find the NRFJPROG DLL in the working directory.
        this_dir, this_file = os.path.split(__file__) 
        
        if sys.platform.lower().startswith('win'):
            nrfjprog_dll_name = 'nrfjprog.dll'
        elif sys.platform.lower().startswith('linux'):
            nrfjprog_dll_name = 'libnrfjprogdll.so'
        
        nrfjprog_dll_path = os.path.join(os.path.abspath(this_dir), nrfjprog_dll_name)

        if not nrfjprog_dll_path:
            raise APIError("Failed to locate the NRFJPROG DLL in the pynrfjprog directory.")
        
        try:
            self._lib = ctypes.CDLL(nrfjprog_dll_path)
        except Exception as err:
            raise APIError("Could not load the NRFJPROG DLL: '%s'." % err)
        
        # Load the functions from the library
        for key in self._DLL_FUNCTIONS:
            self._DLL_FUNCTIONS[key].set_lib(self._lib)
        

    def dll_version(self):
        """ Returns the JLinkARM.dll version."""
        
        major = ctypes.c_uint32()
        minor = ctypes.c_uint32()
        revision = ctypes.c_uint8()
        
        result = self._DLL_FUNCTIONS['dll_version'](major, minor, revision)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
        return (major.value, minor.value, chr(revision.value))
        
            
    def open(self):
        """ Opens the JLinkARM DLL and prepares the dll to work with a specific nRF device family."""
        
        result = self._DLL_FUNCTIONS['open_dll'](self._jlink_arm_dll_path, self._log_str_cb, self._device_family.value)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def close(self):
        """ Closes and frees the JLinkARM DLL."""
        
        self._DLL_FUNCTIONS['close_dll']()
    
    
    def enum_emu_snr(self):
        """ Enumerates the serial numbers of connected USB J-Link emulators.
            Return: List with the serial numbers of connected emulators."""
        
        serial_numbers_len  = 50
        serial_numbers      = (ctypes.c_uint32 * serial_numbers_len)()
        num_available       = ctypes.c_uint32()

        result = self._DLL_FUNCTIONS['enum_emu_snr'](serial_numbers, serial_numbers_len, num_available)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
       
        snr = [int(serial_numbers[i]) for i in range(0, min(num_available.value, serial_numbers_len))]

        if len(snr) == 0:
            return None
        else:
            return snr

            
    def is_connected_to_emu(self):
        """ Checks if the emulator has an established connection with Segger emulator/debugger. 
            Return: True or False."""
        
        is_connected_to_emu = ctypes.c_bool()
        result = self._DLL_FUNCTIONS['is_connected_to_emu'](is_connected_to_emu)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return is_connected_to_emu.value
        
    
    def connect_to_emu_with_snr(self, serial_number, jlink_speed_khz=_DEFAULT_JLINK_SPEED_KHZ):
        """ Connects to a given emulator/debugger.
            Input: Serial number of the emulator to connect to. Optional: Speed for the SWD communication."""
        
        if not self._is_u32(serial_number):
            raise APIError('The serial_number parameter must be an unsigned 32bit value.')
        
        if not self._is_u32(jlink_speed_khz):
            raise APIError('The jlink_speed_khz parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['connect_to_emu_with_snr'](serial_number, jlink_speed_khz)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
        
        
    def connect_to_emu_without_snr(self, jlink_speed_khz=_DEFAULT_JLINK_SPEED_KHZ):
        """ Connects to an emulator/debugger. If more than one emulator is available, a pop-up window will appear.
            Input: Optional: Speed for the SWD communication."""
        
        if not self._is_u32(jlink_speed_khz):
            raise APIError('The jlink_speed_khz parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['connect_to_emu_without_snr'](jlink_speed_khz)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
            
    def disconnect_from_emu(self):
        """ Disconnects from a connected emulator. """
        
        result = self._DLL_FUNCTIONS['disconnect_from_emu']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
        
        
    def recover(self):
        """ Recovers the device."""
        
        result = self._DLL_FUNCTIONS['recover']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
    
    def is_connected_to_device(self):
        """ Checks if the emulator has an established connection with an nRF device.
            Return: True or False."""
        
        is_connected_to_device  = ctypes.c_bool()
        result = self._DLL_FUNCTIONS['is_connected_to_device'](is_connected_to_device)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return is_connected_to_device.value
    
    
    def connect_to_device(self):
        """ Connects to the nRF device and halts it."""
        
        result = self._DLL_FUNCTIONS['connect_to_device']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
    
    def readback_protect(self, desired_protection_level):
        """ Protects the device against read or debug.
            Input: Desired protection level of readback protection (ReadbackProtection)."""
        
        if not self._is_enum(desired_protection_level, ReadbackProtection):
            raise APIError('Parameter desired_protection_level must be of type int, str or ReadbackProtection enumeration.')
            
        desired_protection_level = self._decode_enum(desired_protection_level, ReadbackProtection)
        if desired_protection_level is None:
            raise APIError('Parameter desired_protection_level must be of type int, str or ReadbackProtection enumeration.')
        
        result = self._DLL_FUNCTIONS['readback_protect'](desired_protection_level.value)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
    
    def readback_status(self):
        """ Returns the status of the readback protection.
            Return: ReadbackProtection status."""
        
        status  = ctypes.c_uint32()
        result = self._DLL_FUNCTIONS['readback_status'](status)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return ReadbackProtection(status.value).name
        
        
    def read_region_0_size_and_source(self):
        """ Returns the region 0 size and source of protection if any.
            Return: Region size, and ReadbackProtection."""
        
        size  = ctypes.c_uint32()
        source  = ctypes.c_uint32()
        result = self._DLL_FUNCTIONS['read_region_0_size_and_source'](size, source)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return size.value, Region0Source(source.value).name
   
   
    def sys_reset(self):
        """ Executes a system reset request."""
        
        result = self._DLL_FUNCTIONS['sys_reset']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def pin_reset(self):
        """ Executes a pin reset."""
        
        result = self._DLL_FUNCTIONS['pin_reset']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def disable_bprot(self):
        """ Disables BPROT."""
        
        result = self._DLL_FUNCTIONS['disable_bprot']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
        
    def erase_all(self):
        """ Erases all flash."""
        
        result = self._DLL_FUNCTIONS['erase_all']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

    
    def erase_page(self, addr):
        """ Erases a page of code flash.
            Input: Address of the code flash page to erase."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')
    
        result = self._DLL_FUNCTIONS['erase_page'](addr)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
    
        
    def erase_uicr(self):
        """ Erases UICR."""
        
        result = self._DLL_FUNCTIONS['erase_uicr']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            

    def write_u32(self, addr, data, control):
        """ Writes one uint32_t data at the given address.
            Input: Address to write to. Value to write. If the target address needs NVMC control."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')

        if not self._is_u32(data):
            raise APIError('The data parameter must be an unsigned 32bit value.')
            
        if not self._is_bool(control):
            raise APIError('The control parameter must be a boolean value.')

        result = self._DLL_FUNCTIONS['write_u32'](addr, data, control)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            

    def read_u32(self, addr):
        """ Reads one uint32 address.
            Input: Address to read from.
            Return: uint32 value at address."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')

        data  = ctypes.c_uint32()
        result = self._DLL_FUNCTIONS['read_u32'](addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return data.value
        

    def write(self, addr, data, control):
        """ Writes data from the buffer starting at the given address.
            Input: Start address of the region to write to. Buffer with data to write. If the target 
            address needs NVMC control."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')

        if not self._is_valid_buf(data):
            raise APIError('The data parameter must be a tuple or a list with at least one item.')
            
        if not self._is_bool(control):
            raise APIError('The control parameter must be a boolean value.')
        
        data = (ctypes.c_uint8 * len(data))(*data)

        result = self._DLL_FUNCTIONS['write'](addr, data, len(data), control)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

   
    def read(self, addr, length):
        """ Reads length bytes starting at address addr.
            Input: Address to read from. Number of bytes to read.
            Return: Returns list with uint8 values from addr."""
        
        if not self._is_u32(addr):
            raise APIError('The addr parameter must be an unsigned 32bit value.')

        if not self._is_u32(length):
            raise APIError('The length parameter must be an unsigned 32bit value.')

        data = (ctypes.c_uint8 * length)()

        result = self._DLL_FUNCTIONS['read'](addr, data, length)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return list(data)


    def is_halted(self):
        """ Checks if the nRF CPU is halted.
            Return: True of False."""
        
        is_halted  = ctypes.c_bool()
        result = self._DLL_FUNCTIONS['is_halted'](is_halted)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return is_halted.value
        

    def halt(self):
        """ Halts the nRF CPU."""
        
        result = self._DLL_FUNCTIONS['halt']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

            
    def run(self, pc, sp):
        """ Starts the nRF CPU with the given pc and sp.
            Input: Program Counter to start running from. Stack Pointer to use when running."""
        
        if (not self._is_u32(pc)):
            raise APIError('The pc parameter must be an unsigned 32bit value.')

        if (not self._is_u32(sp)):
            raise APIError('The sp parameter must be an unsigned 32bit value.')

        result = self._DLL_FUNCTIONS['run'](pc, sp)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)


    def go(self):
        """ Starts the nRF CPU."""
        
        result = self._DLL_FUNCTIONS['go']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
            
    def is_ram_powered(self):
        """ Reads the RAM power status.
            Return: List with RAM power information; array of results, number of sections in device, size of sections."""
        
        status_size = 64
        status = (ctypes.c_uint32 * status_size)()
        number  = ctypes.c_uint32()
        size  = ctypes.c_uint32()

        result = self._DLL_FUNCTIONS['is_ram_powered'](status, status_size, number, size)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
        
        return [RamPower(elem).name for elem in list(status)[0:number.value]], number.value, size.value
       
    
    def power_ram_all(self):
        """ Powers all RAM sections of the device."""
        
        result = self._DLL_FUNCTIONS['power_ram_all']()
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
     
     
    def unpower_ram_section(self, section_index):
        """ Unpowers a RAM section of the device.
            Input: Index of RAM section to power_off."""
        
        if (not self._is_u32(section_index)):
            raise APIError('The section_index parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['unpower_ram_section'](section_index)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
    
    def read_cpu_register(self, register_name):
        """ Reads a CPU register.
            Input: CPU Register name to read (CpuRegister).
            Return: uint32 value from register."""
        
        if not self._is_enum(register_name, CpuRegister):
            raise APIError('Parameter register_name must be of type int, str or CpuRegister enumeration.')
            
        register_name = self._decode_enum(register_name, CpuRegister)
        if register_name is None:
            raise APIError('Parameter register_name must be of type int, str or CpuRegister enumeration.')
        
        value  = ctypes.c_uint32()
        result = self._DLL_FUNCTIONS['read_cpu_register'](register_name.value, value)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return value.value
        
        
    def write_cpu_register(self, register_name, value):
        """ Writes a CPU register.
            Input: CPU register to write (CpuRegister). uint32 Value to write."""
        
        if (not self._is_u32(value)):
            raise APIError('The value parameter must be an unsigned 32bit value.')

        if not self._is_enum(register_name, CpuRegister):
            raise APIError('Parameter register_name must be of type int, str or CpuRegister enumeration.')
            
        register_name = self._decode_enum(register_name, CpuRegister)
        if register_name is None:
            raise APIError('Parameter register_name must be of type int, str or CpuRegister enumeration.')
        
        result = self._DLL_FUNCTIONS['write_cpu_register'](register_name, value)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
    
    def read_device_version(self):
        """ Reads the device version connected to the device.
            Return: uint32 DeviceVersion number."""
        
        version = ctypes.c_uint32()

        result = self._DLL_FUNCTIONS['read_device_version'](version)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return DeviceVersion(version.value).name
        
        
    def read_debug_port_register(self, reg_addr):
        """ Reads a debugger debug port register.
            Input: Register address to read.
            Return: uin32 data Value from register."""
        
        if (not self._is_u8(reg_addr)):
            raise APIError('The reg_addr parameter must be an unsigned 8bit value.')
        
        data  = ctypes.c_uint32()
        
        result = self._DLL_FUNCTIONS['read_debug_port_register'](reg_addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return data.value
        
    
    def write_debug_port_register(self, reg_addr, data):
        """ Writes a debugger debug port register.
            Input: Register address to write. uint32 data to write into register."""
        
        if (not self._is_u8(reg_addr)):
            raise APIError('The reg_addr parameter must be an unsigned 8bit value.')
            
        if (not self._is_u32(data)):
            raise APIError('The data parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['write_debug_port_register'](reg_addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)
            
    
    def read_access_port_register(self, ap_index, reg_addr):
        """ Reads a debugger access port register.
            Input: Access port index for red if ap_access. Register address to read.
            Return: uint32 data value from register."""
        
        if (not self._is_u8(ap_index)):
            raise APIError('The ap_index parameter must be an unsigned 8bit value.')
            
        if (not self._is_u8(reg_addr)):
            raise APIError('The reg_addr parameter must be an unsigned 8bit value.')
        
        data  = ctypes.c_uint32()
        
        result = self._DLL_FUNCTIONS['read_access_port_register'](ap_index, reg_addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

        return data.value
        
    
    def write_access_port_register(self, ap_index, reg_addr, data):
        """ Writes a debugger access port register.
            Input: Access port index for write if ap_access. Register address to write. Data to write to register."""
        
        if (not self._is_u8(ap_index)):
            raise APIError('The ap_index parameter must be an unsigned 8bit value.')
            
        if (not self._is_u8(reg_addr)):
            raise APIError('The reg_addr parameter must be an unsigned 8bit value.')
            
        if (not self._is_u32(data)):
            raise APIError('The data parameter must be an unsigned 32bit value.')
        
        result = self._DLL_FUNCTIONS['write_access_port_register'](ap_index, reg_addr, data)
        if result != NrfjprogdllErr.SUCCESS:
            raise APIError.from_nrfjprog_err(result)

            
    def _is_u32(self, value):
        """ Checks if a value is uint32."""
        if not isinstance(value, int):
            return False

        return (0 <= value <= 0xFFFFFFFF)
        
        
    def _is_u8(self, value):
        """ Checks if a value is uint8."""
        if not isinstance(value, int):
            return False

        return (0 <= value <= 0xFF)

        
    def _is_bool(self, value):
        """ Checks if value is boolean."""
        if not isinstance(value, int):
            return False

        return (0 <= value <= 1)
        

    def _is_valid_buf(self, buf):
        """ Checks if a buffer is valid or not."""
        if not isinstance(buf, tuple) and not isinstance(buf, list):
            return False

        for value in buf:
            if value < 0:
                return False

        return (len(buf) != 0)
        
        
    def _is_number(self, value):
        """ Checks if value is number."""
        if not isinstance(value, int):
            return False
            
        return True
        
        
    def _is_string(self, string):
        """ Checks if string is string."""
        return isinstance(string, str)
        
        
    def _is_enum(self, param, enum_type):
        """ Checks if param is enum_type."""
        if self._is_number(param):
            if param in [member.value for name, member in enum_type.__members__.items()]:
                return True
        elif self._is_string(param):
            if param in [name for name, member in enum_type.__members__.items()]:
                return True
        elif param in enum_type.__members__.items():
            return True
        
        return False

    def _decode_enum(self, param, enum_type):
        """ Decodes param of enum_type."""
        if not self._is_enum(param, enum_type):
            return None
        
        if self._is_number(param):
            return enum_type(param)
        elif self._is_string(param):
            return enum_type[param]
        else: 
            return param
        

    def __enter__(self):
        """ Called automatically when the 'with' construct is used."""
        self.open()
        return self


    def __exit__(self, type, value, traceback):
        """ Called automatically when the 'with' construct is used."""
        self.close()


    def _debug_print(self, msg_str, prefix='[nrfjprog.API] '):
        print("{} {}".format(prefix, msg_str.strip()), file=sys.stderr)
        
        
