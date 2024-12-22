import re
from dataclasses import dataclass
from typing import Optional, Set, Union

from chords import MID_CHORDS

@dataclass
class Sound:
    ipa:      Optional[Union[str, Set[str]]] = None
    stressed: Optional[bool]                 = None
    spelled:  Optional[Union[str, Set[str]]] = None

    @classmethod
    def from_ipa(cls, ipa):
        vowel = re.match(r'([aɑɛɪɔoɵʉʌə])(\u0301?)([ːjw]?)', ipa)
        if vowel:
            first, stress, second = vowel.groups()
            ipa = first + second
            stressed = bool(stress)
        else:
            stressed = False
        return cls(ipa, stressed)

    def is_vowel(self):
        assert self.ipa is not None
        return self.ipa in MID_CHORDS

    def stronger_than(self, other):
        assert self.stressed  is not None
        assert other.stressed is not None
        return self.stressed and not other.stressed

    def __eq__(self, other):
        if not isinstance(other, Sound):
            return NotImplemented
        for attr in ['ipa', 'stressed', 'spelled']:
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

BREAK = Sound('.')
