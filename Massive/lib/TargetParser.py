"""
TargetParser.py
Orf 2012
"""

import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
from collections import namedtuple
import datetime
import re

WeightResult = namedtuple("weightmatch","weight_start weight_end weight_values remaining_text")

class InvalidText(Exception):
    pass

class DateInvalid(Exception):
    pass

WeightConversions = {
    "pounds":lambda x: x*0.45,
    "kilograms":lambda x:x,
    "stone":lambda x:x*6.35,
}


class Weight(object):
    """ I store the weight in Kilograms and convert from other sources """
    def __init__(self):
        self.weight = 0

    def AddWeight(self, weight_type, value):
        self.weight += WeightConversions[weight_type](float(value))

    def __repr__(self):
        return "<Weight: %s kg>"%self.weight

    def __str__(self):
        return repr(self)


class TargetParser(object):
    """
    I'm a TargetParser. I take in human text through my .Parse() method and process it into a Target
    I understand these weights:
        * Kilogram
        * Stone
        * Pounds

    Input should loosely be in this format:
        WEIGHT_VALUE [(WEIGHT_LINK) WEIGHT_VALUE ] (LINK) DATE_TIME

    E.g:
        12 stone and 2 pounds in 3 months and 12 days
        6 kilograms in the next 30 days
        14 pounds within a month
        10 kilograms by a month on thursday

    Assumptions:
        All users can spell
        All users use digits instead of human words for numbers (for now, wouldn't be hard to change)
        All users are english
        The first number in the input string is the amount of
    """

    LINK = ("by","in the next","in")
    WEIGHT_VALUE = ("kilo(gram|)(s|)","stone","pound(s|)")
    WEIGHT_LINK = ("and",)

    _weight_regex = re.compile("(?P<value>\d+(.\d)?) (?P<weight>(%s))"%("|".join(["(%s)"%val for val in WEIGHT_VALUE])))


    def __init__(self):
        self.parser = pdt.Calendar(pdc.Constants())


    def ExtractSingleWeight(self, text):
        match = self._weight_regex.match(text)
        if not match: return None

        rest_of_string = text[match.end():].strip()

        return WeightResult(match.start(), match.end(),
                            match.groupdict(), rest_of_string.strip())


    def GetTotalWeightFromString(self, string):

        total_weight = Weight()

        first_weight = self.ExtractSingleWeight(string)
        if first_weight is None:
            raise InvalidText()

        total_weight.AddWeight(first_weight.weight_values["weight"], first_weight.weight_values["value"])

        new_string = first_weight.remaining_text

        if new_string.startswith(self.WEIGHT_LINK):
            for prefix in self.WEIGHT_LINK:
                new_string = new_string.lstrip(prefix).strip()

        second_weight = self.ExtractSingleWeight(new_string)
        if second_weight:
            total_weight.AddWeight(second_weight.weight_values["weight"], second_weight.weight_values["value"])
            new_string = second_weight.remaining_text

        return new_string, total_weight


    def GetDateFromString(self, string):
        result, code = self.parser.parse(string)
        if not code == 1:
            raise DateInvalid()


    def Parse(self, text):
        text = text.lower().strip()
        print text
        string, weight = self.GetTotalWeightFromString(text)
        print weight
        print self.GetDateFromString(string)


