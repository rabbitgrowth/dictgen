import re
from dataclasses import dataclass
from typing import Optional, Set, Union

from chords import LEFT_CHORDS, MID_CHORDS, RIGHT_CHORDS

LEFT_AND_RIGHT_CHORDS = LEFT_CHORDS | RIGHT_CHORDS

@dataclass
class Sound:
    ipa:      Optional[Union[str, Set[str]]] = None
    spell:    Optional[Union[str, Set[str]]] = None
    stressed: Optional[bool]                 = None
    cont:     Optional[bool]                 = None

    @classmethod
    def from_ipa(cls, ipa):
        vowel = re.match(r'([aɑɛɪɔoɵʉʌə])(\u0301?)([ːjw]?)', ipa)
        if vowel:
            first, stress, second = vowel.groups()
            ipa = first + second
            stressed = bool(stress)
        else:
            stressed = False
        return cls(ipa, stressed=stressed)

    def is_vowel(self):
        assert self.ipa is not None
        return self.ipa in MID_CHORDS

    def is_consonant(self):
        assert self.ipa is not None
        return self.ipa in LEFT_AND_RIGHT_CHORDS

    def __eq__(self, other):
        if not isinstance(other, Sound):
            return NotImplemented
        for attr in self.__annotations__:
            self_attr  = getattr(self,  attr)
            other_attr = getattr(other, attr)
            if self_attr is None or other_attr is None:
                continue
            if isinstance(other_attr, set):
                return NotImplemented
            if isinstance(self_attr, set):
                if other_attr not in self_attr:
                    return False
            else:
                if self_attr != other_attr:
                    return False
        else:
            return True

START = Sound('^')
BREAK = Sound('.')
END   = Sound('$')
