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
    sources = ['HIP 32349', 'HIP 27989', 'HIP 24961']
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

    return Position(altaz.alt.deg, altaz.az.deg)

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

        target_id = last_target_id + i + 1
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
for i in range(10):
    target_list = generateTargets(3)
    db.storeProposal(target_list)
