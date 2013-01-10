import cv2.cv as cv
import sys

##Track an object using it's color
##constructor takes in cam number
##output array (x,y) of obj location
 
color_tracker_window = "Color Tracker" 
 
class ColorTracker: 
    
    objPos = []
    
    def __init__(camNum): 
        cv.NamedWindow( color_tracker_window, 1 ) 
        self.capture = cv.CaptureFromCAM(camNum)

    def getPos(self):
        return self.objPos
        
    def run(self): 
        while True: 
            img = cv.QueryFrame( self.capture )

            if img is []:
                print 'Error: frame is null...\n'
                break;
                                       
            hsv_min = cv.Scalar(140,100,130)
            hsv_max = cv.Scalar(358,256,255)
            hsv_img = cv.CreateImage(cv.GetSize(img),8,3)
            thresholded = cv.CreateImage(cv.GetSize(img),8,1)
            cv.CvtColor(img,hsv_img,cv.CV_BGR2HSV)
            cv.InRangeS(hsv_img,hsv_min,hsv_max,thresholded)
            storage = cv.CreateMemStorage(0)
            cv.Smooth(thresholded, thresholded,2,9,9)
            image = cv.GetMat(thresholded)
            
            #determine the objects moments and check that the area is large  
            #enough to be our object 
            moments = cv.Moments(image, 0) 
            area = cv.GetCentralMoment(moments, 0, 0)

            if(area>100000):
                x = cv.GetSpatialMoment(moments,1,0)/area
                y = cv.GetSpatialMoment(moments,0,1)/area

                print 'x: ' + str(x) + ' y: ' + str(y) + ' area: ' + str(area)
                overlay = cv.CreateImage(cv.GetSize(img),8,3)
                cv.Circle(overlay, (int(x), int(y)), 2,(255,255,255), 20)
                cv.Add(img,overlay,img)
                self.objPos = (x,y)
                #cv.Merge(image,None,None,None,img)
                        
            #display the image
            cv.ShowImage("After color filter",thresholded)
            cv.ShowImage(color_tracker_window, img) 
            
            if cv.WaitKey(10) == 27: 
                del(self.capture)
                cv.DestroyAllWindows()
                break     
            
                
##if __name__=="__main__": 
##    color_tracker = ColorTracker() 
##    color_tracker.run()
    
