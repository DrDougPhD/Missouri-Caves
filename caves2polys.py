import csv
import os
import urllib
import sys
import xml.etree.ElementTree as ET
import simplekml
trs2latlong_url = r"http://www.geocommunicator.gov/TownshipGeocoder/TownshipGeocoder.asmx/GetLatLonFeed?TRS="


def get_TRS_string(cave):
    aliquot_parts = cave['Section Division'].split()
    aliquot_parts.reverse()
    geocomm_compliant_aliquot_parts = []
    for p in aliquot_parts:
        # If the Aliquot Part is listed as a 1/2 sector and not a quarter sector, it could screw things up.
        if len(p) == 2:
          geocomm_compliant_aliquot_parts.append(p)
        
        # L stands for lot.
        elif p[0] == 'L':
          geocomm_compliant_aliquot_parts.append(p)
        
        # If the Aliquot Part is N, S, E, or W, then it is a half sector and would probably break GeoCommunicator.
        elif p[0] == 'N' or p[0] == 'S' or p[0] == 'E' or p[0] == 'W':
          break

    geocomm_compliant_aliquot_parts.reverse()
    cave['Section Division'] = "".join(geocomm_compliant_aliquot_parts)
    
    # More info: http://www.blm.gov/nils/GeoComm/documents/NILS_GeoCommunicator_Web_Services_TGC_Formats.pdf
    return "{State},{Principal Meridian Code},{Township Number},{Township Fraction},{Township Direction},{Range Number},{Range Fraction},{Range Direction},{Section},{Section Division},{Township Duplicate}".format(**cave)


def get_centroid_coords(cave):
    centroid = cave[0][1][4].text.split()
    return centroid


def get_cave_poly(cave):
    points = cave[0][2][4].text.split(",")
    coords = zip(points[::2], points[1::2])
    return [(c[1], c[0]) for c in coords]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: not enough cli arguments. Please provide the input CSV to be processed.")
        print(" $ python {0} /path/to/cave.csv".format(sys.argv[0]))
        exit()

    caves = []
    path = sys.argv[1]
    with open(path) as f:
        bretz_data = csv.DictReader(f)
        for c in bretz_data:
            cave = dict(c)
            cave['TRS'] = get_TRS_string(cave)
            caves.append(cave)

    kml = simplekml.Kml()
    for c in caves:
        print("Getting info on {Cave name}".format(**c))
        georss_url = trs2latlong_url + c['TRS']
        georss_str = urllib.urlopen(georss_url).read()
        georss_xml = ET.fromstring(georss_str)

        centroid = get_centroid_coords(georss_xml)
        poly = get_cave_poly(georss_xml)

        kml.newpoint(name=c['Cave name'], description=c['Description'], coords=[centroid])
        estimated_location = kml.newpolygon(name=c['Cave name'])
        estimated_location.outerboundaryis = poly
        estimated_location.style.polystyle.fill = 0

    kml.save(os.path.basename(sys.argv[1]) + ".kml")
