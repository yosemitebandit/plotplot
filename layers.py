'''
layers
breaking down greyscale images
'''
from PIL import Image

inputImage = 'samples/portrait.jpg'   #  925 x 617
im = Image.open(inputImage)

grey = im.convert('L')
grey.show()
pixels = list(grey.getdata())
print pixels 
print len(pixels)

print grey.mode

images = {}
for percentile in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
    images[percentile] = []
    percentile_append = images[percentile].append
    
    threshold = 255-255*percentile/100
    print threshold
    for p in pixels:
        if p < threshold:
            percentile_append(p)
        else:
            percentile_append(0)

    # make a new image
    i = Image.new('L', (925, 617))
    # putdata for this array
    i.putdata(images[percentile])
    # show
    i.show()
    # save

