from esphome.components import cover
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import (
    CONF_OUTPUT_ID,
    CONF_MIN_VALUE,
    CONF_MAX_VALUE,
)
from .. import tuya_ns, CONF_TUYA_ID, Tuya

DEPENDENCIES = ["tuya"]

CONF_POSITION_DATAPOINT = "position_datapoint"
CONF_INVERT_POSITION = "invert_position"

TuyaCover = tuya_ns.class_("TuyaCover", cover.Cover, cg.Component)

CONFIG_SCHEMA = cv.All(
    cover.COVER_SCHEMA.extend(
        {
            cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(TuyaCover),
            cv.GenerateID(CONF_TUYA_ID): cv.use_id(Tuya),
            cv.Required(CONF_POSITION_DATAPOINT): cv.uint8_t,
            cv.Optional(CONF_MIN_VALUE): cv.int_,
            cv.Optional(CONF_MAX_VALUE): cv.int_,
            cv.Optional(CONF_INVERT_POSITION): cv.boolean,
        }
    ).extend(cv.COMPONENT_SCHEMA),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    await cg.register_component(var, config)
    await cover.register_cover(var, config)

    if CONF_POSITION_DATAPOINT in config:
        cg.add(var.set_position_id(config[CONF_POSITION_DATAPOINT]))
    if CONF_MIN_VALUE in config:
        cg.add(var.set_min_value(config[CONF_MIN_VALUE]))
    if CONF_MAX_VALUE in config:
        cg.add(var.set_max_value(config[CONF_MAX_VALUE]))
    if CONF_INVERT_POSITION in config:
        cg.add(var.set_invert_position(config[CONF_INVERT_POSITION]))
    paren = await cg.get_variable(config[CONF_TUYA_ID])
    cg.add(var.set_tuya_parent(paren))
