import random
from Acspy.Clients.SimpleClient import PySimpleClient

client = PySimpleClient()
db = client.getComponent("DATABASE_S")

from TYPES import (
    Target,
    TargetList,
    Position
)

from astroquery.simbad import Simbad

import numpy as np
from astropy.time import Time
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
import astropy.units as u

import time

from copy import deepcopy


def get_visible_sources():
    sources = [
    "HIP 13847", "HIP 7588", "HIP 60718", "HIP 33579", "HIP 68702", "HIP 95947", "HIP 65477", "HIP 17702", "HIP 21421", "HIP 105199",
    "HIP 1067", "HIP 50583", "HIP 14576", "HIP 31681", "HIP 62956", "HIP 67301", "HIP 9640", "HIP 109268", "HIP 25428", "HIP 26311",
    "HIP 26727", "HIP 46390", "HIP 76267", "HIP 677", "HIP 98036", "HIP 97649", "HIP 2081", "HIP 80763", "HIP 69673", "HIP 25985",
    "HIP 112247", "HIP 87937", "HIP 25336", "HIP 27989", "HIP 96295", "HIP 30438", "HIP 24608", "HIP 746", "HIP 36850", "HIP 63125",
    "HIP 98298", "HIP 102098", "HIP 57632", "HIP 3419", "HIP 54061", "HIP 107315", "HIP 87833", "HIP 113368", "HIP 57939", "HIP 68702",
    "HIP 9884", "HIP 72105", "HIP 24186", "HIP 90185", "HIP 72607", "HIP 110893", "HIP 36208", "HIP 113963", "HIP 59774", "HIP 14135",
    "HIP 53910", "HIP 25930", "HIP 10826", "HIP 5447", "HIP 15863", "HIP 65378", "HIP 25606", "HIP 92855", "HIP 58001", "HIP 17851",
    "HIP 11767", "HIP 37826", "HIP 37279", "HIP 70890", "HIP 84345", "HIP 86032", "HIP 30089", "HIP 49669", "HIP 24436", "HIP 71683",
    "HIP 109074", "HIP 27366", "HIP 113881", "HIP 85927", "HIP 3179", "HIP 92420", "HIP 32349", "HIP 65474", "HIP 97278", "HIP 68756",
    "HIP 77070", "HIP 3829", "HIP 91262", "HIP 63608", "HIP 18543", "HIP 60936"
]
    return deepcopy(sources)

def get_target_coordinates(name):
    simbad = Simbad()
    simbad.add_votable_fields("ra", "dec")
    result = simbad.query_object(name)
    ra = result['ra'][0]
    dec = result['dec'][0]

    observer_lat = 52.52        # Observer latitude (degrees)
    observer_lon = 13.405       # Observer longitude (degrees)
    obs_time = Time.now()       # Current time

    # Observer location
    location = EarthLocation(lat=observer_lat*u.deg, lon=observer_lon*u.deg)

    # Coordinate of the object
    sky_coord = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))

    # Transform to AltAz
    altaz_frame = AltAz(obstime=obs_time, location=location)
    altaz = sky_coord.transform_to(altaz_frame)
    
    print(f"Object: {name}, AZ: {altaz.az.deg}, EL: {altaz.alt.deg}")

    if altaz.alt.deg > 20:
        print(f"Object {name} is visible.")
        return Position(altaz.alt.deg, altaz.az.deg)
    else:
        return None

# def generateProposal(n_proposals=10, last_proposal_id=0):
#     """
#     Generate a list of proposals.
#     """
#     proposals = []
#     sources = get_visible_sources()
#     for i in range(n_proposals):
#         proposal_id = last_proposal_id + i + 1
#         targets = []
#         for j in range(random.randint(4, 10)):
#             # random select a unique source from the sources list
#             name = random.choice(sources)
#             sources.remove(name)

#             target_id = proposal_id * 1000 + j
#             target = Target(
#                 tid = target_id,
#                 coordinates = get_target_coordinates(name),
#                 expTime = random.randint(1, 10)
#             )
#             targets.append(target)
#         proposal = Proposal(
#             pid=proposal_id,
#             targets=TargetList(targets),
#             status=0
#         )
#         proposals.append(proposal)
#     return ProposalList(proposals)

def generateTargets(n_targets=10, last_target_id=0):
    """
    Generate a list of targets.
    """
    targets = []
    sources = get_visible_sources()
    for i in range(n_targets):
        print(f"Generating target {i+1}/{n_targets}...")
        # random select a unique source from the sources list
        name = random.choice(sources)
        sources.remove(name)

        target_id = int(name.split(" ")[-1])
        print(target_id)
        coordinates = get_target_coordinates(name)
        if coordinates is None:
            print(f"Target {name} is not visible.")
            continue
        target = Target(
            tid = target_id,
            coordinates = get_target_coordinates(name),
            expTime = random.randint(1, 10)
        )
        targets.append(target)
        time.sleep(1)
    return targets

# get the latest proposal
# proposal_list = db.getProposals()
# proposal = proposal_list[-1]
# proposal_id = proposal.pid
# add 10 new proposals
for i in range(2):
    target_list = generateTargets(3)
    db.storeProposal(target_list)
