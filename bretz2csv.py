import sys
import os
from pyparsing import *
import csv


def parse_cave_details(details):
    ##########################################################################
    # Define the Bretz Grammar.
    # Sample cave description:
    # Boring Caverns SE1/4 NW1/4 sec. 16, T. 37 N., R. 10 W., Pulaski County Not shown on Waynesville Quadrangle map The mouth of this cave ...\n
    # Another Cave S1/2 sec. 15, T. 36 N., R. 12 W., Pulaski County Not shown on Waynesville Quadrangle map There are two large caves...\n
    # Something Bridge Sec. 15 or 22, T. 36 N., R. 13 W., Pulaski County Not shown on Richland Quadrangle map This cave is near Ozark...\n
    #
    #  CAVE ::= CAVE_NAME [ALIQUOT_PART] SECTION, TOWNSHIP, RANGE, COUNTY QUAD_MAP DESCRIPTION
    #  ALIQUOT_PART ::= (((NE|SE|SW|NW)1/4)|((N|E|S|W)1/2))*
    #  SECTION ::= (S|s)ec. num+
    #  TOWNSHIP ::= T. num+ TOWNSHIP_DIR.
    #  TOWNSHIP_DIR ::= N|S
    #  RANGE ::= R. num+ RANGE_DIR.
    #  RANGE_DIR ::= E|W
    #  COUNTY = WORD+ County
    #  QUAD_MAP = (Not s|S)hown on QUAD Quadrangle map
    #  QUAD = WORD+
    #  DESCRIPTION = WORD+
    aliquotQuadrantID = Literal("NE") |\
                        Literal("SE") |\
                        Literal("SW") |\
                        Literal("NW")
    aliquotQuadrantString = aliquotQuadrantID + Suppress("1/4")
    aliquotHalfString = oneOf("N E S W") + Suppress("1/2")
    aliquotPart = Group(ZeroOrMore(aliquotQuadrantString | aliquotHalfString))\
                  .setResultsName("aliquot")\
                  .setParseAction(lambda kwd: " ".join(kwd[0]))

    sectionToken = Suppress(oneOf("S s") + Literal("ec") + Optional("."))
    sectionNumber = Word(nums)
    section = Group(
      sectionToken \
      + sectionNumber \
      + ZeroOrMore(Suppress("or") + sectionNumber)
    ).setResultsName("section")

    afterEndOfCaveName = aliquotHalfString | aliquotQuadrantString | sectionToken
    caveName = Group(OneOrMore(~afterEndOfCaveName + Word(printables)))\
               .setResultsName('name')\
               .setParseAction(lambda name: " ".join(name[0]))

    townshipDirection = oneOf("N S").setResultsName("direction")
    townshipNumber = Word(nums).setResultsName("number")
    township = Suppress("T.") \
             + Group(townshipNumber + townshipDirection).setResultsName("township")\
             + Suppress('.')

    rangeDirection = oneOf("E W").setResultsName("direction")
    rangeNumber = Word(nums).setResultsName("number")
    range_info = Suppress("R.") \
               + Group(rangeNumber + rangeDirection).setResultsName("range")\
               + Suppress('.')

    countyKeyword = Literal("County")
    countyName = Group(OneOrMore(~countyKeyword + Word(alphas+"-'.")))\
                 .setResultsName("county")\
                 .setParseAction(lambda c: " ".join(c[0]))
    county = countyName + Suppress("County")

    notShownOnQuad = (Literal("Not") + Suppress("s"))\
                     .setParseAction(lambda x: False)
    shownOnQuad = Literal("S").setParseAction(lambda x: True)
    onKeyword = Literal("on")
    mapAlias = Group(OneOrMore(~onKeyword + Word(printables)))\
               .setParseAction(lambda alias: " ".join(alias[0]))\
               .setResultsName("alias")
    quadrangleStatus = (shownOnQuad | notShownOnQuad).setResultsName("is_on_map")\
                     + Suppress("hown") \
                     + Optional(Suppress('as') + mapAlias)\
                     + Suppress(onKeyword)
    quadrangleKeyword = Literal("Quadrangle") + Literal("map")
    quadrangleName = Group(OneOrMore(~quadrangleKeyword + Word(alphas+"-'.")))\
                     .setResultsName("name")\
                     .setParseAction(lambda name: " ".join(name[0]))
    quadrangle = Group(quadrangleStatus + quadrangleName).setResultsName("quad") \
               + Suppress(quadrangleKeyword)

    description = Group(ZeroOrMore(Word(alphanums + printables)))\
                  .setResultsName("description")\
                  .setParseAction(lambda desc: " ".join(desc[0]))

    location = caveName \
             + aliquotPart \
             + section + Suppress(',') \
             + township + Suppress(',') \
             + range_info + Suppress(',')\
             + county \
             + quadrangle \
             + description

    return location.parseString(details)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: pass in the filename as the second argument.")
        print(" $ python {0} /path/to/file.txt".format(sys.argv[0]))
        exit()

    filepath = sys.argv[1]
    with open(filepath) as f:
        raw_text = f.read()

    raw_caves = raw_text.split("\n")
    caves = []
    for raw_cave_text in raw_caves:
        raw_cave_text = raw_cave_text.strip()
        if raw_cave_text:
            try:
                cave = parse_cave_details(raw_cave_text)
                caves.append({
                    'Cave name': cave.name,
                    'Alias': cave.quad.alias,
                    'On map': cave.quad.is_on_map,
                    'Quad': cave.quad.name,
                    'County': cave.county,
                    'State': 'MO',
                    'Principal Meridian Code': 5,
                    'Township Number': cave.township.number,
                    'Township Fraction': 0,
                    'Township Direction': cave.township.direction,
                    'Range Number': cave.range.number,
                    'Range Fraction': 0,
                    'Range Direction': cave.range.direction,
                    'Section': cave.section[0],
                    'Section Division': "".join(cave.aliquot),
                    'Township Duplicate': 0,
                    'Description': raw_cave_text,
                })

            except:
                print("="*80)
                print("ERROR: unexpected format for {0}".format(cave.name))
                print(raw_cave_text)
                import traceback
                print(traceback.format_exc())
                print("\t" + "\n\t".join([str(x) for x in sys.exc_info()]))
                print("Skipping this cave for the next one")
            else:
                sections = " or ".join(cave.section)
                #print("="*80)
                #print("{1} := {0.aliquot} Sect. {2}, T. {0.township.number} {0.township.direction}., R. {0.range.number} {0.range.direction}., in {0.county} County on the {0.quad.name} quad map.".format(cave, cave.name, sections))
                #print("   Marked on map as {0}".format(cave.quad.alias if cave.quad.alias else cave.name) if cave.quad.is_on_map else "   Not on map")

    output_path = os.path.basename(filepath).split(".")[0] + ".csv"
    print("#"*80)
    print("{0} caves processed! Saving to '{1}'.".format(len(caves), output_path))
    with open(output_path, 'wb') as f:
        cave_csv = csv.DictWriter(f, fieldnames=caves[0].keys())
        try:
          cave_csv.writeheader()
          
        except: # Versions before 2.7 of Python do not have csv with writeheader().
          header = {}
          for k in caves[0].keys():
            header[k] = k
          
          cave_csv.writerow(header)

        cave_csv.writerows(caves)
