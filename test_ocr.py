import cv2
import numpy as np
import pytesseract
import os

filename = os.path.join('namecard', '03.jpg')
img = cv2.imread(filename)

# TODO: Pre-Processing
img99 = img
# img99 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Tesseract OCR
d = pytesseract.image_to_data(img99, output_type=pytesseract.Output.DICT)
data_list = []
for key in d.keys():
    data_list.append(d.get(key))
print(str(d['text']))

# Make Dictionary of Key
key_dictionary = {i: list(d.keys())[i] for i in range(0, len(d.keys()))}
key_dictionary = {x: i for i, x in key_dictionary.items()}

# Find Empty Text
empty_list = []
for x in range(len(data_list[11])):
    if data_list[11][x].replace(' ', '') == '':
        empty_list.append(x)

# Delete Empty Text
empty_list.reverse()
for x in empty_list:
    for row in data_list:
        del row[x]

# Sort Based on LEFT
temp = np.array(data_list).T
temp = temp[temp[:, 7].argsort()]
data_list_new = temp.T.tolist()

# Sort Based on TOP
temp = np.array(data_list_new).T
temp = temp[temp[:, 7].argsort()]
data_list_new = temp.T.tolist()

# List of Tuple (left, top) => (x, y)
coordinate_list = []
for x in range(len(data_list[0])):
    coordinate_list.append((data_list[6][x], data_list[7][x]))
# print(coordinate_list)

# List of Tuple (width, height)
size_list = []
for x in range(len(data_list[0])):
    size_list.append((data_list[8][x], data_list[9][x]))
# print(size_list)

# # Find Sentences
# for x in range(len(data_list_new[0])):
#     for y in (i for i in np.arange(len(data_list_new[0])) if i != x):
#         print(x, y)

# Concat Sentences
sentences = []
counter = 1
temp_sentence = data_list[11][0]
while counter < len(data_list[0]):
    if abs(data_list[7][counter]-data_list[7][counter-1]) < 2:
        temp_sentence = temp_sentence + ' ' + data_list[11][counter+1]
    else:
        sentences.append(temp_sentence)
        try:
            temp_sentence = data_list[11][counter]
        except IndexError:
            break
    counter = counter + 1
print(sentences)

# Print
for x in range(len(data_list)):
    print(list(d)[x])
    print(data_list[x])

# new_d = [x for x in d['text'] if x.replace(' ', '') != '']
# print(new_d)

h, w, c = img99.shape
boxes = pytesseract.image_to_boxes(img99)
for b in boxes.splitlines():
    b = b.split(' ')
    img99 = cv2.rectangle(img99, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# TODO: Threshold or Plot the Color Composition of an Image
crop = img[114:439, 39:487]
crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
# crop = cv2.adaptiveThreshold(crop, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
_, crop = cv2.threshold(crop, 100, 255, cv2.THRESH_BINARY)  # | cv2.THRESH_OTSU)
res = pytesseract.image_to_string(crop)
print('Result: ' + str(res) + '!!!')

cv2.imshow('Image', img99)
cv2.imshow('Crop', crop)
# cv2.imshow('Result', img_result)
key = cv2.waitKey(0)



