from ..skills import Skill, PEERLESS_HEROINE, MC_ULT

DEFAULT_ULT = Skill(
    "Ultimate Pass",
    "Gain insane velocity at the second half of the race, when in second place",
    0,
    (
        (
            "self",
            {
                "vel": 16
            }
        ),
    ),
    1,
    lambda v, race: v.order_rate >= 50 and v.placement == 2,
    type="Ult",
    icon="yellow_ult"
)
