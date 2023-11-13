import numpy as np

class XL330:
    def __init__(self, id: int):
        self.id = id
        self.DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
        self.DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
        self.inputDirection = self._reversedInternal(False)

    def setMinMaxPositionValue(self, min: int, max: int):
        self.DXL_MINIMUM_POSITION_VALUE = min
        self.DXL_MAXIMUM_POSITION_VALUE = max

    def _reversedInternal(self, reversed: bool):
        if reversed:
            return -1
        else:
            return 1
        
    def setReverseInputDirection(self, reversed: bool):
        self.inputDirection = self._reversedInternal(reversed)

    def getGoalPos(self, x: float) -> int:
        right_direction = x*self.inputDirection
        pwm = np.interp(right_direction, [-1, 1], [self.DXL_MINIMUM_POSITION_VALUE, self.DXL_MAXIMUM_POSITION_VALUE])
        return int(np.clip(pwm, self.DXL_MINIMUM_POSITION_VALUE, self.DXL_MAXIMUM_POSITION_VALUE))
    

if __name__ == "__main__":
    test = XL330(1)
    print(test.getGoalPos(1))
    test.setReverseInputDirection(True)
    print(test.getGoalPos(-1))