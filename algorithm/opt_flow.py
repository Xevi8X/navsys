import cv2 as cv
import numpy as np

class OpticalFlow:
    def __init__(self):
        self.MIN_FEATURES = 3

        self.params_features = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
        
        self.param_lk = dict( winSize  = (15, 15),
                        maxLevel = 2,
                        criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
        
        self.frame_old = None
        self.p0 = None
        self.mask = None

    def reset(self):
        self.frame_old = None
        self.p0 = None
        self.mask = None
    
    def feed(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if self.frame_old is None or self.p0 is None or len(self.p0) < self.MIN_FEATURES:
            self.frame_old = frame.copy()
            self.p0 = self._find_features(frame)
            return None

        return self._calc_optical_flow(frame)
    
    def remove_features(self, features : list[(int, int)]):
        new_p0 = []
        for px in self.p0:
            if (px[0][0], px[0][1]) not in features:
                new_p0.append(px)
        self.p0 = np.array(new_p0)

    def set_mask(self, mask):
        self.mask = mask
        
    def _find_features(self, frame):
        return cv.goodFeaturesToTrack(frame, mask=self.mask, **self.params_features)
    
    def _calc_optical_flow(self, frame):
        frame = cv.bitwise_and(frame, frame, mask=self.mask)
        p1, st, err = cv.calcOpticalFlowPyrLK(self.frame_old, frame, self.p0, None, **self.param_lk)
        if p1 is not None:
            pixels_old = self.p0[st==1]
            pixels_new = p1[st==1]
            self.p0 = pixels_new.reshape(-1, 1, 2)
            self.frame_old = frame.copy()
            pixels = []
            for px_old, px_new in zip(pixels_old, pixels_new):
                x_old, y_old = px_old.ravel()
                x_new, y_new = px_new.ravel()
                pixels.append((x_old, y_old, x_new, y_new))
            return pixels

        self.p0 = None
        return None


        

        