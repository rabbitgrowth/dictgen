from plover_stroke import BaseStroke

class Stroke(BaseStroke):
    pass

Stroke.setup(
    '# S- T- K- P- W- H- R- A- O- * -E -U -F -R -P -B -L -G -T -S -D -Z'.split(),
    'A- O- * -E -U'.split(),
)

LEFT_BANK  = Stroke('STKPWHR')
MID_BANK   = Stroke('AOEU')
RIGHT_BANK = Stroke('-FRPBLGTSDZ')
