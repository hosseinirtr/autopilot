
import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('./road_test.jpg')
lane_img = np.copy(image)


# In[3]:


def make_coordinates(image,line_parameters):
    slope , intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])
    


# In[4]:


def acerage_slope_intercepr(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parametrs = np.polyfit((x1,x2),(y1,y2),1)
        slope = parametrs[0]
        intercept = parametrs[1]
#         print('slope',slope,'intercept',intercept)
        if slope < 0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average = np.average(left_fit,axis=0)
    right_fit_average = np.average(right_fit,axis=0)
#     print('left fit is {} '.format(left_fit))
#     print('right fit is {}'.format(right_fit))
#     print('left fit average is {} '.format(left_fit_average))
#     print('right fit average is {}'.format(right_fit_average))
    left_line = make_coordinates(image,left_fit_average)
    right_line = make_coordinates(image,right_fit_average)
#     print("right_line",right_line)
#     print("left_line",left_line)
    return np.array([left_line,right_line])
            


# In[5]:


def canny(img):
    gray = cv2.cvtColor(lane_img,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur,50,150)
    return canny



# In[6]:


def display_lines(img,lines):
    line_img = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(line_img,(x1,y1),(x2,y2),(255,10,0),20)
    return line_img
#             print([x1,y1,x2,y2])


# In[7]:


def region_of_interst(image):
    height = image.shape[0]
    polygons = np.array([
        [(200,height),(1100,height),(550,250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    masked_img = cv2.bitwise_and(image,mask)
    return masked_img



# In[8]:


# lane_img = np.copy(image) 
# canny_img = canny(lane_img)
# cropped_img = region_of_interst(canny_img)
# lines = cv2.HoughLinesP(cropped_img,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
# averaged_lines = acerage_slope_intercepr(lane_img,lines)
# line_img = display_lines(lane_img,averaged_lines)
# combo_img = cv2.addWeighted(lane_img,0.8, line_img,1,1)
# cv2.imshow('road', combo_img)
# cv2.waitKey(0)


# In[9]:
cap = cv2.VideoCapture('./test2.mp4')
while (cap.isOpened()):
    _, frame = cap.read()
    canny_frame = canny(frame)
    cropped_frame = region_of_interst(canny_frame)
    lines = cv2.HoughLinesP(cropped_frame,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
    averaged_lines = acerage_slope_intercepr(frame,lines)
    line_frame = display_lines(frame,averaged_lines)
    combo_frame = cv2.addWeighted(frame,0.8, line_frame,1,1)
    cv2.imshow('road', combo_frame)
    
#     v2 ->
#     lane_img = frame
#     canny_img = canny(lane_img)
#     cropped_img = region_of_interst(canny_img)
#     lines = cv2.HoughLinesP(cropped_img,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
#     averaged_lines = acerage_slope_intercepr(lane_img,lines)
#     line_img = display_lines(lane_img,averaged_lines)
#     combo_img = cv2.addWeighted(lane_img,0.8, line_img,1,1)
#     cv2.imshow('road', combo_img)
#     cv2.waitKey(0)
    
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
