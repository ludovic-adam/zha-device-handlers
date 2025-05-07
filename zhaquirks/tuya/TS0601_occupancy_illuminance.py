"""Tuya TS0601 occupancy & illuminance sensors"""

from zigpy.quirks.v2 import EntityPlatform
from zigpy.types import t

from zhaquirks.tuya.builder import TuyaQuirkBuilder
from zigpy.zcl.clusters.measurement import OccupancySensing
from zhaquirks.tuya import TuyaLocalCluster

class TuyaOccupancySensing(OccupancySensing, TuyaLocalCluster):
    """Tuya local OccupancySensing cluster."""

class PirState(t.enum8):
    """Pir state"""

    pir = 0x00
    none = 0x01


    @staticmethod
    def to_occupancy(x):
        """ Map PIR state to occupancy enum. Actually the PirState is Occupancy inverted."""

        if x == PirState.pir:
            return OccupancySensing.Occupancy.Occupied
        return OccupancySensing.Occupancy.Unoccupied

(
    TuyaQuirkBuilder("_TZE200_f1pvdgoh", "TS0601")
    .tuya_dp(
        dp_id=1,
        ep_attribute=TuyaOccupancySensing.ep_attribute,
        attribute_name=OccupancySensing.AttributeDefs.occupancy.name,
        converter=PirState.to_occupancy,
    )
    .adds(TuyaOccupancySensing)
    .tuya_illuminance(dp_id=101)
    .tuya_battery(dp_id=4)
    .add_to_registry()
)