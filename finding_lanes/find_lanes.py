import cv2

image = cv2.imread('./road_test.jpg')
cv2.imshow('road', image)
cv2.waitKey(0)
