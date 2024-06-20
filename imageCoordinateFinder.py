from PIL import Image
import matplotlib.pyplot as plt

# Load an image
image = Image.open('./emptybill.png')
plt.imshow(image)
plt.title('Click on the image to get coordinates')
plt.axis('on')  # Show axes with ticks

# Function to handle click event
def onclick(event):
    ix, iy = event.xdata, event.ydata
    print('Coordinates:', ix, iy)

# Connect the click event to the handler
fig = plt.gcf()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
