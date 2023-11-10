import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
   
def colour_mask(img, lower_colour, upper_colour):
    mask = cv2.inRange(img, lower_colour, upper_colour)
    masked = cv2.bitwise_and(img,img, mask=mask)
    return masked

def colour_filter(img, lower_colour, upper_colour):
    mask = cv2.inRange(img, lower_colour, upper_colour)
    masked = cv2.bitwise_and(img,img, mask=mask)
    result = img - masked
    return result

def colour_histogram(img):
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.show()

def detect_lines(img):
    edges = cv2.Canny(img,50,150,apertureSize = 3)
    display_image(edges)
    
    minLineLength=5
    maxLineGap=5
    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=200,lines=np.array([]), minLineLength=minLineLength,maxLineGap=maxLineGap)

    a,b,c = lines.shape
    for i in range(a):
        cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
        display_image(edges)


# Rotates on multiples of 90 degrees
# cv2.ROTATE_90_CLOCKWISE
# cv2.ROTATE_180
# cv2.ROTATE_90_COUNTERCLOCKWISE
def rotate(img, rot):
    return cv2.rotate(img, rot)

# Scales the image maintaining aspect ratio
# cv2.INTER_NEAREST
# cv2.INTER_LINEAR
# cv2.INTER_CUBIC
# cv2.INTER_AREA
def uniform_scale(img, factor, interp=cv2.INTER_NEAREST):
    scaled_resolution = (img.shape[0] * factor, img.shape[1] * factor)
    print(scaled_resolution)
    return cv2.resize(img, scaled_resolution, interpolation=interp)

# Scales the image using seperate scaling factors for each dimension
# cv2.INTER_NEAREST
# cv2.INTER_LINEAR
# cv2.INTER_CUBIC
# cv2.INTER_AREA
def scale(img, x_factor, y_factor, interp=cv2.INTER_NEAREST):
    scaled_resolution = (int(img.shape[0] * x_factor), int(img.shape[1] * y_factor))
    print(scaled_resolution)
    return cv2.resize(img, scaled_resolution, interpolation=interp)

# Adds guassian noise to image according to parameters
def guassian_noise(img, strength=1, mean=0, variance=400):
    gauss = np.random.normal(mean, variance**0.5, img.shape)
    gauss = gauss.reshape(img.shape)
    noisy = img + gauss * 2
    noisy = np.clip(noisy, 0, 255)
    noisy = noisy.astype(np.uint8)
    return noisy

# Adds salt and pepper noise ot image
# ratio of salt to pepper (higher ration -> more salt)
# single channel or B & W
def salt_pepper_noise(img, ratio=0.5, freq=0.05, b_w=False):
    noisy = np.copy(img)
    amount = int(freq * img.shape[0] * img.shape[1] * img.shape[2])
    salt = int(ratio * amount)

    for i in range(amount):
        coord = [np.random.randint(0, i) for i in img.shape]
        if i <= salt:
            if b_w:
                noisy[coord[0]][coord[1]] = [255 for i in img.shape[2]]
            else:
                noisy[coord[0]][coord[1]][coord[2]] = 255
        else:
            if b_w:
                noisy[coord[0]][coord[1]] = [0 for i in img.shape[2]]
            else:
                noisy[coord[0]][coord[1]][coord[2]] = 0
    return noisy

# Mix images using linear ratio
def mix_images(img, img2, ratio=0.2):
    return (img * ratio).astype(np.uint8) + (img2 * (1 - ratio)).astype(np.uint8)

# Insert image at coordinates (no mixing/blending)
def insert_image(img, img2, x, y):
    result = np.copy(img)
    print(img2.shape)
    result[y: y + img2.shape[1], x: x + img2.shape[0]] = img2
    return result

# Blend image into another using transparency 
### TODO slow
def blend_images(img, img2, x, y):
    result = np.copy(img)
    for j in range(img2.shape[1]):
        for i in range(img2.shape[0]):
            ### TODO use transparency as proportionate ratio
            if img2[j, i, 3] != 0:
                result[j + y, i + x] = img2[j, i]
    return result

# Set specific colour to transparent
def remove_colour(img, r, g, b, a):
    result = np.copy(img)
    cells = np.where(np.all(img == [b, g, r, a], axis=-1))
    result[cells[0], cells[1], :] = [b, g, r, 0]
    return result

# Set specific colour range to transparent
def remove_colour_range(img, c1, c2):
    mask = cv2.inRange(img, c1, c2) # create the Mask
    mask = 255 - mask  # inverse mask
    return cv2.bitwise_and(img, img, mask=mask)

# Load image from file
# cv2.IMREAD_COLOR
# cv2.IMREAD_GRAYSCALE 
# cv2.IMREAD_UNCHANGED
def load_image(path, colourspace=cv2.IMREAD_COLOR):
    img = cv2.imread(path, colourspace)
    return convert_colourspace(img)

def load_dir(path):
    imgs = []
    for filename in os.listdir(path):
        img_path = os.path.join(path, filename)
        imgs.append(load_image(img_path))
    return imgs

# NOTE: images are BGR
def display_image(img):
    plt.imshow(img)
    plt.show()

# cv2.COLOR_BGR2RGB
# cv2.COLOR_RGB2BGR
def convert_colourspace(img, conversion=cv2.COLOR_RGB2BGRA):
    return cv2.cvtColor(img, conversion)

if __name__ == "__main__":
    cwd = os.getcwd()
    bricks_dir = os.path.join(cwd, "bricks")
    bg_dir = os.path.join(cwd, "backgrounds")

    brick_imgs = load_dir(bricks_dir)
    bg_imgs = load_dir(bg_dir)

    test_img = brick_imgs[0]
    test_img2 = brick_imgs[1]

    display_image(test_img)
    display_image(test_img2)

    display_image(rotate(test_img, cv2.ROTATE_90_CLOCKWISE))
    display_image(uniform_scale(test_img, 2, cv2.INTER_NEAREST))
    display_image(scale(test_img, 2, 0.5, cv2.INTER_NEAREST))

    display_image(guassian_noise(test_img, 2))
    # display_image(salt_pepper_noise(test_img))
    # display_image(salt_pepper_noise(test_img, b_w=True))

    display_image(mix_images(test_img, test_img2))
    scaled_test2_img = scale(test_img2, 0.5, 0.5)
    display_image(insert_image(test_img, scaled_test2_img, 100, 100))

    colour_histogram(test_img)

    bg_remove = remove_colour(test_img, 70, 70, 70, 255)
    bg_remove = remove_colour(bg_remove, 71, 71, 71, 255)
    display_image(bg_remove)

    bg_rem = remove_colour_range(test_img, (70, 70, 70, 255), (72, 72, 72, 255))
    display_image(blend_images(bg_imgs[0], bg_rem, 100, 100))

