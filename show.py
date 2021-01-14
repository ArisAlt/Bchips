from matplotlib import pyplot as plt

class Show:

    def __init__(self, image1, image2) -> None:
         self.res = image1
         self.src = image2

    def image_show(self):
    
        plt.subplot(121),plt.imshow(self.res,cmap = 'gray')
        plt.title('Image 1 '), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(self.src,cmap = 'gray')
        plt.title('Image 2 '), plt.xticks([]), plt.yticks([])
        plt.suptitle("hello")
        plt.show()

    def detect_show(self):
        pass