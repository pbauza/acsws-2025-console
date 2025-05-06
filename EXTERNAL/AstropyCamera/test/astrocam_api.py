import time

import numpy as np
import matplotlib.pyplot as plt

from astrocam.api import AstrocamAPI
from astropy.visualization import simple_norm

def main():
    a = AstrocamAPI()

    # RA/DEC Object
    #object_name = "M51"
    #coord = a.resolve_object(object_name)
    #image = a.fetch_sky_image(coord)
    #a.plot_fits_image(image)

    height = 500
    width = 500
    image = a.fetch_sky_image_altazm(21.884329270053367, 169.68496421793208)[0].data
    #a.plot_fits_image(image)

    plt.figure(figsize=(8, 8))
    plt.imshow(image)
    plt.colorbar()
    plt.show()


    print(image.shape)
    norm = simple_norm(image, stretch='linear')
    ndata = norm(image)
    img_data = (ndata * 255).astype(np.uint8).tobytes()

    img = np.frombuffer(img_data, dtype=np.uint8).reshape((height, width))
    plt.figure(figsize=(8, 8))
    plt.imshow(img)
    plt.colorbar()
    plt.show()



if __name__ == "__main__":
    main()
