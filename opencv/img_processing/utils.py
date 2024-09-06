from matplotlib import pyplot as plt
import cv2


def show_img(*imgs, scale=1, axis="off") -> None:
    """
    Shows the images in scale and correct color.
    Args:
        imgs: Images
        scale: Take larger numbers for smaller images
        axis: on/off the axis around the img
    Returns:
        None. Just shows the images.
    """
    ncols = len(imgs)
    plt.figure(figsize=(20//scale, 24//scale))
    for i, img in enumerate(imgs, start=1):
        plt.subplot(1, ncols, i)
        img = img[..., ::-1] if len(img.shape) == 3 else img
        plt.imshow(img, cmap="gray")
        plt.axis(axis)
    plt.tight_layout()
    plt.show()

def show_hist(pic, limY=None, limX=(0, 256), mask=None) -> None:
    """
    Calculates the color histograms of the image.
    Args:
        pic (np.ndarray): Image
        limY (tuple): Limits of the y axis
        limX (tuple): Limits of the x axis
        mask (np.ndarray): Masked area
    Returns:
        None. Just shows the histogram graphs.
    """
    if len(pic.shape) == 3:
        color_list = ["b", "g", "r"]
    elif len(pic.shape) == 2:
        color_list = ["black"]

    for i, c in enumerate(color_list):
        picture_hist = cv2.calcHist(
            images=[pic],
            channels=[i],
            mask=mask,
            histSize=[256],
            ranges=[0,256])
        plt.plot(picture_hist, color=c)
        plt.xlim(limX)
        plt.ylim(limY)
        plt.grid(b=True, color="lightgray", linestyle=(0, (5, 10)))
