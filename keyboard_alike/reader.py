import usb.core
import usb.util

from keyboard_alike import mapping


class DeviceException(Exception):
    pass


class ReadException(Exception):
    pass


class Reader(object):
    def __init__(self, vendor_id, product_id, chunk_size, char_number, should_reset, debug=False):
        """
        :param vendor_id: USB vendor id (check dmesg or lsusb under Linux)
        :param product_id: USB device id (check dmesg or lsusb under Linux)
        :param chunk_size: chunk size like 6 or 8, check experimentally by looking on the raw output with debug=True
        :param should_reset: if true will also try to reset device preventing garbage reading.
        Doesn't work with all devices - locks them
        :param debug: if true will print raw data
        """
        self.interface = 0
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.chunk_size = chunk_size
        self.should_reset = should_reset
        self.debug = debug
        self._device = None
        self._endpoint = None
        self.char_number = char_number

    def initialize(self):
        self._device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)

        if self._device is None:
            raise DeviceException('No device found, check vendor_id and product_id')

        if self._device.is_kernel_driver_active(self.interface):
            try:
                self._device.detach_kernel_driver(self.interface)
            except usb.core.USBError as e:
                raise DeviceException('Could not detach kernel driver: %s' % str(e))

        try:
            self._device.set_configuration()
            if self.should_reset:
                self._device.reset()
        except usb.core.USBError as e:
            raise DeviceException('Could not set configuration: %s' % str(e))

        self._endpoint = self._device[0][(0, 0)][0]

    def read(self):
        data = []
        data_read = False

        while not data_read:
            try:
                data += self._endpoint.read(self._endpoint.wMaxPacketSize)    
                decoded_data = self.decode_raw_data(data);  
		#+1 pour le saut de ligne qu'on retire avant de retourner les données
                data_read = (len(decoded_data) == self.char_number + 1)
            except usb.core.USBError as e:
                print(e)
                data = []
        if self.debug:
            print('Raw data', data)
        return self.decode_raw_data(data).rstrip("\n")

    def decode_raw_data(self, raw_data):
        data = self.extract_meaningful_data_from_chunk(raw_data)
        return self.raw_data_to_keys(data)

    def extract_meaningful_data_from_chunk(self, raw_data):
        shift_indicator_index = 0
        raw_key_value_index = 2
        for chunk in self.get_chunked_data(raw_data):
            yield (chunk[shift_indicator_index], chunk[raw_key_value_index])

    def get_chunked_data(self, raw_data):
        return mapping.chunk_data(raw_data, self.chunk_size)

    @staticmethod
    def raw_data_to_keys(extracted_data):
        return ''.join(map(mapping.raw_to_key, extracted_data))

    def disconnect(self):
        if self.should_reset:
            self._device.reset()
        usb.util.release_interface(self._device, self.interface)
        self._device.attach_kernel_driver(self.interface)
