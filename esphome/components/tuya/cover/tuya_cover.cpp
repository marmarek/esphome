#include "esphome/core/log.h"
#include "tuya_cover.h"

namespace esphome {
namespace tuya {

static const char *const TAG = "tuya.cover";

void TuyaCover::setup() {
  if (this->position_id_.has_value()) {
    this->parent_->register_listener(*this->position_id_, [this](const TuyaDatapoint &datapoint) {
      this->position = float(datapoint.value_uint) / this->max_value_;
      this->publish_state();
    });
  }
}

void TuyaCover::control(const cover::CoverCall &call) {
  if (call.get_stop()) {
    auto position_int = static_cast<uint32_t>(this->position * this->max_value_);
    position_int = std::max(position_int, this->min_value_);

    parent_->set_integer_datapoint_value(*this->position_id_, position_int);
  }
  if (call.get_position().has_value()) {
    auto pos = *call.get_position();
    auto position_int = static_cast<uint32_t>(pos * this->max_value_);
    position_int = std::max(position_int, this->min_value_);

    parent_->set_integer_datapoint_value(*this->position_id_, position_int);
  }

  this->publish_state();
}

void TuyaCover::dump_config() {
  ESP_LOGCONFIG(TAG, "Tuya Cover:");
  if (this->position_id_.has_value())
    ESP_LOGCONFIG(TAG, "   Position has datapoint ID %u", *this->position_id_);
}

cover::CoverTraits TuyaCover::get_traits() {
  auto traits = cover::CoverTraits();
  traits.set_supports_position(true);
  return traits;
}

}  // namespace tuya
}  // namespace esphome
