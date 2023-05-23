## Day 2 session 1

## Task 1 - Skew Correction
 
### Step 1 - Pre-Processing
- read the image
- convert the image to grayscale
- blur the image using gaussian blur to reduce noise
- apply a denoising algorithm (N1means)
- apply binary thresholding

### Step 2 - Canny Edge detection

### Step 3 - Line detection using Hough transforms
- apply hough transform to get all the lines
- filter all the peak lines

### step 4 - Skew Detection (getting the most dominant line)
- find the dominant angle by doing a mode of all the angles and 
picking the angle with the maximum mode

### Step 5 - convert the image by rotating by skew-angle
- rotate the image by the skew angle
