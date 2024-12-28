"""
Name-US: CV-Apply Weights To Selection
Description-US: Apply the current strength Weights to your component selection
"""

import c4d
from c4d import gui
#Welcome to the world of Python


def main():

    c4d.modules.character.CAWeightMgr.ApplyWeightFunction(doc)
    c4d.EventAdd()

if __name__=='__main__':
    main()