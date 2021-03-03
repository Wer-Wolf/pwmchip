from collections.abc import Sequence

# Path definitions
PWM_BASE_PATH = '/sys/class/pwm'
PWM_PATH = PWM_BASE_PATH + '/pwmchip%d'

# Files and directories found inside PWM_PATH
PWM_EXPORT_FILE = 'export'
PWM_UNEXPORT_FILE = 'unexport'
PWM_CHANNELS_FILE = 'npwm'
PWM_CHANNEL_FOLDER = 'pwm%d'

# Files found inside PWM_CHANNEL_FOLDER
PWM_CHANNEL_ENABLE_FILE = 'enable'
# Both in nanoseconds
PWM_CHANNEL_DUTY_CYCLE_FILE = 'duty_cycle'
PWM_CHANNEL_PERIOD_FILE = 'period'
# normal or inversed
PWM_CHANNEL_POLARITY_FILE = 'polarity'


class PwmChannel:
    def __init__(self, path, force):
        pass


class PwmChip(Sequence):
    def __init__(self, chip, force=False):
        self.path = PWM_PATH % chip
        self.force = force
        channels = '/'.join((self.path, PWM_CHANNELS_FILE))
        with open(channels, 'r') as fd:
            self.channels = int(fd.read())

    def __len__(self):
        return self.channels

    def __getitem__(self, key):
        if isinstance(key, int):
            if key > len(self) - 1:
                raise IndexError('Not enough channels available')
            elif key < 0:
                raise IndexError('Negative channels are not supported')
            path = '/'.join((self.path, PWM_CHANNEL_FOLDER))
            return PwmChannel(path, self.force)
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return list([self[i] for i in range(start, stop, step)])
        elif isinstance(key, tuple):
            return list([self[i] for i in key])
        else:
            raise TypeError('Unsupported type')
