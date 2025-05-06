import numpy as np

from astroquery.simbad import Simbad
from astroquery.skyview import SkyView

import astropy.units as u
from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.visualization import simple_norm
import matplotlib.pyplot as plt

class AstrocamAPI:
    LAT=51.2993
    LON=9.491
    ALT=0
    FOV = 0.2
    ASPECT = [1920, 1080]
    PIXELS = [1920, 1080]
    def __init__(self, fov=FOV, aspect=ASPECT, pixels=PIXELS):
        SkyView.TIMEOUT = 10
        self.simbad = Simbad()
        self.simbad.add_votable_fields("ra", "dec")
        self.location = EarthLocation(lat=AstrocamAPI.LAT*u.deg, lon=AstrocamAPI.LON*u.deg, height=AstrocamAPI.ALT*u.m)
        self.w_fov = fov * (aspect[0] / aspect[1]) * u.deg
        self.h_fov = fov * u.deg
        self.pixels = [int(x / 5) for x in pixels]

    def resolve_object(self, name):
        result = self.simbad.query_object(name)
        ra = result['ra'][0]
        dec = result['dec'][0]
        coord = SkyCoord(ra, dec, unit='deg')
        return coord

    def fetch_sky_image(self, coord, survey="DSS"):
        #images = SkyView.get_images(position=coord, survey=[survey], pixels=self.pixels, radius=self.h_fov)
        images = SkyView.get_images(position=coord, survey=[survey], pixels=self.pixels, width=self.w_fov, height=self.h_fov)
        return images[0]

    def fetch_sky_image_altazm(self, alt, azm, survey="DSS"):
        obstime = Time.now()
        altazm = AltAz(alt=alt*u.deg, az=azm*u.deg, obstime=obstime, location=self.location)
        coord = SkyCoord(altazm).transform_to('icrs')
        return self.fetch_sky_image(coord, survey)

    def retrieve_raw_image(self, alt, azm):
        data = self.fetch_sky_image_altazm(alt, azm)[0].data
        norm = simple_norm(data, stretch='linear')
        ndata = norm(data)
        return (ndata * 255).astype(np.uint8).tobytes()

    def plot_fits_image(self, hdu):
        data = hdu[0].data
        norm = simple_norm(data, 'sqrt', percent=99)

        plt.figure(figsize=(8, 8))
        plt.imshow(data, cmap='gray', origin='lower', norm=norm)
        plt.colorbar()
        plt.show()
