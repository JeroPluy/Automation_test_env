-- STANDARD INTEGRATION
/* import the standard integrations */

INSERT INTO integration(i_id, i_name)
VALUES  (1,     'alarm_control_panel'),
        (2,     'binary_sensor'),
        (3,     'button'),
        (4,     'calendar'),
        (5,     'camera'),
        (6,     'climate'),
        (7,     'conversation'),
        (8,     'cover'),
        (9,     'date'),
        (10,    'datetime'),
        (11,    'device_tracker'),
        (12,    'event'),
        (13,    'fan'),
        (14,    'humidifier'),
        (15,    'image'),
        (16,    'lawn_mower'),
        (17,    'light'),
        (18,    'lock'),
        (19,    'media_player'),
        (20,    'notify'),
        (21,    'number'),
        (22,    'remote'),
        (23,    'scene'),
        (24,    'select'),
        (25,    'sensor'),
        (26,    'sensor_enum'),
        (27,    'siren'),
        (28,    'stt'),
        (29,    'switch'),
        (30,    'text'),
        (31,    'time'),
        (32,    'todo'),
        (33,    'tts'),
        (34,    'update'),
        (35,    'vacuum'),
        (36,    'valve'),
        (37,    'wake_word'),
        (38,    'water_heater'),
        (39,    'weather');
  
-- POSSIBLE VALUES --
/* import the values from standard integrations */

/* alarm_control_panel 
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/alarm-control-panel
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (1,     'main',     'None'),	                --Unknown state.
        (2,     'main',     'disarmed'),	        --The alarm is disarmed (off).
        (3,     'main',     'armed_home'),	        --The alarm is armed in home mode.
        (4,     'main',     'armed_away'),	        --The alarm is armed in away mode.
        (5,     'main',     'armed_night'),	        --The alarm is armed in night mode.
        (6,     'main',     'armed_vacation'),	        --The alarm is armed in vacation mode.
        (7,     'main',     'armed_custom_bypass'),     --The alarm is armed in bypass mode.
        (8,     'main',     'pending'),	                --The alarm is pending (towards triggered).
        (9,     'main',     'arming'),	                --The alarm is arming.
        (10,    'main',     'disarming'),	        --The alarm is disarming.
        (11,    'main',     'triggered');               --The alarm is triggered.
        (12,    'main',     'unknown'),	                --Unknown state.
        (13,    'main',     'unavailable');             --The entity is not reachable.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (1, 10),
        (1, 11),
        (1, 12),
        (1, 13);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'code_format',          'number'),      --The code format of the alarm control panel.
        (,      'code_format',          'text'),        --The code format of the alarm control panel.
        (,      'changed_by',           'string'),      --The alarm control panel got changed by a user.
        (,      'code_arm_required',    'string'),      --The code required to arm the alarm control panel.
        (,      'supported_features',   'int');         --The count of supported features of the alarm control panel.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(1, ),
        (1, ),
        (1, ),
        (1, ),
        (1, );

/* binary_sensor 
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/binary-sensor
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/binary_sensor
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (14,    'main',     'on'),      --The sensor detects something.
        (15,    'main',     'off');     --The sensor detects nothing.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(2, 12),
        (2, 13),
        (2, 14),
        (2, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'device_class',         'battery'),             --The device class of the binary sensor.
        (,      'device_class',         'battery_charging'),    --The device class of the binary sensor.
        (,      'device_class',         'co'),                  --The device class of the binary sensor.
        (,      'device_class',         'cold'),                --The device class of the binary sensor.
        (,      'device_class',         'connectivity'),        --The device class of the binary sensor.
        (,      'device_class',         'door'),                --The device class of the binary sensor.
        (,      'device_class',         'garage_door'),         --The device class of the binary sensor.
        (,      'device_class',         'gas'),                 --The device class of the binary sensor.
        (,      'device_class',         'heat'),                --The device class of the binary sensor.
        (,      'device_class',         'light'),               --The device class of the binary sensor.
        (,      'device_class',         'lock'),                --The device class of the binary sensor.
        (,      'device_class',         'moisture'),            --The device class of the binary sensor.
        (,      'device_class',         'motion'),              --The device class of the binary sensor.
        (,      'device_class',         'moving'),              --The device class of the binary sensor.
        (,      'device_class',         'occupancy'),           --The device class of the binary sensor.
        (,      'device_class',         'opening'),             --The device class of the binary sensor.
        (,      'device_class',         'plug'),                --The device class of the binary sensor.
        (,      'device_class',         'power'),               --The device class of the binary sensor.
        (,      'device_class',         'presence'),            --The device class of the binary sensor.
        (,      'device_class',         'problem'),             --The device class of the binary sensor.
        (,      'device_class',         'running'),             --The device class of the binary sensor.
        (,      'device_class',         'safety'),              --The device class of the binary sensor.
        (,      'device_class',         'smoke'),               --The device class of the binary sensor.
        (,      'device_class',         'sound'),               --The device class of the binary sensor.
        (,      'device_class',         'tamper'),              --The device class of the binary sensor.
        (,      'device_class',         'update'),              --The device class of the binary sensor.
        (,      'device_class',         'vibration'),           --The device class of the binary sensor.
        (,      'device_class',         'window');              --The device class of the binary sensor.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, ),
        (2, );

/* button 
        states(main) / attributes extracted from:
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/button
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES	(3, 12),
        (3, 13);


/* calendar
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/calendar
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/calendar
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES	(4, 12),
        (4, 13),
        (4, 14),
        (4, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'description',          'string'),      --The calender description.
        (,      'message',              'string'),      --The calender message.
        (,      'all_day',              'string'),      --The calender event is all day.
        (,      'start_time',           'string'),      --The calender event start time.
        (,      'end_time',             'string'),      --The calender event end time.
        (,      'location',             'string');      --The calender event location.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(4, ),
        (4, ),
        (4, ),
        (4, ),
        (4, ),
        (4, );

/* camera 
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/camera
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/camera

*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (16,    'main',     'idle'),            --The camera observes.
        (17,    'main',     'recording'),       --The camera records the recording.
        (18,    'main',     'streaming');       --The camera streams the recording.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(5, 12),
        (5, 13),
        (5, 16),
        (5, 17),
        (5, 18);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'frontend_stream_type', 'hls'),         --The streaming format in the ui of the camera.
        (,      'frontend_stream_type', 'web_rtc');     --The streaming format in the ui of the camera.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(5, ),
        (5, ); -- supp features


/* climate  
        states(main) / attributes extracted from:
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/climate
        https://www.home-assistant.io/integrations/climate.mqtt/ 
        https://www.home-assistant.io/integrations/climate/
        https://developers.home-assistant.io/docs/core/entity/climate/
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (19,    'main',     'auto'),            --The device is set to a schedule, learned behavior, AI.
        (20,    'main',     'cool'),            --The device is set to cool to a target temperature.
        (21,    'main',     'heat'),            --The device is set to heat to a target temperature.
        (22,    'main',     'heat_cool'),       --The device is set to heat/cool to a target temperature range.
        (23,    'main',     'dry'),             --The device is set to dry/humidity mode.
        (24,    'main',     'fan_only');        --The device only has the fan on. No heating or cooling taking place.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (6, 12),
        (6, 13),
        (6, 15),
        (6, 20),
        (6, 21),
        (6, 22),
        (6, 23),
        (6, 24);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'current_humidity',     'float'),       --The current humidity.
        (,      'current_temperature',  'float'),       --The current temperature.
        (,      'max_humidity',         'float'),       --The maximum humidity.
        (,      'max_temp',             'float'),       --The maximum temperature in temperature_unit.
        (,      'min_humidity',         'float'),       --The minimum humidity.
        (,      'min_temp',             'float'),       --The minimum temperature in temperature_unit.
        (,      'precision',            'float'),       --The precision of the temperature in the system. Defaults to tenths for TEMP_CELSIUS, whole number otherwise.
        (,      'humidity',             'float'),       --The target humidity the device is trying to reach.
        (,      'temperature',          'float'),       --The temperature currently set to be reached.
        (,      'target_temp_high',     'float'),       --The upper bound target temperature.
        (,      'target_temp_low',      'float'),       --The lower bound target temperature
        (,      'target_temp_step',     'int'),         --The supported step size a target temperature can be increased or decreased
        (,      'temperature_unit',     'string'),      --The unit of temperature measurement for the system (TEMP_CELSIUS or TEMP_FAHRENHEIT).
        (,      'hvac_action',          'preheating'),  --Device is preheating.
        (,      'hvac_action',          'heating'),     --Device is heating.
        (,      'hvac_action',          'cooling'),     --Device is cooling.
        (,      'hvac_action',          'drying'),      --Device is drying.
        (,      'hvac_action',          'fan'),         --Device has fan on.
        (,      'hvac_action',          'defrosting'),  --Device is defrosting.
        (,      'hvac_action',          'off'),         --Device is off.
        (,      'hvac_action',          'idle'),        --Device is doing nothing.        
        (,      'fan_mode',             'on'),          --The fan on.
        (,      'fan_mode',             'off'),         --The fan off.
        (,      'fan_mode',             'auto_high'),   --The fan turns on automatically high.
        (,      'fan_mode',             'auto_low'),    --The fan turns on automatically low.
        (,      'fan_mode',             'on_low'),      --The fan speed is low.
        (,      'fan_mode',             'on_medium'),   --The fan speed is medium.
        (,      'fan_mode',             'on_high'),     --The fan speed is high.
        (,      'fan_mode',             'middle'),      --The fan stayes in the middle.
        (,      'fan_mode',             'focus'),       --The fan focuses in on direction.
        (,      'fan_mode',             'diffuse'),     --The fan diffuse in all possible directions.
        (,      'swing_mode',           'off'),         --The fan don't swing.
        (,      'swing_mode',           'auto'),        --The fan swings automatically.
        (,      'swing_mode',           '1'),           --The fan swings with speed 1.
        (,      'swing_mode',           '2'),           --The fan swings with speed 2.
        (,      'swing_mode',           '3'),           --The fan swings with speed 3.
        (,      'swing_mode',           'vertical'),    --The fan swings vertically.
        (,      'swing_mode',           'horizontal'),  --The fan swings horizontally.
        (,      'swing_mode',           'both');        --The fan swings in both directions.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ),
        (6, ); -- supp features

/* conversation 
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/conversation/
        https://developers.home-assistant.io/docs/core/entity/conversation
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (25,    'main',     'string');          --The scentence in the converstation.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (7, 12),
        (7, 13),
        (7, 25);

/* cover
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/cover

*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (26,    'main',     'closed'),          --The cover has reach the closed position.
        (27,    'main',     'closing'),         --The cover is in the process of closing to reach a set position.
        (28,    'main',     'open'),            --The cover has reached the open position.
        (29,    'main',     'opening');         --The cover is in the process of opening to reach a set position.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (8, 12),
        (8, 13),
        (8, 26),
        (8, 27),
        (8, 28),
        (8, 29);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'device_class',         'awning'),      --The device class of the binary sensor.
        (,      'device_class',         'blind'),       --The device class of the binary sensor.
        (,      'device_class',         'curtain'),     --The device class of the binary sensor.
        (,      'device_class',         'damper'),      --The device class of the binary sensor.
        (,      'device_class',         'garage'),      --The device class of the binary sensor.
        (,      'device_class',         'gate'),        --The device class of the binary sensor.
        (,      'device_class',         'shade'),       --The device class of the binary sensor.(,    'device_class',           'awning'),                 --The device class of the binary sensor.
        (,      'device_class',         'sutter');      --The device class of the binary sensor.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (8, ),
        (8, ),
        (8, ),
        (8, ),
        (8, ),
        (8, ),
        (8, ),--dev_class door
        (8, ),
        (8, ),
        (8, ),
        (8, ),--dev_class window
        (8, );-- supp features

/* date
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/date
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/date
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (9, 12),
        (9, 13),
        (9, 25);

/* datetime
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/datetime
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/datetime
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (10, 12),
        (10, 13),
        (10, 25);

/* device_tracer
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/device-tracker
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/device_tracker
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (30,    'main',     'home'),            --The device is home.
        (31,    'main',     'not_home');        --The cover is not home.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (11, 12),
        (11, 13),
        (11, 30),
        (11, 31):

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'source_type',          'gps'),                 --The source of the device connection.
        (,      'source_type',          'router'),              --The source of the device connection.
        (,      'source_type',          'bluetooth'),           --The source of the device connection.
        (,      'source_type',          'bluetooth_le'),        --The source of the device connection.
        (,      'longitude',            'float'),               --The source of the device connection.
        (,      'latitude',             'float'),               --The source of the device connection.
        (,      'location_accuracy',    'string'),              --The source of the device connection.
        (,      'battery',              'int');                 --The source of the device connection.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (11, ),
        (11, ),
        (11, ),
        (11, ),
        (11, ),
        (11, ),
        (11, ),
        (11, );

/* event
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/event
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/event
        https://www.home-assistant.io/docs/configuration/events/
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (12, 12),
        (12, 13),
        (12, 25); -- time_fired

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'event_type',           'pressed'),                     --The event of a button press.
        (,      'event_type',           'call_service'),                --The event of a service called.
        (,      'event_type',           'component_loaded'),            --The event of component loaded.
        (,      'event_type',           'core_config_updated'),         --The event of update the core config.
        (,      'event_type',           'data_entry_flow_progressed'),  --The event of data entry flow progresses.
        (,      'event_type',           'homeassistant_start'),         --The event of home assistant starting.
        (,      'event_type',           'homeassistant_started'),       --The event ofhome assistant started.
        (,      'event_type',           'homeassistant_stop'),          --The event home assistant stopped.
        (,      'event_type',           'homeassistant_final_write'),   --The event home assistant makes it final write befor shutting down.
        (,      'event_type',           'logbook_entry'),               --The event of making a logbook entry.
        (,      'event_type',           'service_registered'),          --The event of register a new service.
        (,      'event_type',           'service_removed'),             --The event of removing a service.
        (,      'event_type',           'state_changed'),               --The event of state change of an entity.
        (,      'event_type',           'themes_updated'),              --The event of the theme change in the ui.
        (,      'event_type',           'user_added'),                  --The event for a new user.
        (,      'event_type',           'user_removed'),                --The event to remove a user.
        (,      'event_type',           'automation_reloaded'),         --The event of reloading the automation.yaml files.
        (,      'event_type',           'automation_triggered'),        --The event of triggering an automation.
        (,      'event_type',           'scene_reloaded'),              --The event of reload a scene. 
        (,      'event_type',           'script_started'),              --The event of the start of a script.
        (,      'event_type',           'area_registry_updated'),       --The event of an area update.
        (,      'event_type',           'category_registry_updated'),   --The event of a category registry update.
        (,      'event_type',           'device_registry_updated'),     --The event of a device registry update.
        (,      'event_type',           'entity_registry_updated');     --The event of a entity registry update.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, ),
        (12, );

/* fan
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/fan
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/fan
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (13, 12),
        (13, 13),
        (13, 14),
        (13, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'percentage',           'int'),         --The current speed percentage. Must be a value between 0 (off) and 100.
        (,      'percentage_step',      'int'),         --The steps for the speed percentage. Must be a value between 1 and 100.
        (,      'oscillating',          'bool'),        --The if the fan is oscillating.
        (,      'direction',            'forward'),     --The fan spinns forward.
        (,      'direction',            'reverse');     --The fan spinns reverse.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (13, ),
        (13, ),
        (13, ),
        (13, ),
        (13, ),
        (13, ); -- supp features

/* humidifier
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/humidifier
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/humidifier
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (14, 12),
        (14, 13),
        (14, 14),
        (14, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'action',               'off'),                 --The humidifier is off.
        (,      'action',               'idle'),                --The humidifier does nothing.
        (,      'action',               'humidifying'),         --The humidifier humidifying the air.
        (,      'action',               'drying'),              --The humidifier drying the air.
        (,      'device_class',         'humidifier'),          --The humidifier is a humidifier.
        (,      'device_class',         'dehumidifier');        --The humidifier is a dehumidifier.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (14, ), --min hum
        (14, ), --max hum
        (14, ), --curr hum
        (14, ), --hum
        (14, ),
        (14, ),
        (14, ),
        (14, ),
        (14, ),
        (14, ),
        (14, ); -- supp features


/* image
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/image
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (15, 12),
        (15, 13),
        (15, 25);

/* lawn_mower
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/lawn-mower
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/lawn_mower

*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (32,    'main',     'mowing'), 	        --The lawn mower is currently mowing.
        (33,    'main',     'docked'),	        --The lawn mower is done mowing and is currently docked.
        (34,    'main',     'paused'),	        --The lawn mower was active and is now paused.
        (35,    'main',     'error');           --The lawn mower encountered an error while active and needs assistance.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (16, 12),
        (16, 13),
        (16, 32),
        (16, 33),
        (16, 34),
        (16, 35);

/* light
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/light
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/light
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (17, 12),
        (17, 13),
        (17, 14),
        (17, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'effect',               'rainbow'),                             --The light makes a rainbow effect.
        (,      'effect',               'none'),                                --The light makes no effect.
        (,      'min_color_temp_kelvin','int'),                                 --The minimal color value.
        (,      'max_color_temp_kelvin','int'),                                 --The maximal color value.
        (,      'color_mode',           'color_temp'),                          --The ui color setting.
        (,      'color_mode',           'hs'),                                  --The ui color setting.
        (,      'brightness',           'int'),                                 --The brightness of the light.
        (,      'color_temp_kelvin',    'int'),                                 --The color of the light as kelvin number.
        (,      'hs_color',             'tuple[float, float]'),                 --The color of the light in hs-format.
        (,      'rgb_color',            'tuple[int, int, int]'),                --The color of the light in rgb-format.
        (,      'xy_color',             'tuple[float, float]'),                 --The color of the light in xy-format.
        (,      'rgbw_color',           'tuple[int, int, int, int]'),           --The color of the light in rgbw-format.
        (,      'rgbww_color',          'tuple[int, int, int, int, int]');      --The color of the light in rgbww-format.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (17, ),
        (17, ),
        (17, ),
        (17, ),
        (17, ),
        (17, ),
        (17, ),
        (17, ),
        (17, ),
        (17, ),
        (17, ); -- supp features

/* lock
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/lock
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/lock
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (36,    'main',     'jammed'),          --The lock is unabled to toggle.
        (37,    'main',     'locked'),          --The lock is locked.
        (38,    'main',     'locking'),         --The lock is looking.
        (39,    'main',     'unlocked'),        --The lock is unlocked.
        (40,    'main',     'unlocking');       --The lock is unlooking.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (18, 12),
        (18, 13),
        (18, 28),
        (18, 29),
        (18, 36),
        (18, 37),
        (18, 38),
        (18, 39),
        (18, 40);

-- ATTRIBUTES --
INSERT INTO integration_values(i_id, pv_id)
VALUES  (18, ), -- code_format num
        (18, ), -- code_format text
        (18, ), -- changed_by 
        (18, ); -- supp features

/* media_player
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/media-player
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/media_player
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (41,    'main',     'playing'),         --The media player playimg something.
        (42,    'main',     'standby'),         --The media player is in standby mode.
        (43,    'main',     'buffering');       --The media player buffering something.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (19, 12),
        (19, 13),
        (19, 14),
        (19, 15),
        (19, 16),
        (19, 41),
        (19, 34),
        (19, 42),
        (19, 43),

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'volume_level',         'float '),              --The volume level of the media player in the range (0..1).
        (,      'is_volume_muted',      'bool'),                --Its true if volume is currently muted.
        (,      'volume_step',          'float'),               --The volume step to use for the volume_up and volume_down services.
        (,      'media_content_id',     'string'),              --The content ID of current playing media.
        (,      'media_content_type',   'album'),               --The content type of current playing media.
        (,      'media_content_type',   'app'),                  --The content type of current playing media.
        (,      'media_content_type',   'artist'),              --The content type of current playing media.
        (,      'media_content_type',   'channel'),             --The content type of current playing media.
        (,      'media_content_type',   'channels'),            --The content type of current playing media.
        (,      'media_content_type',   'composer'),            --The content type of current playing media.
        (,      'media_content_type',   'contibuting_artist'),  --The content type of current playing media.
        (,      'media_content_type',   'episode'),             --The content type of current playing media.
        (,      'media_content_type',   'game'),                --The content type of current playing media.
        (,      'media_content_type',   'genre'),               --The content type of current playing media.
        (,      'media_content_type',   'image'),               --The content type of current playing media.
        (,      'media_content_type',   'movie'),               --The content type of current playing media.
        (,      'media_content_type',   'music'),               --The content type of current playing media.
        (,      'media_content_type',   'playlist'),            --The content type of current playing media.
        (,      'media_content_type',   'podcast'),             --The content type of current playing media.
        (,      'media_content_type',   'season'),              --The content type of current playing media.
        (,      'media_content_type',   'track'),               --The content type of current playing media.
        (,      'media_content_type',   'tvshow'),              --The content type of current playing media.
        (,      'media_content_type',   'url'),                 --The content type of current playing media.
        (,      'media_content_type',   'video'),               --The content type of current playing media.
        (,      'app_name',             'string'),              --The name of the current running app.
        (,      'group_members',        'list[string]'),        --A dynamic list of player entities which are currently grouped together for synchronous playback.
        (,      'media_album_artist',   'string'),              --The album artist of current playing media, music track only.
        (,      'media_album_name',     'string'),              --The album name of current playing media, music track only.
        (,      'media_artist',         'string'),              --The artist of current playing media, music track only.
        (,      'media_channel',        'string'),              --The channel currently playing.
        (,      'media_duration',       'int'),                 --The duration of current playing media in seconds.
        (,      'media_episode',        'string'),              --The episode of current playing media, TV show only.
        (,      'media_playlist',       'string'),              --The duration of current playing media in seconds.
        (,      'media_position',       'int'),                 --The episode of current playing media, TV show only
        (,      'media_season',         'string'),              --The duration of current playing media in seconds.
        (,      'media_series_title',   'string'),              --The episode of current playing media, TV show only
        (,      'media_title',          'string'),              --The duration of current playing media in seconds.
        (,      'media_track',          'int'),                 --The track number of current playing media, music track only.
        (,      'repeat',               'off'),                 --The current repeat mode.
        (,      'repeat',               'one'),                 --The current repeat mode.
        (,      'repeat',               'all'),                 --The current repeat mode.
        (,      'shuffle',              'bool'),                --True if shuffle is enabled.
        (,      'source',               'dvd'),                 --The currently selected input source for the media player.
        (,      'source',               'youtube'),             --The currently selected input source for the media player.
        (,      'sound_mode',           'music'),               --The current sound mode of the media player.
        (,      'sound_mode',           'movie'),               --The current sound mode of the media player.
        (,      'device_class',         'tv'),                  --The media player is a tv.
        (,      'device_class',         'speaker'),             --The media player is a speaker.
        (,      'device_class',         'receiver');            --The media player is a receiver.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ),
        (19, ); -- supp features

/* notify
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/notify
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/notify
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (20, 12),
        (20, 13);

-- ATTRIBUTES --
INSERT INTO integration_values(i_id, pv_id)
VALUES  (20, ); -- supp features

/* number
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/number
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (44,    'main',     'float'),                   --The number of the entity.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (21, 12),
        (21, 13),
        (21, 44);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'min',                  'float '),      --The minimum accepted value in the number's (inclusive).
        (,      'max',                  'float'),       --The maximum accepted value in the number's (inclusive).
        (,      'step',                 'float'),       --Defines the resolution of the values, i.e. the smallest increment or decrement in the number's.
        (,      'mode',                 'string'),      --Defines how the number should be displayed in the UI. Can be box, slider or auto.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (21, ),
        (21, ),
        (21, ),
        (21, );

/* remote
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/remote
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/remote
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (22, 12),
        (22, 13),
        (22, 25);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'activity',             'string'),      --The minimum accepted value in the number's (inclusive).
        (,      'current_activity',     'string');      --The maximum accepted value in the number's (inclusive).


INSERT INTO integration_values(i_id, pv_id)
VALUES  (22, ),
        (22, );

/* scene
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/scene
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/scene/__init__.py
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (23, 12),
        (23, 13),
        (23, 25);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'id',                   'string'),      --The id of the scene.
        (,      'entity_id',            'string');      --The id of the entity in the scene.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (23, ),
        (23, );

/* select
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/select
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/select
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (45,    'main', 	'option');      --The one of the options of the select.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (24, 12),
        (24, 13),
        (24, 45);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'options',              'list[string]');        --All options of the select.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (24, );

/* sensor
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/sensor
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/sensor
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (25, 12),
        (25, 13),
        (25, 25),
        (25, 44);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'device_class',         'apparent_power'),                      --The device class of the sensor.
        (,      'device_class',         'aqi'),                                 --The device class of the sensor.
        (,      'device_class',         'carbon_dioxide'),                      --The device class of the sensor.
        (,      'device_class',         'carbon_monoxide'),                     --The device class of the sensor.
        (,      'device_class',         'current'),                             --The device class of the sensor.
        (,      'device_class',         'date'),                                --The device class of the sensor.
        (,      'device_class',         'duration'),                            --The device class of the sensor.
        (,      'device_class',         'energy'),                              --The device class of the sensor.
        (,      'device_class',         'frequency'),                           --The device class of the sensor.
        (,      'device_class',         'humidity'),                            --The device class of the sensor.
        (,      'device_class',         'illuminance'),                         --The device class of the sensor.
        (,      'device_class',         'monetary'),                            --The device class of the sensor.
        (,      'device_class',         'nitrogen_dioxide'),                    --The device class of the sensor.
        (,      'device_class',         'nitrogen_monoxide'),                   --The device class of the sensor.
        (,      'device_class',         'nitrous_oxide'),                       --The device class of the sensor.
        (,      'device_class',         'ozone'),                               --The device class of the sensor.
        (,      'device_class',         'ph'),                                  --The device class of the sensor.
        (,      'device_class',         'pm1'),                                 --The device class of the sensor.
        (,      'device_class',         'pm10'),                                --The device class of the sensor.
        (,      'device_class',         'pm25'),                                --The device class of the sensor.
        (,      'device_class',         'power_factor'),                        --The device class of the sensor.
        (,      'device_class',         'pressure'),                            --The device class of the sensor.
        (,      'device_class',         'reactive_power'),                      --The device class of the sensor.
        (,      'device_class',         'signal_strength'),                     --The device class of the sensor.
        (,      'device_class',         'sulphur_dioxide'),                     --The device class of the sensor.
        (,      'device_class',         'temperature'),                         --The device class of the sensor.
        (,      'device_class',         'timestamp'),                           --The device class of the sensor.
        (,      'device_class',         'volatile_organic_compounds'),          --The device class of the sensor.
        (,      'device_class',         'volatile_organic_compounds_parts'),    --The device class of the sensor.
        (,      'device_class',         'voltage'),                             --The device class of the sensor.
        (,      'device_class',         'volume_flow_rate'),                    --The device class of the sensor.
        (,      'unit_of_measurement',  'string'),                              --The unit of the sensor value.
        (,      'battery_level',        'int');                                 --The battery level of the sensor.
        
INSERT INTO integration_values(i_id, pv_id)
VALUES  (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, ),
        (25, );

/* sensor_enum
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/sensor
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/sensor
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (26, 12),
        (26, 13),
        (26, 45);

-- ATTRIBUTES --
INSERT INTO integration_values(i_id, pv_id)
VALUES  (26, ); --All options of the sensor.

/* siren
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/siren
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/siren
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (27, 12),
        (27, 13),
        (27, 14),
        (27, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'available_tones',      'list[string]');        --The list of possible sounds for the siren.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (27, ),
        (27, ); --supp feat

/* stt
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/stt
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/stt
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (28, 12),
        (28, 13);

/* switch
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/switch
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (29, 12),
        (29, 13),
        (29, 14),
        (29, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'device_class',         'switch'),      --The device class of the switch.
        (,      'device_class',         'outlet'),      --The device class of the switch.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (29, ),
        (29, );

/* text
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/text
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (30, 12),
        (30, 13),
        (30, 25);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'mode',                 'text'),        --The text ui mode.
        (,      'mode',                 'password'),    --The text ui mode.
        (,      'pattern',              'string'),      --A regex pattern that the text value must match to be valid.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (30, ),
        (30, ),
        (30, ),--min
        (30, ),--max
        (30, );

/* time
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/time
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (31, 12),
        (31, 13),
        (31, 25);

/* todo
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/todo
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (46,      'main',         'int');           --A TodoListEntity state is the count of incomplete items in the To-do list.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (32, 12),
        (32, 13),
        (32, 46);

-- ATTRIBUTES --
INSERT INTO integration_values(i_id, pv_id)
VALUES  (32, );--supp feat

/* tts
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/tts
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (33, 12),
        (33, 13);

/* update
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/update
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/update
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (34, 12),
        (34, 13),
        (34, 14),
        (34, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'auto_update',          'bool'),        --The device or service that the entity represents has auto update logic. When this is set to True you can not skip updates.
        (,      'installed_version',    'string'),      --The currently installed and used version of the software.
        (,      'in_progress',          'int'),         --Update installation progress. Can either return a boolean (1 if in progress, 0 if not) or an int to indicate the progress from 0 to 100%.
        (,      'release_summary',      'string'),      --Summary of the release notes or changelog.
        (,      'release_url',          'string'),      --URL to the full release notes of the latest version available.
        (,      'current_version',      'string'),      --The current version of the update.
        (,      'skipped_version',      'string'),      --The version that was skipped.
        (,      'title',                'string'),      --Title of the software.
        (,      'latest_version',       'string'),      --The latest version of the software available.
        (,      'device_class',         'firmware');    --The device class of the update.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (34, ),
        (34, ),
        (34, ),
        (34, ),
        (34, ),
        (34, ),
        (34, ),
        (34, ),
        (34, ),
        (34, ),
        (34, );--supp feat

/* vacuum
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/vacuum
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (47,    'main',     'cleaning'),                --The vacuum is cleaning.
        (48,    'main',     'returning');               --The vacuum is returning to the dock.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (35, 12),
        (35, 13),
        (35, 47),
        (35, 33),
        (35, 16),
        (35, 34),
        (35, 48),
        (35, 35);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'battery_icon',         'string'),      --The time the vacuum has been cleaning.
        (,      'cleaned_area',         'float'),       --The percentage of the area that has been cleaned.
        (,      'fan_speed',            'min'),         --The speed of the vacuum fan.
        (,      'fan_speed',            'medium'),      --The speed of the vacuum fan.
        (,      'fan_speed',            'high'),        --The speed of the vacuum fan.
        (,      'fan_speed',            'max');         --The speed of the vacuum fan.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (35,)--battery_level
        (35,)
        (35,)
        (35,)
        (35,)
        (35,)
        (35,)
        (35,);--supp feat

/* valve
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/valve
        https://www.home-assistant.io/integrations/valve/
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (36, 12),
        (36, 13),
        (36, 26),
        (36, 27),
        (36, 28),
        (36, 29);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'device_class',         'water'),       --The device class of the valve.
        (,      'current_position',     'int');         --The current position of the valve.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (36, ),--device_class gas
        (36, ),
        (36, );

/* wake_word
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/wake_word
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (37, 12),
        (37, 13);

/* water_heater
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/water-heater
        https://github.com/home-assistant/core/blob/master/homeassistant/components/water_heater/__init__.py
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (49,    'main',     'eco'),                     --The water heater is in eco mode.
        (50,    'main',     'electric'),                --The water heater is in electric mode.
        (51,    'main',     'performance'),             --The water heater is in high performance mode.
        (52,    'main',     'high_demand'),             --The water heater is in high performance mode.
        (53,    'main',     'heat_pump'),               --The water heater is in heat pump mode.
        (54,    'main',     'gas');                     --The water heater is in gas mode.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (38, 12),
        (38, 13),
        (38, 15),
        (38, 21),
        (38, 49),
        (38, 50),
        (38, 51),
        (38, 52),
        (38, 53),
        (38, 54);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'operation_mode',       'eco'),         --The operation mode of the water heater.
        (,      'operation_mode',       'electric'),    --The operation mode of the water heater.
        (,      'operation_mode',       'performance'), --The operation mode of the water heater.
        (,      'operation_mode',       'high_demand'), --The operation mode of the water heater.
        (,      'operation_mode',       'heat_pump'),   --The operation mode of the water heater.
        (,      'operation_mode',       'gas'),         --The operation mode of the water heater.
        (,      'operation_mode',       'off'),         --The operation mode of the water heater.
        (,      'away_mode',            'on'),          --The away mode of the water heater.
        (,      'away_mode',            'off');         --The away mode of the water heater.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (38, ), --min_temp
        (38, ), --max_temp
        (38, ), --curr_temp
        (38, ), --temp
        (38, ), --target_temp_high
        (38, ), --target_temp_low
        (38, ),
        (38, ),
        (38, ),
        (38, ),
        (38, ),
        (38, ),
        (38, ),
        (38, ),
        (38, ),
        (38, );--supp feat

/* weather
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/weather
        https://github.com/home-assistant/core/blob/master/homeassistant/components/water_heater/__init__.py
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (55,    'main',     'clear-night'),             --The weather is clear at night.
        (56,    'main',     'cloudy'),                   --The weather is cloudy.
        (57,    'main',     'exceptional'),              --The weather is exceptional.
        (58,    'main',     'fog'),                      --The weather is foggy.
        (59,    'main',     'hail'),                     --The weather is hailing.
        (60,    'main',     'lightning'),                --The weather is lightning.
        (61,    'main',     'lightning-rainy'),          --The weather is lightning and rainy.
        (62,    'main',     'partlycloudy'),             --The weather is partly cloudy.
        (63,    'main',     'pouring'),                  --The weather is pouring.
        (64,    'main',     'rainy'),                    --The weather is rainy.
        (65,    'main',     'snowy'),                    --The weather is snowy.
        (66,    'main',     'snowy-rainy'),              --The weather is snowy and rainy.
        (67,    'main',     'sunny'),                    --The weather is sunny.
        (68,    'main',     'windy'),                    --The weather is windy.
        (69,    'main',     'windy-variant');            --The weather is windy and variant.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (39, 12),
        (39, 13),
        (39, 15),
        (39, 21),
        (39, 55),
        (39, 56),
        (39, 57),
        (39, 58),
        (39, 59),
        (39, 60),
        (39, 61),
        (39, 62),
        (39, 63),
        (39, 64),
        (39, 65),
        (39, 66),
        (39, 67),
        (39, 68),
        (39, 69);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (,      'attribution',          'string'),      --The attributor of the weather.
        (,      'apparent_temperature', 'float'),       --The current apparent (feels-like) temperature in °C or °F.
        (,      'pressure',             'flaot'),       --The pressure of the weather.
        (,      'pressure_unit',        'string'),      --The pressure unit of the weather.
        (,      'wind_speed',           'float'),       --The wind bearing of the weather.
        (,      'wind_speed_unit',      'string'),      --The wind speed unit of the weather.
        (,      'wind_bearing',         'string'),      --The current wind bearing in azimuth angle (degrees) or 1-3 letter cardinal direction.
        (,      'wind_gust_speed',      'float'),       --he current wind gust speed.
        (,      'visibility',           'float'),       --The visibility of the weather.
        (,      'visibility_unit',      'string'),      --The visibility unit of the weather.
        (,      'cloud_coverage',       'int'),         --The cloud coverage of the weather.
        (,      'dew_point',            'float')        --The dew point temperature in °C or °F.
        (,      'ozone',                'float'),       --The current ozone level of the weather.
        (,      'uv_index',             'float'),       --The uv index of the weather.
        (,      'precipitation_unit',   'string');      -- The precipitation unit in mm or in.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (39, ),--humidity
        (39, ),--temperature
        (39, ),--temperature_unit
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, ),
        (39, );--supp feat
        