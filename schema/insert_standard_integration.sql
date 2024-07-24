-- TODO remove the following lines
DELETE FROM integration_values;  
DELETE FROM possible_values;
DELETE FROM integration; 

-- STANDARD INTEGRATION
/* import the standard integrations for entities */

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
        (25,    'sensor_float'),
        (26,    'sensor_string'),
        (27,    'sensor_enum'),
        (28,    'siren'),
        (29,    'stt'),
        (30,    'switch'),
        (31,    'text'),
        (32,    'time'),
        (33,    'todo'),
        (34,    'tts'),
        (35,    'update'),
        (36,    'vacuum'),
        (37,    'valve'),
        (38,    'wake_word'),
        (39,    'water_heater'),
        (40,    'weather'),
        -- TRIGGER INTEGRATION
/* import the integrations for triggers */
        (41,    'homeassistant'),
        (42,    'mqtt'),
        (43,    'sun'),
        (44,    'tag'),
        (45,    'time_pattern'),
        (46,    'persistent_notification'),
        (47,    'webhook'),
        (48,    'zone'),
        (49,    'device');

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
        (11,    'main',     'triggered'),               --The alarm is triggered.
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
VALUES  (70,    'code_format',          'number'),      --The code format of the alarm control panel.
        (71,    'code_format',          'text'),        --The code format of the alarm control panel.
        (72,    'changed_by',           'string'),      --The alarm control panel got changed by a user.
        (73,    'code_arm_required',    'string'),      --The code required to arm the alarm control panel.
        (74,    'supported_features',   'int');         --The count of supported features of the alarm control panel.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(1, 70),
        (1, 71),
        (1, 72),
        (1, 73),
        (1, 74);

/* binary_sensor 
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/binary-sensor
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/binary_sensor
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (14,    'main',     'on'),      --The sensor detects something.
        (15,    'main',     'off');     --The sensor detects nothing.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(2, 12), -- unkonwn
        (2, 13), -- unavailable
        (2, 14),
        (2, 15);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (75,    'device_class',         'battery'),             --The device class of the binary sensor.
        (76,    'device_class',         'battery_charging'),    --The device class of the binary sensor.
        (77,    'device_class',         'co'),                  --The device class of the binary sensor.
        (78,    'device_class',         'cold'),                --The device class of the binary sensor.
        (79,    'device_class',         'connectivity'),        --The device class of the binary sensor.
        (80,    'device_class',         'door'),                --The device class of the binary sensor.
        (81,    'device_class',         'garage_door'),         --The device class of the binary sensor.
        (82,    'device_class',         'gas'),                 --The device class of the binary sensor.
        (83,    'device_class',         'heat'),                --The device class of the binary sensor.
        (84,    'device_class',         'light'),               --The device class of the binary sensor.
        (85,    'device_class',         'lock'),                --The device class of the binary sensor.
        (86,    'device_class',         'moisture'),            --The device class of the binary sensor.
        (87,    'device_class',         'motion'),              --The device class of the binary sensor.
        (88,    'device_class',         'moving'),              --The device class of the binary sensor.
        (89,    'device_class',         'occupancy'),           --The device class of the binary sensor.
        (90,    'device_class',         'opening'),             --The device class of the binary sensor.
        (91,    'device_class',         'plug'),                --The device class of the binary sensor.
        (92,    'device_class',         'power'),               --The device class of the binary sensor.
        (93,    'device_class',         'presence'),            --The device class of the binary sensor.
        (94,    'device_class',         'problem'),             --The device class of the binary sensor.
        (95,    'device_class',         'running'),             --The device class of the binary sensor.
        (96,    'device_class',         'safety'),              --The device class of the binary sensor.
        (97,    'device_class',         'smoke'),               --The device class of the binary sensor.
        (98,    'device_class',         'sound'),               --The device class of the binary sensor.
        (99,    'device_class',         'tamper'),              --The device class of the binary sensor.
        (100,   'device_class',         'update'),              --The device class of the binary sensor.
        (101,   'device_class',         'vibration'),           --The device class of the binary sensor.
        (102,   'device_class',         'window');              --The device class of the binary sensor.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(2, 75),
        (2, 76),
        (2, 77),
        (2, 78),
        (2, 79),
        (2, 80),
        (2, 81),
        (2, 82),
        (2, 83),
        (2, 84),
        (2, 85),
        (2, 86),
        (2, 87),
        (2, 88),
        (2, 89),
        (2, 90),
        (2, 91),
        (2, 92),
        (2, 93),
        (2, 94),
        (2, 95),
        (2, 96),
        (2, 97),
        (2, 98),
        (2, 99),
        (2, 100),
        (2, 101),
        (2, 102);

/* button 
        states(main) / attributes extracted from:
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/button
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES	(3, 12), -- unkonwn
        (3, 13); -- unavailable


/* calendar
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/calendar
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/calendar
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES	(4, 12), -- unkonwn
        (4, 13), -- unavailable
        (4, 14), -- on
        (4, 15); -- off

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (103,   'description',          'string'),      --The calender description.
        (104,   'message',              'string'),      --The calender message.
        (105,   'all_day',              'string'),      --The calender event is all day.
        (106,   'start_time',           'string'),      --The calender event start time.
        (107,   'end_time',             'string'),      --The calender event end time.
        (108,   'location',             'string');      --The calender event location.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(4, 103),
        (4, 104),
        (4, 105),
        (4, 106),
        (4, 107),
        (4, 108);

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
VALUES	(5, 12), -- unkonwn
        (5, 13), -- unavailable
        (5, 16),
        (5, 17),
        (5, 18);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (109,   'frontend_stream_type', 'hls'),         --The streaming format in the ui of the camera.
        (110,   'frontend_stream_type', 'web_rtc');     --The streaming format in the ui of the camera.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(5, 109),
        (5, 110),
        (5, 74); -- supp features


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
VALUES  (6, 12), -- unkonwn
        (6, 13), -- unavailable
        (6, 15), -- off
        (6, 19),
        (6, 20),
        (6, 21),
        (6, 22),
        (6, 23),
        (6, 24);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (111,   'current_humidity',     'float'),       --The current humidity.
        (112,   'current_temperature',  'float'),       --The current temperature.
        (113,   'max_humidity',         'float'),       --The maximum humidity.
        (114,   'max_temp',             'float'),       --The maximum temperature in temperature_unit.
        (115,   'min_humidity',         'float'),       --The minimum humidity.
        (116,   'min_temp',             'float'),       --The minimum temperature in temperature_unit.
        (117,   'precision',            'float'),       --The precision of the temperature in the system. Defaults to tenths for TEMP_CELSIUS, whole number otherwise.
        (118,   'humidity',             'float'),       --The target humidity the device is trying to reach.
        (119,   'temperature',          'float'),       --The temperature currently set to be reached.
        (120,   'target_temp_high',     'float'),       --The upper bound target temperature.
        (121,   'target_temp_low',      'float'),       --The lower bound target temperature
        (122,   'target_temp_step',     'int'),         --The supported step size a target temperature can be increased or decreased
        (123,   'temperature_unit',     'string'),      --The unit of temperature measurement for the system (TEMP_CELSIUS or TEMP_FAHRENHEIT).
        (124,   'hvac_action',          'preheating'),  --Device is preheating.
        (125,   'hvac_action',          'heating'),     --Device is heating.
        (126,   'hvac_action',          'cooling'),     --Device is cooling.
        (127,   'hvac_action',          'drying'),      --Device is drying.
        (128,   'hvac_action',          'fan'),         --Device has fan on.
        (129,   'hvac_action',          'defrosting'),  --Device is defrosting.
        (130,   'hvac_action',          'off'),         --Device is off.
        (131,   'hvac_action',          'idle'),        --Device is doing nothing.        
        (132,   'fan_mode',             'on'),          --The fan on.
        (133,   'fan_mode',             'off'),         --The fan off.
        (134,   'fan_mode',             'auto_high'),   --The fan turns on automatically high.
        (135,   'fan_mode',             'auto_low'),    --The fan turns on automatically low.
        (136,   'fan_mode',             'on_low'),      --The fan speed is low.
        (137,   'fan_mode',             'on_medium'),   --The fan speed is medium.
        (138,   'fan_mode',             'on_high'),     --The fan speed is high.
        (139,   'fan_mode',             'middle'),      --The fan stayes in the middle.
        (140,   'fan_mode',             'focus'),       --The fan focuses in on direction.
        (141,   'fan_mode',             'diffuse'),     --The fan diffuse in all possible directions.
        (142,   'swing_mode',           'off'),         --The fan don't swing.
        (143,   'swing_mode',           'auto'),        --The fan swings automatically.
        (144,   'swing_mode',           '1'),           --The fan swings with speed 1.
        (145,   'swing_mode',           '2'),           --The fan swings with speed 2.
        (146,   'swing_mode',           '3'),           --The fan swings with speed 3.
        (147,   'swing_mode',           'vertical'),    --The fan swings vertically.
        (148,   'swing_mode',           'horizontal'),  --The fan swings horizontally.
        (149,   'swing_mode',           'both');        --The fan swings in both directions.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(6, 111),
        (6, 112),
        (6, 113),
        (6, 114),
        (6, 115),
        (6, 116),
        (6, 117),
        (6, 118),
        (6, 119),
        (6, 120),
        (6, 121),
        (6, 122),
        (6, 123),
        (6, 124),
        (6, 125),
        (6, 126),
        (6, 127),
        (6, 128),
        (6, 129),
        (6, 130),
        (6, 131),
        (6, 132),
        (6, 133),
        (6, 134),
        (6, 135),
        (6, 136),
        (6, 137),
        (6, 138),
        (6, 139),
        (6, 140),
        (6, 141),
        (6, 142),
        (6, 143),
        (6, 144),
        (6, 145),
        (6, 146),
        (6, 147),
        (6, 148),
        (6, 149),
        (6, 74); -- supp features

/* conversation 
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/conversation/
        https://developers.home-assistant.io/docs/core/entity/conversation
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (25,    'main',     'string');          --date of the last call in the converstation.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (7, 12), -- unkonwn
        (7, 13), -- unavailable
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
VALUES  (8, 12), -- unkonwn
        (8, 13), -- unavailable
        (8, 26),
        (8, 27),
        (8, 28),
        (8, 29);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (150,   'device_class',         'awning'),      --The device class of the binary sensor.
        (151,   'device_class',         'blind'),       --The device class of the binary sensor.
        (152,   'device_class',         'curtain'),     --The device class of the binary sensor.
        (153,   'device_class',         'damper'),      --The device class of the binary sensor.
        (154,   'device_class',         'garage'),      --The device class of the binary sensor.
        (155,   'device_class',         'gate'),        --The device class of the binary sensor.
        (156,   'device_class',         'shade'),       --The device class of the binary sensor.(,    'device_class',           'awning'),                 --The device class of the binary sensor.
        (157,   'device_class',         'sutter');      --The device class of the binary sensor.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (8, 150),
        (8, 151),
        (8, 152),
        (8, 153),
        (8, 154),
        (8, 155),
        (8, 156),
        (8, 157),
        (8, 80),  -- device_class door
        (8, 102), -- device_class window
        (8, 74);  -- supp features

/* date
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/date
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/date
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (9, 12), -- unkonwn
        (9, 13), -- unavailable
        (9, 25); -- date as string

/* datetime
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/datetime
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/datetime
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (10, 12), -- unkonwn
        (10, 13), -- unavailable
        (10, 25); -- datetime as string

/* device_tracer
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/device-tracker
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/device_tracker
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (30,    'main',     'home'),            --The device is home.
        (31,    'main',     'not_home');        --The cover is not home.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (11, 12), -- unkonwn
        (11, 13), -- unavailable
        (11, 30),
        (11, 31);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (158,   'source_type',          'gps'),                 --The source of the device connection.
        (159,   'source_type',          'router'),              --The source of the device connection.
        (160,   'source_type',          'bluetooth'),           --The source of the device connection.
        (161,   'source_type',          'bluetooth_le'),        --The source of the device connection.
        (162,   'longitude',            'float'),               --The source of the device connection.
        (163,   'latitude',             'float'),               --The source of the device connection.
        (164,   'location_accuracy',    'string'),              --The source of the device connection.
        (165,   'battery',              'int');                 --The source of the device connection.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (11, 158),
        (11, 159),
        (11, 160),
        (11, 161),
        (11, 162),
        (11, 163),
        (11, 164),
        (11, 165);

/* event
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/event
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/event
        https://www.home-assistant.io/docs/configuration/events/
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (12, 12), -- unkonwn
        (12, 13), -- unavailable
        (12, 25); -- time as string

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (166,   'event_type',           'pressed'),                     --The event of a button press.
        (167,   'event_type',           'call_service'),                --The event of a service called.
        (168,   'event_type',           'component_loaded'),            --The event of component loaded.
        (169,   'event_type',           'core_config_updated'),         --The event of update the core config.
        (170,   'event_type',           'data_entry_flow_progressed'),  --The event of data entry flow progresses.
        (171,   'event_type',           'homeassistant_start'),         --The event of home assistant starting.
        (172,   'event_type',           'homeassistant_started'),       --The event ofhome assistant started.
        (173,   'event_type',           'homeassistant_stop'),          --The event home assistant stopped.
        (174,   'event_type',           'homeassistant_final_write'),   --The event home assistant makes it final write befor shutting down.
        (175,   'event_type',           'logbook_entry'),               --The event of making a logbook entry.
        (176,   'event_type',           'service_registered'),          --The event of register a new service.
        (177,   'event_type',           'service_removed'),             --The event of removing a service.
        (178,   'event_type',           'state_changed'),               --The event of state change of an entity.
        (179,   'event_type',           'themes_updated'),              --The event of the theme change in the ui.
        (180,   'event_type',           'user_added'),                  --The event for a new user.
        (181,   'event_type',           'user_removed'),                --The event to remove a user.
        (182,   'event_type',           'automation_reloaded'),         --The event of reloading the automation.yaml files.
        (183,   'event_type',           'automation_triggered'),        --The event of triggering an automation.
        (184,   'event_type',           'scene_reloaded'),              --The event of reload a scene. 
        (185,   'event_type',           'script_started'),              --The event of the start of a script.
        (186,   'event_type',           'area_registry_updated'),       --The event of an area update.
        (187,   'event_type',           'category_registry_updated'),   --The event of a category registry update.
        (188,   'event_type',           'device_registry_updated'),     --The event of a device registry update.
        (189,   'event_type',           'entity_registry_updated');     --The event of a entity registry update.
        (190,   'event_type',           'string');                      --A custom event.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (12, 166),
        (12, 167),
        (12, 168),
        (12, 169),
        (12, 170),
        (12, 171),
        (12, 172),
        (12, 173),
        (12, 174),
        (12, 175),
        (12, 176),
        (12, 177),
        (12, 178),
        (12, 179),
        (12, 180),
        (12, 181),
        (12, 182),
        (12, 183),
        (12, 184),
        (12, 185),
        (12, 186),
        (12, 187),
        (12, 188),
        (12, 189),
        (12, 190);

/* fan
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/fan
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/fan
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (13, 12), -- unkonwn
        (13, 13), -- unavailable
        (13, 14), -- on
        (13, 15); -- off

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (191,      'percentage',           'int'),         --The current speed percentage. Must be a value between 0 (off) and 100.
        (192,      'percentage_step',      'int'),         --The steps for the speed percentage. Must be a value between 1 and 100.
        (193,      'oscillating',          'bool'),        --The if the fan is oscillating.
        (194,      'direction',            'forward'),     --The fan spinns forward.
        (195,      'direction',            'reverse');     --The fan spinns reverse.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (13, 191),
        (13, 192),
        (13, 193),
        (13, 194),
        (13, 195),
        (13, 74); -- supp features

/* humidifier
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/humidifier
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/humidifier
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (14, 12), -- unkonwn
        (14, 13), -- unavailable
        (14, 14), -- on
        (14, 15); -- off

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (196,   'action',               'off'),                 --The humidifier is off.
        (197,   'action',               'idle'),                --The humidifier does nothing.
        (198,   'action',               'humidifying'),         --The humidifier humidifying the air.
        (199,   'action',               'drying'),              --The humidifier drying the air.
        (200,   'device_class',         'humidifier'),          --The humidifier is a humidifier.
        (201,   'device_class',         'dehumidifier');        --The humidifier is a dehumidifier.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (14, 115), -- min_humidity
        (14, 113), -- max_humidity
        (14, 111), -- current_humidity
        (14, 118), -- humidity
        (14, 196),
        (14, 197),
        (14, 198),
        (14, 199),
        (14, 200),
        (14, 201),
        (14, 74); -- supp features


/* image
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/image
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (15, 12), -- unkonwn
        (15, 13), -- unavailable
        (15, 25); -- image url as string

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
VALUES  (16, 12), -- unkonwn
        (16, 13), -- unavailable
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
VALUES  (17, 12), -- unkonwn
        (17, 13), -- unavailable
        (17, 14), -- on
        (17, 15); -- off

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (202,   'effect',               'rainbow'),                             --The light makes a rainbow effect.
        (203,   'effect',               'none'),                                --The light makes no effect.
        (204,   'min_color_temp_kelvin','int'),                                 --The minimal color value.
        (205,   'max_color_temp_kelvin','int'),                                 --The maximal color value.
        (206,   'color_mode',           'color_temp'),                          --The ui color setting.
        (207,   'color_mode',           'hs'),                                  --The ui color setting.
        (208,   'brightness',           'int'),                                 --The brightness of the light.
        (209,   'color_temp_kelvin',    'int'),                                 --The color of the light as kelvin number.
        (210,   'hs_color',             'tuple[float, float]'),                 --The color of the light in hs-format.
        (211,   'rgb_color',            'tuple[int, int, int]'),                --The color of the light in rgb-format.
        (212,   'xy_color',             'tuple[float, float]'),                 --The color of the light in xy-format.
        (213,   'rgbw_color',           'tuple[int, int, int, int]'),           --The color of the light in rgbw-format.
        (214,   'rgbww_color',          'tuple[int, int, int, int, int]');      --The color of the light in rgbww-format.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (17, 202),
        (17, 203),
        (17, 204),
        (17, 205),
        (17, 206),
        (17, 207),
        (17, 208),
        (17, 209),
        (17, 210),
        (17, 211),
        (17, 212),
        (17, 213),
        (17, 214),
        (17, 74); -- supp features

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
VALUES  (18, 12), -- unkonwn
        (18, 13), -- unavailable
        (18, 28), -- open
        (18, 29), -- opening
        (18, 36),
        (18, 37),
        (18, 38),
        (18, 39),
        (18, 40);

-- ATTRIBUTES --
INSERT INTO integration_values(i_id, pv_id)
VALUES  (18, 70), -- code_format num
        (18, 71), -- code_format text
        (18, 72), -- changed_by 
        (18, 74); -- supp features

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
VALUES  (19, 12), -- unknown
        (19, 13), -- unavailable
        (19, 14), -- on
        (19, 15), -- off
        (19, 16), -- idle
        (19, 34), -- paused
        (19, 41),
        (19, 42),
        (19, 43);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (215,   'volume_level',         'float'),              --The volume level of the media player in the range (0..1).
        (216,   'is_volume_muted',      'bool'),                --Its true if volume is currently muted.
        (217,   'volume_step',          'float'),               --The volume step to use for the volume_up and volume_down services.
        (218,   'media_content_id',     'string'),              --The content ID of current playing media.
        (219,   'media_content_type',   'album'),               --The content type of current playing media.
        (220,   'media_content_type',   'app'),                  --The content type of current playing media.
        (221,   'media_content_type',   'artist'),              --The content type of current playing media.
        (222,   'media_content_type',   'channel'),             --The content type of current playing media.
        (223,   'media_content_type',   'channels'),            --The content type of current playing media.
        (224,   'media_content_type',   'composer'),            --The content type of current playing media.
        (225,   'media_content_type',   'contibuting_artist'),  --The content type of current playing media.
        (226,   'media_content_type',   'episode'),             --The content type of current playing media.
        (227,   'media_content_type',   'game'),                --The content type of current playing media.
        (228,   'media_content_type',   'genre'),               --The content type of current playing media.
        (229,   'media_content_type',   'image'),               --The content type of current playing media.
        (230,   'media_content_type',   'movie'),               --The content type of current playing media.
        (231,   'media_content_type',   'music'),               --The content type of current playing media.
        (232,   'media_content_type',   'playlist'),            --The content type of current playing media.
        (233,   'media_content_type',   'podcast'),             --The content type of current playing media.
        (234,   'media_content_type',   'season'),              --The content type of current playing media.
        (235,   'media_content_type',   'track'),               --The content type of current playing media.
        (236,   'media_content_type',   'tvshow'),              --The content type of current playing media.
        (237,   'media_content_type',   'url'),                 --The content type of current playing media.
        (238,   'media_content_type',   'video'),               --The content type of current playing media.
        (239,   'app_name',             'string'),              --The name of the current running app.
        (240,   'group_members',        'list[string]'),        --A dynamic list of player entities which are currently grouped together for synchronous playback.
        (241,   'media_album_artist',   'string'),              --The album artist of current playing media, music track only.
        (242,   'media_album_name',     'string'),              --The album name of current playing media, music track only.
        (243,   'media_artist',         'string'),              --The artist of current playing media, music track only.
        (244,   'media_channel',        'string'),              --The channel currently playing.
        (245,   'media_duration',       'int'),                 --The duration of current playing media in seconds.
        (246,   'media_episode',        'string'),              --The episode of current playing media, TV show only.
        (247,   'media_playlist',       'string'),              --The duration of current playing media in seconds.
        (248,   'media_position',       'int'),                 --The episode of current playing media, TV show only
        (249,   'media_season',         'string'),              --The duration of current playing media in seconds.
        (250,   'media_series_title',   'string'),              --The episode of current playing media, TV show only
        (251,   'media_title',          'string'),              --The duration of current playing media in seconds.
        (252,   'media_track',          'int'),                 --The track number of current playing media, music track only.
        (253,   'repeat',               'off'),                 --The current repeat mode.
        (254,   'repeat',               'one'),                 --The current repeat mode.
        (255,   'repeat',               'all'),                 --The current repeat mode.
        (256,   'shuffle',              'bool'),                --True if shuffle is enabled.
        (257,   'source',               'dvd'),                 --The currently selected input source for the media player.
        (258,   'source',               'youtube'),             --The currently selected input source for the media player.
        (259,   'sound_mode',           'music'),               --The current sound mode of the media player.
        (260,   'sound_mode',           'movie'),               --The current sound mode of the media player.
        (261,   'device_class',         'tv'),                  --The media player is a tv.
        (262,   'device_class',         'speaker'),             --The media player is a speaker.
        (263,   'device_class',         'receiver');            --The media player is a receiver.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (19, 215),
        (19, 216),
        (19, 217),
        (19, 218),
        (19, 219),
        (19, 220),
        (19, 221),
        (19, 222),
        (19, 223),
        (19, 224),
        (19, 225),
        (19, 226),
        (19, 227),
        (19, 228),
        (19, 229),
        (19, 230),
        (19, 231),
        (19, 232),
        (19, 233),
        (19, 234),
        (19, 235),
        (19, 236),
        (19, 237),
        (19, 238),
        (19, 239),
        (19, 240),
        (19, 241),
        (19, 242),
        (19, 243),
        (19, 244),
        (19, 245),
        (19, 246),
        (19, 247),
        (19, 248),
        (19, 249),
        (19, 250),
        (19, 251),
        (19, 252),
        (19, 253),
        (19, 254),
        (19, 255),
        (19, 256),
        (19, 257),
        (19, 258),
        (19, 259),
        (19, 260),
        (19, 261),
        (19, 262),
        (19, 263),
        (19, 74); -- supp features

/* notify
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/notify
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/notify
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (20, 12), -- unknown
        (20, 13); -- unavailable

-- ATTRIBUTES --
INSERT INTO integration_values(i_id, pv_id)
VALUES  (20, 74); -- supp features

/* number
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/number
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (44,    'main',     'float');                   --The number of the entity.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (21, 12), -- unknown
        (21, 13), -- unavailable
        (21, 44);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (264,   'min',                  'float'),      --The minimum accepted value in the number's (inclusive).
        (265,   'max',                  'float'),       --The maximum accepted value in the number's (inclusive).
        (266,   'step',                 'float'),       --Defines the resolution of the values, i.e. the smallest increment or decrement in the number's.
        (267,   'mode',                 'string');      --Defines how the number should be displayed in the UI. Can be box, slider or auto.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (21, 264),
        (21, 265),
        (21, 266),
        (21, 267);

/* remote
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/remote
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/remote
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (22, 12), -- unknown
        (22, 13), -- unavailable
        (22, 25); -- url as string

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (268,   'activity',             'string'),      --The minimum accepted value in the number's (inclusive).
        (269,   'current_activity',     'string');      --The maximum accepted value in the number's (inclusive).


INSERT INTO integration_values(i_id, pv_id)
VALUES  (22, 268),
        (22, 269);

/* scene
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/scene
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/scene/__init__.py
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (23, 12), -- unknown
        (23, 13), -- unavailable
        (23, 25); -- scentence as string

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (270,   'id',                   'string'),      --The id of the scene.
        (271,   'entity_id',            'string');      --The id of the entity in the scene.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (23, 270),
        (23, 271);

/* select
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/select
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/select
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (45,    'main', 	'option');      --The one of the options of the select.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (24, 12), -- unknown
        (24, 13), -- unavailable
        (24, 45);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (272,   'options',              'list[string]');        --All options of the select.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (24, 272);

/* sensor_float
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/sensor
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/sensor
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (25, 12), -- unknown
        (25, 13), -- unavailable
        (25, 44); -- value as float

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (273,   'device_class',         'apparent_power'),                      --The device class of the sensor.
        (274,   'device_class',         'aqi'),                                 --The device class of the sensor.
        (275,   'device_class',         'atmospheric_pressure'),                --The device class of the sensor.
        (276,   'device_class',         'conductivity'),                        --The device class of the sensor.
        (277,   'device_class',         'carbon_dioxide'),                      --The device class of the sensor.
        (278,   'device_class',         'carbon_monoxide'),                     --The device class of the sensor.
        (279,   'device_class',         'current'),                             --The device class of the sensor.
        (280,   'device_class',         'data_rate'),                           --The device class of the sensor.
        (281,   'device_class',         'data_size'),                           --The device class of the sensor.
        (282,   'device_class',         'distance'),                            --The device class of the sensor.
        (283,   'device_class',         'duration'),                            --The device class of the sensor.
        (284,   'device_class',         'energy'),                              --The device class of the sensor.
        (285,   'device_class',         'energy_storage'),                      --The device class of the sensor.
        (286,   'device_class',         'frequency'),                           --The device class of the sensor.
        (287,   'device_class',         'humidity'),                            --The device class of the sensor.
        (288,   'device_class',         'illuminance'),                         --The device class of the sensor.
        (289,   'device_class',         'irradiance'),                          --The device class of the sensor.
        (290,   'device_class',         'monetary'),                            --The device class of the sensor.
        (291,   'device_class',         'nitrogen_dioxide'),                    --The device class of the sensor.
        (292,   'device_class',         'nitrogen_monoxide'),                   --The device class of the sensor.
        (293,   'device_class',         'nitrous_oxide'),                       --The device class of the sensor.
        (294,   'device_class',         'ozone'),                               --The device class of the sensor.
        (295,   'device_class',         'ph'),                                  --The device class of the sensor.
        (296,   'device_class',         'pm1'),                                 --The device class of the sensor.
        (297,   'device_class',         'pm10'),                                --The device class of the sensor.
        (298,   'device_class',         'pm25'),                                --The device class of the sensor.
        (299,   'device_class',         'power_factor'),                        --The device class of the sensor.
        (300,   'device_class',         'precipitation'),                       --The device class of the sensor.
        (301,   'device_class',         'precipitation_intensity'),             --The device class of the sensor.
        (302,   'device_class',         'pressure'),                            --The device class of the sensor.
        (303,   'device_class',         'reactive_power'),                      --The device class of the sensor.
        (304,   'device_class',         'signal_strength'),                     --The device class of the sensor.
        (305,   'device_class',         'sound_pressure'),                      --The device class of the sensor.
        (306,   'device_class',         'speed'),                               --The device class of the sensor.
        (307,   'device_class',         'sulphur_dioxide'),                     --The device class of the sensor.
        (308,   'device_class',         'temperature'),                         --The device class of the sensor.
        (309,   'device_class',         'volatile_organic_compounds'),          --The device class of the sensor.
        (310,   'device_class',         'volatile_organic_compounds_parts'),    --The device class of the sensor.
        (311,   'device_class',         'voltage'),                             --The device class of the sensor.
        (312,   'device_class',         'volume'),                              --The device class of the sensor.
        (313,   'device_class',         'volume_storage'),                      --The device class of the sensor.
        (314,   'device_class',         'volume_flow_rate'),                    --The device class of the sensor.
        (315,   'device_class',         'water'),                               --The device class of the sensor.
        (316,   'device_class',         'weight'),                              --The device class of the sensor.
        (317,   'device_class',         'wind_speed'),                          --The device class of the sensor.
        (318,   'unit_of_measurement',  'string'),                              --The unit of the sensor value.
        (319,   'battery_level',        'int');                                 --The battery level of the sensor.
        
INSERT INTO integration_values(i_id, pv_id)
VALUES  (25, 273),
        (25, 274),
        (25, 275),
        (25, 276),
        (25, 277),
        (25, 278),
        (25, 279),
        (25, 280),
        (25, 281),
        (25, 282),
        (25, 283),
        (25, 284),
        (25, 285),
        (25, 286),
        (25, 287),
        (25, 288),
        (25, 289),
        (25, 290),
        (25, 291),
        (25, 292),
        (25, 293),
        (25, 294),
        (25, 295),
        (25, 296),
        (25, 297),
        (25, 298),
        (25, 299),
        (25, 300),
        (25, 301),
        (25, 302),
        (25, 303),
        (25, 304),
        (25, 305),
        (25, 306),
        (25, 307),
        (25, 308),
        (25, 309),
        (25, 310),
        (25, 311),
        (25, 312),
        (25, 313),
        (25, 314),
        (25, 315),
        (25, 316),
        (25, 317),
        (25, 318),
        (25, 319),
        (25, 75), -- device_class battery
        (25, 82), -- device_class gas
        (25, 86), -- device_class moisture
        (25, 92); -- device_class power

/* sensor_string
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/sensor
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/sensor
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (26, 12), -- unknown
        (26, 13), -- unavailable
        (26, 25); -- values as string

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (320,   'device_class',         'date'),                                --The device class of the sensor.
        (321,   'device_class',         'timestamp');                           --The device class of the sensor.
        
INSERT INTO integration_values(i_id, pv_id)
VALUES  (26, 320),
        (26, 321);

/* sensor_enum
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/sensor
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/sensor
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (27, 12), -- unknown
        (27, 13), -- unavailable
        (27, 45); -- option

-- ATTRIBUTES --
INSERT INTO integration_values(i_id, pv_id)
VALUES  (27, 272); --All options of the sensor.

/* siren
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/siren
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/siren
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (28, 12), -- unknown
        (28, 13), -- unavailable
        (28, 14), -- on
        (28, 15); -- off

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (322,   'available_tones',      'list[string]');        --The list of possible sounds for the siren.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (28, 322),
        (28, 74); --supp features

/* stt
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/stt
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/stt
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (29, 12), -- unknown
        (29, 13); -- unavailable

/* switch
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/switch
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (30, 12), -- unknown
        (30, 13), -- unavailable
        (30, 14), -- on
        (30, 15); -- off

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (323,   'device_class',         'switch'),      --The device class of the switch.
        (324,   'device_class',         'outlet');      --The device class of the switch.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (30, 323),
        (30, 324);

/* text
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/text
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (31, 12), -- unknown
        (31, 13), -- unavailable
        (31, 25); -- text as string

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (325,   'mode',                 'text'),        --The text ui mode.
        (326,   'mode',                 'password'),    --The text ui mode.
        (327,   'pattern',              'string');      --A regex pattern that the text value must match to be valid.


INSERT INTO integration_values(i_id, pv_id)
VALUES  (31, 325),
        (31, 326),
        (31, 327),
        (31, 264), -- min
        (31, 265); -- max

/* time
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/time
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (32, 12), -- unknown
        (32, 13), -- unavailable
        (32, 25); -- time as string

/* todo
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/todo
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (46,    'main',         'int');           --A TodoListEntity state is the count of incomplete items in the To-do list.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (33, 12), -- unknown
        (33, 13), -- unavailable
        (33, 46);

-- ATTRIBUTES --
INSERT INTO integration_values(i_id, pv_id)
VALUES  (33, 74); -- supp features

/* tts
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/tts
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (34, 12), -- unknown
        (34, 13); -- unavailable

/* update
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/update
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/update
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (35, 12), -- unknown
        (35, 13), -- unavailable
        (35, 14), -- on
        (35, 15); -- off

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (328,   'auto_update',          'bool'),        --The device or service that the entity represents has auto update logic. When this is set to True you can not skip updates.
        (329,   'installed_version',    'string'),      --The currently installed and used version of the software.
        (330,   'in_progress',          'int'),         --Update installation progress. Can either return a boolean (1 if in progress, 0 if not) or an int to indicate the progress from 0 to 100%.
        (331,   'release_summary',      'string'),      --Summary of the release notes or changelog.
        (332,   'release_url',          'string'),      --URL to the full release notes of the latest version available.
        (333,   'current_version',      'string'),      --The current version of the update.
        (334,   'skipped_version',      'string'),      --The version that was skipped.
        (335,   'title',                'string'),      --Title of the software.
        (336,   'latest_version',       'string'),      --The latest version of the software available.
        (337,   'device_class',         'firmware');    --The device class of the update.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (35, 328),
        (35, 329),
        (35, 330),
        (35, 331),
        (35, 332),
        (35, 333),
        (35, 334),
        (35, 335),
        (35, 336),
        (35, 337),
        (35, 74);--supp features

/* vacuum
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/vacuum
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (47,    'main',     'cleaning'),                --The vacuum is cleaning.
        (48,    'main',     'returning');               --The vacuum is returning to the dock.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (36, 12), -- unknown
        (36, 13), -- unavailable
        (36, 16), -- idle
        (36, 33), -- docked
        (36, 34), -- paused
        (36, 35), -- error
        (36, 47),
        (36, 48);
        

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (338,   'battery_icon',         'string'),      --The time the vacuum has been cleaning.
        (339,   'cleaned_area',         'float'),       --The percentage of the area that has been cleaned.
        (340,   'fan_speed',            'min'),         --The speed of the vacuum fan.
        (341,   'fan_speed',            'medium'),      --The speed of the vacuum fan.
        (342,   'fan_speed',            'high'),        --The speed of the vacuum fan.
        (343,   'fan_speed',            'max');         --The speed of the vacuum fan.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (36, 319), -- battery_level
        (36, 338),
        (36, 339),
        (36, 340),
        (36, 341),
        (36, 342),
        (36, 343),
        (36, 74);--supp features

/* valve
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/valve
        https://www.home-assistant.io/integrations/valve/
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (37, 12), -- unknown
        (37, 13), -- unavailable
        (37, 26), -- closed
        (37, 27), -- closing
        (37, 28), -- open
        (37, 29); -- opening

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (344,   'current_position',     'int');         --The current position of the valve.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (37, 82), -- device_class gas
        (37, 315), -- device_class water
        (37, 344);

/* wake_word
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/wake_word
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (38, 12), -- unknown
        (38, 13), -- unavailable
        (38, 25); -- wake word as string

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
VALUES  (39, 12), -- unknown
        (39, 13), -- unavailable
        (39, 15), -- off
        (39, 21), -- heat
        (39, 49),
        (39, 50),
        (39, 51),
        (39, 52),
        (39, 53),
        (39, 54);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (345,   'operation_mode',       'eco'),         --The operation mode of the water heater.
        (346,   'operation_mode',       'electric'),    --The operation mode of the water heater.
        (347,   'operation_mode',       'performance'), --The operation mode of the water heater.
        (348,   'operation_mode',       'high_demand'), --The operation mode of the water heater.
        (349,   'operation_mode',       'heat_pump'),   --The operation mode of the water heater.
        (350,   'operation_mode',       'gas'),         --The operation mode of the water heater.
        (351,   'operation_mode',       'off'),         --The operation mode of the water heater.
        (352,   'away_mode',            'on'),          --The away mode of the water heater.
        (353,   'away_mode',            'off');         --The away mode of the water heater.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (39, 116), --min_temp
        (39, 114), --max_temp
        (39, 112), --curr_temp
        (39, 119), --temp
        (39, 120), --target_temp_high
        (39, 121), --target_temp_low
        (39, 345),
        (39, 346),
        (39, 347),
        (39, 348),
        (39, 349),
        (39, 350),
        (39, 351),
        (39, 352),
        (39, 353),
        (39, 74);--supp feat

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
VALUES  (40, 12), -- unknown
        (40, 13), -- unavailable
        (40, 15), -- off
        (40, 21), -- heat
        (40, 55),
        (40, 56),
        (40, 57),
        (40, 58),
        (40, 59),
        (40, 60),
        (40, 61),
        (40, 62),
        (40, 63),
        (40, 64),
        (40, 65),
        (40, 66),
        (40, 67),
        (40, 68),
        (40, 69);

-- ATTRIBUTES --
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (354,   'attribution',          'string'),      --The attributor of the weather.
        (355,   'apparent_temperature', 'float'),       --The current apparent (feels-like) temperature in °C or °F.
        (356,   'pressure',             'flaot'),       --The pressure of the weather.
        (357,   'pressure_unit',        'string'),      --The pressure unit of the weather.
        (358,   'wind_speed',           'float'),       --The wind bearing of the weather.
        (359,   'wind_speed_unit',      'string'),      --The wind speed unit of the weather.
        (360,   'wind_bearing',         'string'),      --The current wind bearing in azimuth angle (degrees) or 1-3 letter cardinal direction.
        (361,   'wind_gust_speed',      'float'),       --he current wind gust speed.
        (362,   'visibility',           'float'),       --The visibility of the weather.
        (363,   'visibility_unit',      'string'),      --The visibility unit of the weather.
        (364,   'cloud_coverage',       'int'),         --The cloud coverage of the weather.
        (365,   'dew_point',            'float'),        --The dew point temperature in °C or °F.
        (366,   'ozone',                'float'),       --The current ozone level of the weather.
        (367,   'uv_index',             'float'),       --The uv index of the weather.
        (368,   'precipitation_unit',   'string');      -- The precipitation unit in mm or in.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (40, 118),--humidity
        (40, 119),--temperature
        (40, 123),--temperature_unit
        (40, 354),
        (40, 355),
        (40, 356),
        (40, 357),
        (40, 358),
        (40, 359),
        (40, 360),
        (40, 361),
        (40, 362),
        (40, 363),
        (40, 364),
        (40, 365),
        (40, 366),
        (40, 367),
        (40, 368),
        (40, 74);--supp feat

-- TRIGGER INTEGRATION
/* import the integrations for triggers */

INSERT INTO integration(i_id, i_name)
VALUES  (41, 'homeassistant'),
        (42, 'mqtt'),
        (43, 'sun'),
        (44, 'tag'),
        (45, 'time_pattern'),
        (46, 'persistent_notification'),
        (47, 'webhook'),
        (48, 'zone'),
        (49, 'device'),

/* homeassistant
        attributes extracted from trigger: automation_dissection.py
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (   ,   'event'                 'string'),      --Triggered with this event

INSERT INTO integration_values(i_id, pv_id)



/* sun
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/sun/
*/
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (369,    'main',     'above_horizon'),          --The sun is above the horizon.
        (370,    'main',     'below_horizon');           --The sun is below the horizon.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (42, 12), -- unknown
        (42, 13), -- unavailable
        (42, 369),
        (42, 370);

--- ATTRIBUTES ---
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (371,   'azimuth',              'float'),       --The azimuth of the sun.
        (372,   'elevation',            'float'),       --The elevation of the sun.
        (373,   'next_dawn',            'string'),      --The next dawn time.
        (374,   'next_dusk',            'string'),      --The next dusk time.
        (375,   'next_midnight',        'string'),      --The next midnight time.
        (376,   'next_noon',            'string'),      --The next noon time.
        (377,   'next_rising',          'string'),      --The next rising time.
        (378,   'next_setting',         'string'),      --The next setting time.
        (379,   'rising',               'bool');        --The sun is rising.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (42, 371),
        (42, 372),
        (42, 373),
        (42, 374),
        (42, 375),
        (42, 376),
        (42, 377),
        (42, 378),
        (42, 379);
        
/* tag
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/tag/
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (43, 12), -- unknown
        (43, 13), -- unavailable
        (43, 25); -- date of the last use as string

--- ATTRIBUTES ---
INSERT INTO possible_values(pv_id, property, p_value)
VALUES  (377,   'last_scanned_by_device_id',    'string'),      --The id of the device that last scanned the tag.
        (378,   'tag_id',                       'string');      --The id of the tag.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (43, 377),
        (43, 378);




