# Image Processing Bot
 ##### Using Tesseract OCR, OpenCV and Discord API
 
This bot performs image processing on images submitted in a discord server via asynchronous functions which listen for such events. The bot will save the image, perform some image processing to prepare it for OCR using PyTesseract, perform OCR and brute-force the best output based on a different image processing methods, then perform autocorrect on the character output in order to clean the data. The autocorrected data is then processed in order to assign a point value to the text from the image, and post the image, what it has read, and the amount of points back to discord for the user to enter into a database.
 
