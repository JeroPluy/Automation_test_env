-- TODO remove the following lines
-- DELETE FROM integration_values;  
-- DELETE FROM possible_values;
-- DELETE FROM integration; 

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
        (40,    'weather');


-- POSSIBLE VALUES --
/* import the values from standard integrations */

INSERT INTO possible_values(pv_id, property, p_value)
VALUES  
/* alarm_control_panel 
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/alarm-control-panel
*/
        (1  ,       'main',                             'None'),	                        -- Unknown state.
        (2  ,       'main',                             'disarmed'),	                        -- The alarm is disarmed (off).
        (3  ,       'main',                             'armed_home'),	                        -- The alarm is armed in home mode.
        (4  ,       'main',                             'armed_away'),	                        -- The alarm is armed in away mode.
        (5  ,       'main',                             'armed_night'),	                        -- The alarm is armed in night mode.
        (6  ,       'main',                             'armed_vacation'),	                -- The alarm is armed in vacation mode.
        (7  ,       'main',                             'armed_custom_bypass'),                 -- The alarm is armed in bypass mode.
        (8  ,       'main',                             'pending'),	                        -- The alarm is pending (towards triggered).
        (9  ,       'main',                             'arming'),	                        -- The alarm is arming.
        (10 ,       'main',                             'disarming'),	                        -- The alarm is disarming.
        (11 ,       'main',                             'triggered'),                           -- The alarm is triggered.
        (12 ,       'main',                             'unknown'),	                        -- Unknown state.
        (13 ,       'main',                             'unavailable'),                         -- The entity is not reachable.
        (14 ,       'code_format',                      'number'),                              -- The code format of the alarm control panel.
        (15 ,       'code_format',                      'text'),                                -- The code format of the alarm control panel.
        (16 ,       'changed_by',                       'string'),                              -- The alarm control panel got changed by a user.
        (17 ,       'code_arm_required',                'string'),                              -- The code required to arm the alarm control panel.
        (18 ,       'supported_features',               'int'),                                 -- The count of supported features of the alarm control panel.
/* time
        attribute extracted from: 
        environment_package/automation_dissection.py
*/
        (19,       'at',                               'string'),                              -- Time at which it throws an event
/* binary_sensor 
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/binary-sensor
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/binary_sensor
*/
        (20 ,       'main',                             'on'),                                  -- The sensor detects something.
        (21 ,       'main',                             'off'),                                 -- The sensor detects nothing.
        (22 ,       'device_class',                     'battery'),                             -- The device class of the binary sensor.
        (23 ,       'device_class',                     'battery_charging'),                    -- The device class of the binary sensor.
        (24 ,       'device_class',                     'co'),                                  -- The device class of the binary sensor.
        (25 ,       'device_class',                     'cold'),                                -- The device class of the binary sensor.
        (26 ,       'device_class',                     'connectivity'),                        -- The device class of the binary sensor.
        (27 ,       'device_class',                     'door'),                                -- The device class of the binary sensor.
        (28 ,       'device_class',                     'garage_door'),                         -- The device class of the binary sensor.
        (29 ,       'device_class',                     'gas'),                                 -- The device class of the binary sensor.
        (30 ,       'device_class',                     'heat'),                                -- The device class of the binary sensor.
        (31 ,       'device_class',                     'light'),                               -- The device class of the binary sensor.
        (32 ,       'device_class',                     'lock'),                                -- The device class of the binary sensor.
        (33 ,       'device_class',                     'moisture'),                            -- The device class of the binary sensor.
        (34 ,       'device_class',                     'motion'),                              -- The device class of the binary sensor.
        (35 ,       'device_class',                     'moving'),                              -- The device class of the binary sensor.
        (36 ,       'device_class',                     'occupancy'),                           -- The device class of the binary sensor.
        (37 ,       'device_class',                     'opening'),                             -- The device class of the binary sensor.
        (38 ,       'device_class',                     'plug'),                                -- The device class of the binary sensor.
        (39 ,       'device_class',                     'power'),                               -- The device class of the binary sensor.
        (40 ,       'device_class',                     'presence'),                            -- The device class of the binary sensor.
        (41 ,       'device_class',                     'problem'),                             -- The device class of the binary sensor.
        (42 ,       'device_class',                     'running'),                             -- The device class of the binary sensor.
        (43 ,       'device_class',                     'safety'),                              -- The device class of the binary sensor.
        (44 ,       'device_class',                     'smoke'),                               -- The device class of the binary sensor.
        (45 ,       'device_class',                     'sound'),                               -- The device class of the binary sensor.
        (46 ,       'device_class',                     'tamper'),                              -- The device class of the binary sensor.
        (47 ,       'device_class',                     'update'),                              -- The device class of the binary sensor.
        (48 ,       'device_class',                     'vibration'),                           -- The device class of the binary sensor.
        (49 ,       'device_class',                     'window'),                              -- The device class of the binary sensor.
/* calendar
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/calendar
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/calendar
*/
        (50 ,       'description',                      'string'),                              -- The calender description.
        (51 ,       'message',                          'string'),                              -- The calender message.
        (52 ,       'all_day',                          'string'),                              -- The calender event is all day
        (53 ,       'start_time',                       'string'),                              -- The calender event start time
        (54 ,       'end_time',                         'string'),                              -- The calender event end time.
        (55 ,       'location',                         'string'),                              -- The calender event location.
        (56 ,       'event',                            'string'),                              -- Triggered with this event
        (57 ,       'offset',                           'string'),                              -- Offset of the trigger 
/* camera 
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/camera
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/camera
*/
        (58 ,       'main',                             'idle'),                                -- The camera observes.
        (59 ,       'main',                             'recording'),                           -- The camera records the recording.
        (60 ,       'main',                             'streaming'),                           -- The camera streams the recording.
        (61 ,       'frontend_stream_type',             'hls'),                                 -- The streaming format in the ui of the camera.
        (62 ,       'frontend_stream_type',             'web_rtc'),                             -- The streaming format in the ui of the camera.
/* climate  
        states(main) / attributes extracted from:
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/climate
        https://www.home-assistant.io/integrations/climate.mqtt/ 
        https://www.home-assistant.io/integrations/climate/
        https://developers.home-assistant.io/docs/core/entity/climate/
*/
        (63 ,       'main',                             'auto'),                                -- The device is set to a schedule, learned behavior, AI.
        (64 ,       'main',                             'cool'),                                -- The device is set to cool to a target temperature.
        (65 ,       'main',                             'heat'),                                -- The device is set to heat to a target temperature.
        (66 ,       'main',                             'heat_cool'),                           -- The device is set to heat/cool to a target temperature range.
        (67 ,       'main',                             'dry'),                                 -- The device is set to dry/humidity mode.
        (68 ,       'main',                             'fan_only'),                            -- The device only has the fan on. No heating or cooling taking place.
        (69 ,       'current_humidity',                 'float'),                               -- The current humidity.
        (70 ,       'current_temperature',              'float'),                               -- The current temperature.
        (71 ,       'max_humidity',                     'float'),                               -- The maximum humidity.
        (72 ,       'max_temp',                         'float'),                               -- The maximum temperature in temperature_unit.
        (73 ,       'min_humidity',                     'float'),                               -- The minimum humidity.
        (74 ,       'min_temp',                         'float'),                               -- The minimum temperature in temperature_unit.
        (75 ,       'precision',                        'float'),                               -- The precision of the temperature in the system. Defaults to tenths for TEMP_CELSIUS, whole number otherwise.
        (76 ,       'humidity',                         'float'),                               -- The target humidity the device is trying to reach.
        (77 ,       'temperature',                      'float'),                               -- The temperature currently set to be reached.
        (78 ,       'target_temp_high',                 'float'),                               -- The upper bound target temperature.
        (79 ,       'target_temp_low',                  'float'),                               -- The lower bound target temperature
        (80 ,       'target_temp_step',                 'int'),                                 -- The supported step size a target temperature can be increased or decreased
        (81 ,       'temperature_unit',                 'string'),                              -- The unit of temperature measurement for the system (TEMP_CELSIUS or TEMP_FAHRENHEIT).
        (82 ,       'hvac_action',                      'preheating'),                          -- Device is preheating.
        (83 ,       'hvac_action',                      'heating'),                             -- Device is heating.
        (84 ,       'hvac_action',                      'cooling'),                             -- Device is cooling.
        (85 ,       'hvac_action',                      'drying'),                              -- Device is drying.
        (86 ,       'hvac_action',                      'fan'),                                 -- Device has fan on.
        (87 ,       'hvac_action',                      'defrosting'),                          -- Device is defrosting.
        (88 ,       'hvac_action',                      'off'),                                 -- Device is off.
        (89 ,       'hvac_action',                      'idle'),                                -- Device is doing nothing.        
        (90 ,       'fan_mode',                         'on'),                                  -- The fan on.
        (91 ,       'fan_mode',                         'off'),                                 -- The fan off.
        (92 ,       'fan_mode',                         'auto_high'),                           -- The fan turns on automatically high.
        (93 ,       'fan_mode',                         'auto_low'),                            -- The fan turns on automatically low.
        (94 ,       'fan_mode',                         'on_low'),                              -- The fan speed is low.
        (95 ,       'fan_mode',                         'on_medium'),                           -- The fan speed is medium.
        (96 ,       'fan_mode',                         'on_high'),                             -- The fan speed is high.
        (97 ,       'fan_mode',                         'middle'),                              -- The fan stayes in the middle.
        (98 ,       'fan_mode',                         'focus'),                               -- The fan focuses in on direction.
        (99 ,       'fan_mode',                         'diffuse'),                             -- The fan diffuse in all possible directions.
        (100,       'swing_mode',                       'off'),                                 -- The fan don't swing.
        (101,       'swing_mode',                       'auto'),                                -- The fan swings automatically.
        (102,       'swing_mode',                       '1'),                                   -- The fan swings with speed 1.
        (103,       'swing_mode',                       '2'),                                   -- The fan swings with speed 2.
        (104,       'swing_mode',                       '3'),                                   -- The fan swings with speed 3.
        (105,       'swing_mode',                       'vertical'),                            -- The fan swings vertically.
        (106,       'swing_mode',                       'horizontal'),                          -- The fan swings horizontally.
        (107,       'swing_mode',                       'both'),                                -- The fan swings in both directions.
/* conversation 
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/conversation/
        https://developers.home-assistant.io/docs/core/entity/conversation
*/
        (108,       'main',                             'string'),                              -- Date of the last call in the converstation.
        (109,       'command',                          'string'),                              -- The command to trigger the event
/* cover
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/cover
*/
        (110,       'main',                             'closed'),                              -- The cover has reach the closed position.
        (111,       'main',                             'closing'),                             -- The cover is in the process of closing to reach a set position.
        (112,       'main',                             'open'),                                -- The cover has reached the open position.
        (113,       'main',                             'opening'),                             -- The cover is in the process of opening to reach a set position.
        (114,       'device_class',                     'awning'),                              -- The device class of the binary sensor.
        (115,       'device_class',                     'blind'),                               -- The device class of the binary sensor.
        (116,       'device_class',                     'curtain'),                             -- The device class of the binary sensor.
        (117,       'device_class',                     'damper'),                              -- The device class of the binary sensor.
        (118,       'device_class',                     'garage'),                              -- The device class of the binary sensor.
        (119,       'device_class',                     'gate'),                                -- The device class of the binary sensor.
        (120,       'device_class',                     'shade'),                               -- The device class of the binary sensor.               
        (121,       'device_class',                     'sutter'),                              -- The device class of the binary sensor.
/* device_tracer
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/device-tracker
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/device_tracker
*/
        (122,       'main',                             'home'),                                -- The device is home.
        (123,       'main',                             'not_home'),                            -- The cover is not home.
        (124,       'source_type',                      'gps'),                                 -- The source of the device connection.
        (125,       'source_type',                      'router'),                              -- The source of the device connection.
        (126,       'source_type',                      'bluetooth'),                           -- The source of the device connection.
        (127,       'source_type',                      'bluetooth_le'),                        -- The source of the device connection.
        (128,       'longitude',                        'float'),                               -- The coordinates of the device.
        (129,       'latitude',                         'float'),                               -- The coordinates of the device.
        (130,       'location_accuracy',                'string'),                              -- The coordinate accuracy of the device.
        (131,       'battery',                          'int'),                                 -- The battery level of the device.
/* event
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/event
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/event
        https://www.home-assistant.io/docs/configuration/events/
*/
        (132,       'event_type',                       'pressed'),                             -- The event of a button press.
        (133,       'event_type',                       'call_service'),                        -- The event of a service called.
        (134,       'event_type',                       'component_loaded'),                    -- The event of component loaded.
        (135,       'event_type',                       'core_config_updated'),                 -- The event of update the core config.
        (136,       'event_type',                       'data_entry_flow_progressed'),          -- The event of data entry flow progresses.
        (137,       'event_type',                       'homeassistant_start'),                 -- The event of home assistant starting.
        (138,       'event_type',                       'homeassistant_started'),               -- The event ofhome assistant started.
        (139,       'event_type',                       'homeassistant_stop'),                  -- The event home assistant stopped.
        (140,       'event_type',                       'homeassistant_final_write'),           -- The event home assistant makes it final write befor shutting down.
        (141,       'event_type',                       'logbook_entry'),                       -- The event of making a logbook entry.
        (142,       'event_type',                       'service_registered'),                  -- The event of register a new service.
        (143,       'event_type',                       'service_removed'),                     -- The event of removing a service.
        (144,       'event_type',                       'state_changed'),                       -- The event of state change of an entity.
        (145,       'event_type',                       'themes_updated'),                      -- The event of the theme change in the ui.
        (146,       'event_type',                       'user_added'),                          -- The event for a new user.
        (147,       'event_type',                       'user_removed'),                        -- The event to remove a user.
        (148,       'event_type',                       'automation_reloaded'),                 -- The event of reloading the automation.yaml files.
        (149,       'event_type',                       'automation_triggered'),                -- The event of triggering an automation.
        (150,       'event_type',                       'scene_reloaded'),                      -- The event of reload a scene. 
        (151,       'event_type',                       'script_started'),                      -- The event of the start of a script.
        (152,       'event_type',                       'area_registry_updated'),               -- The event of an area update.
        (153,       'event_type',                       'category_registry_updated'),           -- The event of a category registry update.
        (154,       'event_type',                       'device_registry_updated'),             -- The event of a device registry update.
        (155,       'event_type',                       'entity_registry_updated'),             -- The event of a entity registry update.
        (156,       'event_type',                       'string'),                              -- A custom event.
        (157,       'event_data',                       'dict'),                                -- Dict of additional event data
        (158,       'context',                          'dict'),                                -- Dict of additional event context
/* fan
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/fan
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/fan
*/
        (159,       'percentage',                       'int'),                                 -- The current speed percentage. Must be a value between 0 (off) and 100.
        (160,       'percentage_step',                  'int'),                                 -- The steps for the speed percentage. Must be a value between 1 and 100.
        (161,       'oscillating',                      'bool'),                                -- The if the fan is oscillating.
        (162,       'direction',                        'forward'),                             -- The fan spinns forward.
        (163,       'direction',                        'reverse'),                             -- The fan spinns reverse.
/* humidifier
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/humidifier
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/humidifier
*/
        (164,       'action',                           'off'),                                 -- The humidifier is off.
        (165,       'action',                           'idle'),                                -- The humidifier does nothing.
        (166,       'action',                           'humidifying'),                         -- The humidifier humidifying the air.
        (167,       'action',                           'drying'),                              -- The humidifier drying the air.
        (168,       'device_class',                     'humidifier'),                          -- The humidifier is a humidifier.
        (169,       'device_class',                     'dehumidifier'),                        -- The humidifier is a dehumidifier.
/* lawn_mower
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/lawn-mower
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/lawn_mower
*/
        (170,       'main',                             'mowing'), 	                        -- The lawn mower is currently mowing.
        (171,       'main',                             'docked'),	                        -- The lawn mower is done mowing and is currently docked.
        (172,       'main',                             'paused'),	                        -- The lawn mower was active and is now paused.
        (173,       'main',                             'error'),                               -- The lawn mower encountered an error while active and needs assistance.
/* light
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/light
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/light
*/
        (174,       'effect',                           'rainbow'),                             -- The light makes a rainbow effect.
        (175,       'effect',                           'none'),                                -- The light makes no effect.
        (176,       'min_color_temp_kelvin',            'int'),                                 -- The minimal color value.
        (177,       'max_color_temp_kelvin',            'int'),                                 -- The maximal color value.
        (178,       'color_mode',                       'color_temp'),                          -- The ui color setting.
        (179,       'color_mode',                       'hs'),                                  -- The ui color setting.
        (180,       'brightness',                       'int'),                                 -- The brightness of the light.
        (181,       'color_temp_kelvin',                'int'),                                 -- The color of the light as kelvin number.
        (182,       'hs_color',                         'tuple[float, float]'),                 -- The color of the light in hs-format.
        (183,       'rgb_color',                        'tuple[int, int, int]'),                -- The color of the light in rgb-format.
        (184,       'xy_color',                         'tuple[float, float]'),                 -- The color of the light in xy-format.
        (185,       'rgbw_color',                       'tuple[int, int, int, int]'),           -- The color of the light in rgbw-format.
        (186,       'rgbww_color',                      'tuple[int, int, int, int, int]'),      -- The color of the light in rgbww-format.
/* lock
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/lock
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/lock
*/
        (187,       'main',                             'jammed'),                              -- The lock is unabled to toggle.
        (188,       'main',                             'locked'),                              -- The lock is locked.
        (189,       'main',                             'locking'),                             -- The lock is looking.
        (190,       'main',                             'unlocked'),                            -- The lock is unlocked.
        (191,       'main',                             'unlocking'),                           -- The lock is unlooking.
/* media_player
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/media-player
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/media_player
*/
        (192,       'main',                             'playing'),                             -- The media player playimg something.
        (193,       'main',                             'standby'),                             -- The media player is in standby mode.
        (194,       'main',                             'buffering'),                           -- The media player buffering something.
        (195,       'volume_level',                     'float'),                               -- The volume level of the media player in the range (0..1).
        (196,       'is_volume_muted',                  'bool'),                                -- Its true if volume is currently muted.
        (197,       'volume_step',                      'float'),                               -- The volume step to use for the volume_up and volume_down services.
        (198,       'media_content_id',                 'string'),                              -- The content ID of current playing media.
        (199,       'media_content_type',               'album'),                               -- The content type of current playing media.
        (200,       'media_content_type',               'app'),                                 -- The content type of current playing media.
        (201,       'media_content_type',               'artist'),                              -- The content type of current playing media.
        (202,       'media_content_type',               'channel'),                             -- The content type of current playing media.
        (203,       'media_content_type',               'channels'),                            -- The content type of current playing media.
        (204,       'media_content_type',               'composer'),                            -- The content type of current playing media.
        (205,       'media_content_type',               'contibuting_artist'),                  -- The content type of current playing media.
        (206,       'media_content_type',               'episode'),                             -- The content type of current playing media.
        (207,       'media_content_type',               'game'),                                -- The content type of current playing media.
        (208,       'media_content_type',               'genre'),                               -- The content type of current playing media.
        (209,       'media_content_type',               'image'),                               -- The content type of current playing media.
        (210,       'media_content_type',               'movie'),                               -- The content type of current playing media.
        (211,       'media_content_type',               'music'),                               -- The content type of current playing media.
        (212,       'media_content_type',               'playlist'),                            -- The content type of current playing media.
        (213,       'media_content_type',               'podcast'),                             -- The content type of current playing media.
        (214,       'media_content_type',               'season'),                              -- The content type of current playing media.
        (215,       'media_content_type',               'track'),                               -- The content type of current playing media.
        (216,       'media_content_type',               'tvshow'),                              -- The content type of current playing media.
        (217,       'media_content_type',               'url'),                                 -- The content type of current playing media.
        (218,       'media_content_type',               'video'),                               -- The content type of current playing media.
        (219,       'app_name',                         'string'),                              -- The name of the current running app.
        (220,       'group_members',                    'list[string]'),                        -- A dynamic list of player entities which are currently grouped together for synchronous playback.
        (221,       'media_album_artist',               'string'),                              -- The album artist of current playing media, music track only.
        (222,       'media_album_name',                 'string'),                              -- The album name of current playing media, music track only.
        (223,       'media_artist',                     'string'),                              -- The artist of current playing media, music track only.
        (224,       'media_channel',                    'string'),                              -- The channel currently playing.
        (225,       'media_duration',                   'int'),                                 -- The duration of current playing media in seconds.
        (226,       'media_episode',                    'string'),                              -- The episode of current playing media, TV show only.
        (227,       'media_playlist',                   'string'),                              -- The duration of current playing media in seconds.
        (228,       'media_position',                   'int'),                                 -- The episode of current playing media, TV show only
        (229,       'media_season',                     'string'),                              -- The duration of current playing media in seconds.
        (230,       'media_series_title',               'string'),                              -- The episode of current playing media, TV show only
        (231,       'media_title',                      'string'),                              -- The duration of current playing media in seconds.
        (232,       'media_track',                      'int'),                                 -- The track number of current playing media, music track only.
        (233,       'repeat',                           'off'),                                 -- The current repeat mode.
        (234,       'repeat',                           'one'),                                 -- The current repeat mode.
        (235,       'repeat',                           'all'),                                 -- The current repeat mode.
        (236,       'shuffle',                          'bool'),                                -- True if shuffle is enabled.
        (237,       'source',                           'dvd'),                                 -- The currently selected input source for the media player.
        (238,       'source',                           'youtube'),                             -- The currently selected input source for the media player.
        (239,       'sound_mode',                       'music'),                               -- The current sound mode of the media player.
        (240,       'sound_mode',                       'movie'),                               -- The current sound mode of the media player.
        (241,       'device_class',                     'tv'),                                  -- The media player is a tv.
        (242,       'device_class',                     'speaker'),                             -- The media player is a speaker.
        (243,       'device_class',                     'receiver'),                            -- The media player is a receiver.
/* number
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/number
*/
        (244,       'main',                             'float'),                               -- The number of the entity.
        (245,       'min',                              'float'),                               -- The minimum accepted value in the number's (inclusive).
        (246,       'max',                              'float'),                               -- The maximum accepted value in the number's (inclusive).
        (247,       'step',                             'float'),                               -- Defines the resolution of the values, i.e. the smallest increment or decrement in the number's.
        (248,       'mode',                             'string'),                              -- Defines how the number should be displayed in the UI. Can be box, slider or auto.
/* remote
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/remote
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/remote
*/
        (249,       'activity',                         'string'),                              -- The minimum accepted value in the number's (inclusive).
        (250,       'current_activity',                 'string'),                              -- The maximum accepted value in the number's (inclusive).
/* scene
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/scene
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/scene/__init__.py
*/
        (251,       'id',                               'string'),                              -- The id of the scene.
        (252,       'entity_id',                        'string'),                              -- The id of the entity in the scene.
/* select
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/select
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/select
*/
        (253,       'main', 	                        'option'),                              -- The one of the options of the select.
        (254,       'options',                          'list[string]'),                        -- All options of the select.
/* sensor_float
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/sensor
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/sensor
*/
        (255,       'device_class',                     'apparent_power'),                      -- The device class of the sensor.
        (256,       'device_class',                     'aqi'),                                 -- The device class of the sensor.
        (257,       'device_class',                     'atmospheric_pressure'),                -- The device class of the sensor.
        (258,       'device_class',                     'conductivity'),                        -- The device class of the sensor.
        (259,       'device_class',                     'carbon_dioxide'),                      -- The device class of the sensor.
        (260,       'device_class',                     'carbon_monoxide'),                     -- The device class of the sensor.
        (261,       'device_class',                     'current'),                             -- The device class of the sensor.
        (262,       'device_class',                     'data_rate'),                           -- The device class of the sensor.
        (263,       'device_class',                     'data_size'),                           -- The device class of the sensor.
        (264,       'device_class',                     'distance'),                            -- The device class of the sensor.
        (265,       'device_class',                     'duration'),                            -- The device class of the sensor.
        (266,       'device_class',                     'energy'),                              -- The device class of the sensor.
        (267,       'device_class',                     'energy_storage'),                      -- The device class of the sensor.
        (268,       'device_class',                     'frequency'),                           -- The device class of the sensor.
        (269,       'device_class',                     'humidity'),                            -- The device class of the sensor.
        (270,       'device_class',                     'illuminance'),                         -- The device class of the sensor.
        (271,       'device_class',                     'irradiance'),                          -- The device class of the sensor.
        (272,       'device_class',                     'monetary'),                            -- The device class of the sensor.
        (273,       'device_class',                     'nitrogen_dioxide'),                    -- The device class of the sensor.
        (274,       'device_class',                     'nitrogen_monoxide'),                   -- The device class of the sensor.
        (275,       'device_class',                     'nitrous_oxide'),                       -- The device class of the sensor.
        (276,       'device_class',                     'ozone'),                               -- The device class of the sensor.
        (277,       'device_class',                     'ph'),                                  -- The device class of the sensor.
        (278,       'device_class',                     'pm1'),                                 -- The device class of the sensor.
        (279,       'device_class',                     'pm10'),                                -- The device class of the sensor.
        (280,       'device_class',                     'pm25'),                                -- The device class of the sensor.
        (281,       'device_class',                     'power_factor'),                        -- The device class of the sensor.
        (282,       'device_class',                     'precipitation'),                       -- The device class of the sensor.
        (283,       'device_class',                     'precipitation_intensity'),             -- The device class of the sensor.
        (284,       'device_class',                     'pressure'),                            -- The device class of the sensor.
        (285,       'device_class',                     'reactive_power'),                      -- The device class of the sensor.
        (286,       'device_class',                     'signal_strength'),                     -- The device class of the sensor.
        (287,       'device_class',                     'sound_pressure'),                      -- The device class of the sensor.
        (288,       'device_class',                     'speed'),                               -- The device class of the sensor.
        (289,       'device_class',                     'sulphur_dioxide'),                     -- The device class of the sensor.
        (290,       'device_class',                     'temperature'),                         -- The device class of the sensor.
        (291,       'device_class',                     'volatile_organic_compounds'),          -- The device class of the sensor.
        (292,       'device_class',                     'volatile_organic_compounds_parts'),    -- The device class of the sensor.
        (293,       'device_class',                     'voltage'),                             -- The device class of the sensor.
        (294,       'device_class',                     'volume'),                              -- The device class of the sensor.
        (295,       'device_class',                     'volume_storage'),                      -- The device class of the sensor.
        (296,       'device_class',                     'volume_flow_rate'),                    -- The device class of the sensor.
        (297,       'device_class',                     'water'),                               -- The device class of the sensor.
        (298,       'device_class',                     'weight'),                              -- The device class of the sensor.
        (299,       'device_class',                     'wind_speed'),                          -- The device class of the sensor.
        (300,       'unit_of_measurement',              'string'),                              -- The unit of the sensor value.
        (301,       'battery_level',                    'int'),                                 -- The battery level of the sensor.
/* sensor_string
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/sensor
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/sensor
*/
        (302,       'device_class',                     'date'),                                -- The device class of the sensor.
        (303,       'device_class',                     'timestamp'),                           -- The device class of the sensor.
/* siren
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/siren
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/siren
*/
        (304,       'available_tones',                  'list[string]'),                        -- The list of possible sounds for the siren.
/* switch
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/switch
*/
        (305,       'device_class',                     'switch'),                              -- The device class of the switch.
        (306,       'device_class',                     'outlet'),                              -- The device class of the switch.
/* text
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/text
*/
        (307,       'mode',                             'text'),                                -- The text ui mode.
        (308,       'mode',                             'password'),                            --The text ui mode.
        (309,       'pattern',                          'string'),                              --A regex pattern that the text value must match to be valid.
/* todo
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/todo
*/
        (310,       'main',                             'int'),                                 -- A TodoListEntity state is the count of incomplete items in the To-do list.
/* update
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/update
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/update
*/
        (311,       'auto_update',                      'bool'),                                -- The device or service that the entity represents has auto update logic. When this is set to True you can not skip updates.
        (312,       'installed_version',                'string'),                              -- The currently installed and used version of the software.
        (313,       'in_progress',                      'int'),                                 -- Update installation progress. Can either return a boolean (1 if in progress, 0 if not) or an int to indicate the progress from 0 to 100%.
        (314,       'release_summary',                  'string'),                              -- Summary of the release notes or changelog.
        (315,       'release_url',                      'string'),                              -- URL to the full release notes of the latest version available.
        (316,       'current_version',                  'string'),                              -- The current version of the update.
        (317,       'skipped_version',                  'string'),                              -- The version that was skipped.
        (318,       'title',                            'string'),                              -- Title of the software.
        (319,       'latest_version',                   'string'),                              -- The latest version of the software available.
        (320,       'device_class',                     'firmware'),                            -- The device class of the update.
/* vacuum
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/vacuum
*/
        (321,       'main',                             'cleaning'),                            -- The vacuum is cleaning.
        (322,       'main',                             'returning'),                           -- The vacuum is returning to the dock.
        (323,       'battery_icon',                     'string'),                              -- The time the vacuum has been cleaning.
        (324,       'cleaned_area',                     'float'),                               -- The percentage of the area that has been cleaned.
        (325,       'fan_speed',                        'min'),                                 -- The speed of the vacuum fan.
        (326,       'fan_speed',                        'medium'),                              -- The speed of the vacuum fan.
        (327,       'fan_speed',                        'high'),                                -- The speed of the vacuum fan.
        (328,       'fan_speed',                        'max'),                                 -- The speed of the vacuum fan.
/* valve
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/valve
        https://www.home-assistant.io/integrations/valve/
*/
        (329,       'current_position',                 'int'),                                 -- The current position of the valve.
/* water_heater
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/water-heater
        https://github.com/home-assistant/core/blob/master/homeassistant/components/water_heater/__init__.py
*/
        (330,       'main',                             'eco'),                                 -- The water heater is in eco mode.
        (331,       'main',                             'electric'),                            -- The water heater is in electric mode.
        (332,       'main',                             'performance'),                         -- The water heater is in high performance mode.
        (333,       'main',                             'high_demand'),                         -- The water heater is in high performance mode.
        (334,       'main',                             'heat_pump'),                           -- The water heater is in heat pump mode.
        (335,       'main',                             'gas'),                                 -- The water heater is in gas mode.
        (336,       'operation_mode',                   'eco'),                                 -- The operation mode of the water heater.
        (337,       'operation_mode',                   'electric'),                            -- The operation mode of the water heater.
        (338,       'operation_mode',                   'performance'),                         -- The operation mode of the water heater.
        (339,       'operation_mode',                   'high_demand'),                         -- The operation mode of the water heater.
        (340,       'operation_mode',                   'heat_pump'),                           -- The operation mode of the water heater.
        (341,       'operation_mode',                   'gas'),                                 -- The operation mode of the water heater.
        (342,       'operation_mode',                   'off'),                                 -- The operation mode of the water heater.
        (343,       'away_mode',                        'on'),                                  -- The away mode of the water heater.
        (344,       'away_mode',                        'off'),                                 -- The away mode of the water heater.
/* weather
        states(main) / attributes extracted from:
        https://developers.home-assistant.io/docs/core/entity/weather
        https://github.com/home-assistant/core/blob/master/homeassistant/components/water_heater/__init__.py
*/
        (345,       'main',                             'clear-night'),                         -- The weather is clear at night.
        (346,       'main',                             'cloudy'),                              -- The weather is cloudy.
        (347,       'main',                             'exceptional'),                         -- The weather is exceptional.
        (348,       'main',                             'fog'),                                 -- The weather is foggy.
        (349,       'main',                             'hail'),                                -- The weather is hailing.
        (350,       'main',                             'lightning'),                           -- The weather is lightning.
        (351,       'main',                             'lightning-rainy'),                     -- The weather is lightning and rainy.
        (352,       'main',                             'partlycloudy'),                        -- The weather is partly cloudy.
        (353,       'main',                             'pouring'),                             -- The weather is pouring.
        (354,       'main',                             'rainy'),                               -- The weather is rainy.
        (355,       'main',                             'snowy'),                               -- The weather is snowy.
        (356,       'main',                             'snowy-rainy'),                         -- The weather is snowy and rainy.
        (357,       'main',                             'sunny'),                               -- The weather is sunny.
        (358,       'main',                             'windy'),                               -- The weather is windy.
        (359,       'main',                             'windy-variant'),                       -- The weather is windy and variant.
        (360,       'attribution',                      'string'),                              -- The attributor of the weather.
        (361,       'apparent_temperature',             'float'),                               -- The current apparent (feels-like) temperature in °C or °F.
        (362,       'pressure',                         'flaot'),                               -- The pressure of the weather.
        (363,       'pressure_unit',                    'string'),                              -- The pressure unit of the weather.
        (364,       'wind_speed',                       'float'),                               -- The wind bearing of the weather.
        (365,       'wind_speed_unit',                  'string'),                              -- The wind speed unit of the weather.
        (366,       'wind_bearing',                     'string'),                              -- The current wind bearing in azimuth angle (degrees) or 1-3 letter cardinal direction.
        (367,       'wind_gust_speed',                  'float'),                               -- The current wind gust speed.
        (368,       'visibility',                       'float'),                               -- The visibility of the weather.
        (369,       'visibility_unit',                  'string'),                              -- The visibility unit of the weather.
        (370,       'cloud_coverage',                   'int'),                                 -- The cloud coverage of the weather.
        (371,       'dew_point',                        'float'),                               -- The dew point temperature in °C or °F.
        (372,       'ozone',                            'float'),                               -- The current ozone level of the weather.
        (373,       'uv_index',                         'float'),                               -- The uv index of the weather.
        (374,       'precipitation_unit',               'string');                              -- The precipitation unit in mm or in.


-- CONNECTIONS
/* connect the integrations with the values */

INSERT INTO integration_values(i_id, pv_id)
VALUES
        --alarm_control_panel
        (1, 	 1), 	 	 -- Unknown state.
        (1, 	 2), 	 	 -- The alarm is disarmed (off).
        (1, 	 3), 	 	 -- The alarm is armed in home mode.
        (1, 	 4), 	 	 -- The alarm is armed in away mode.
        (1, 	 5), 	 	 -- The alarm is armed in night mode.
        (1, 	 6), 	 	 -- The alarm is armed in vacation mode.
        (1, 	 7), 	 	 -- The alarm is armed in bypass mode.
        (1, 	 8), 	 	 -- The alarm is pending (towards triggered).
        (1, 	 9), 	 	 -- The alarm is arming.
        (1, 	 10), 	 	 -- The alarm is disarming.
        (1, 	 11), 	 	 -- The alarm is triggered.
        (1, 	 12), 	 	 -- Unknown state.
        (1, 	 13), 	 	 -- The entity is not reachable.
        (1, 	 14), 	 	 -- The code format of the alarm control panel.
        (1, 	 15), 	 	 -- The code format of the alarm control panel.
        (1, 	 16), 	 	 -- The alarm control panel got changed by a user.
        (1, 	 17), 	 	 -- The code required to arm the alarm control panel.
        (1, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --binary_sensor 
        (2, 	 12), 	 	 -- Unknown state.
        (2, 	 13), 	 	 -- The entity is not reachable.
        (2, 	 20), 	 	 -- The sensor detects something.
        (2, 	 21), 	 	 -- The sensor detects nothing.
        (2, 	 22), 	 	 -- The device class of the binary sensor.
        (2, 	 23), 	 	 -- The device class of the binary sensor.
        (2, 	 24), 	 	 -- The device class of the binary sensor.
        (2, 	 25), 	 	 -- The device class of the binary sensor.
        (2, 	 26), 	 	 -- The device class of the binary sensor.
        (2, 	 27), 	 	 -- The device class of the binary sensor.
        (2, 	 28), 	 	 -- The device class of the binary sensor.
        (2, 	 29), 	 	 -- The device class of the binary sensor.
        (2, 	 30), 	 	 -- The device class of the binary sensor.
        (2, 	 31), 	 	 -- The device class of the binary sensor.
        (2, 	 32), 	 	 -- The device class of the binary sensor.
        (2, 	 33), 	 	 -- The device class of the binary sensor.
        (2, 	 34), 	 	 -- The device class of the binary sensor.
        (2, 	 35), 	 	 -- The device class of the binary sensor.
        (2, 	 36), 	 	 -- The device class of the binary sensor.
        (2, 	 37), 	 	 -- The device class of the binary sensor.
        (2, 	 38), 	 	 -- The device class of the binary sensor.
        (2, 	 39), 	 	 -- The device class of the binary sensor.
        (2, 	 40), 	 	 -- The device class of the binary sensor.
        (2, 	 41), 	 	 -- The device class of the binary sensor.
        (2, 	 42), 	 	 -- The device class of the binary sensor.
        (2, 	 43), 	 	 -- The device class of the binary sensor.
        (2, 	 44), 	 	 -- The device class of the binary sensor.
        (2, 	 45), 	 	 -- The device class of the binary sensor.
        (2, 	 46), 	 	 -- The device class of the binary sensor.
        (2, 	 47), 	 	 -- The device class of the binary sensor.
        (2, 	 48), 	 	 -- The device class of the binary sensor.
        (2, 	 49), 	 	 -- The device class of the binary sensor.
        --button 
        (3, 	 12), 	 	 -- Unknown state.
        (3, 	 13), 	 	 -- The entity is not reachable.
        --calendar 
        (4, 	 12), 	 	 -- Unknown state.
        (4, 	 13), 	 	 -- The entity is not reachable.
        (4, 	 20), 	 	 -- The sensor detects something.
        (4, 	 21), 	 	 -- The sensor detects nothing.
        (4, 	 50), 	 	 -- The calender description.
        (4, 	 51), 	 	 -- The calender message.
        (4, 	 52), 	 	 -- The calender event is all day
        (4, 	 53), 	 	 -- The calender event start time
        (4, 	 54), 	 	 -- The calender event end time.
        (4, 	 55), 	 	 -- The calender event location.
        (4,      56),            -- Triggered with this event
        (4,      57),            -- Offset of the trigger 
        --camera 
        (5, 	 12), 	 	 -- Unknown state.
        (5, 	 13), 	 	 -- The entity is not reachable.
        (5, 	 58), 	 	 -- The camera observes.
        (5, 	 59), 	 	 -- The camera records the recording.
        (5, 	 60), 	 	 -- The camera streams the recording.
        (5, 	 61), 	 	 -- The streaming format in the ui of the camera.
        (5, 	 62), 	 	 -- The streaming format in the ui of the camera.
        (5, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --climate 
        (6, 	 12), 	 	 -- Unknown state.
        (6, 	 13), 	 	 -- The entity is not reachable.
        (6, 	 21), 	 	 -- The sensor detects nothing.
        (6, 	 63), 	 	 -- The device is set to a schedule, learned behavior, AI.
        (6, 	 64), 	 	 -- The device is set to cool to a target temperature.
        (6, 	 65), 	 	 -- The device is set to heat to a target temperature.
        (6, 	 66), 	 	 -- The device is set to heat/cool to a target temperature range.
        (6, 	 67), 	 	 -- The device is set to dry/humidity mode.
        (6, 	 68), 	 	 -- The device only has the fan on. No heating or cooling taking place.
        (6, 	 69), 	 	 -- The current humidity.
        (6, 	 70), 	 	 -- The current temperature.
        (6, 	 71), 	 	 -- The maximum humidity.
        (6, 	 72), 	 	 -- The maximum temperature in temperature_unit.
        (6, 	 73), 	 	 -- The minimum humidity.
        (6, 	 74), 	 	 -- The minimum temperature in temperature_unit.
        (6, 	 75), 	 	 -- The precision of the temperature in the system. Defaults to tenths for TEMP_CELSIUS, whole number otherwise.
        (6, 	 76), 	 	 -- The target humidity the device is trying to reach.
        (6, 	 77), 	 	 -- The temperature currently set to be reached.
        (6, 	 78), 	 	 -- The upper bound target temperature.
        (6, 	 79), 	 	 -- The lower bound target temperature
        (6, 	 80), 	 	 -- The supported step size a target temperature can be increased or decreased
        (6, 	 81), 	 	 -- The unit of temperature measurement for the system (TEMP_CELSIUS or TEMP_FAHRENHEIT).
        (6, 	 82), 	 	 -- Device is preheating.
        (6, 	 83), 	 	 -- Device is heating.
        (6, 	 84), 	 	 -- Device is cooling.
        (6, 	 85), 	 	 -- Device is drying.
        (6, 	 86), 	 	 -- Device has fan on.
        (6, 	 87), 	 	 -- Device is defrosting.
        (6, 	 88), 	 	 -- Device is off.
        (6, 	 89), 	 	 -- Device is doing nothing.
        (6, 	 90), 	 	 -- The fan on.
        (6, 	 91), 	 	 -- The fan off.
        (6, 	 92), 	 	 -- The fan turns on automatically high.
        (6, 	 93), 	 	 -- The fan turns on automatically low.
        (6, 	 94), 	 	 -- The fan speed is low.
        (6, 	 95), 	 	 -- The fan speed is medium.
        (6, 	 96), 	 	 -- The fan speed is high.
        (6, 	 97), 	 	 -- The fan stayes in the middle.
        (6, 	 98), 	 	 -- The fan focuses in on direction.
        (6, 	 99), 	 	 -- The fan diffuse in all possible directions.
        (6, 	 100), 	 	 -- The fan don't swing.
        (6, 	 101), 	 	 -- The fan swings automatically.
        (6, 	 102), 	 	 -- The fan swings with speed 1.
        (6, 	 103), 	 	 -- The fan swings with speed 2.
        (6, 	 104), 	 	 -- The fan swings with speed 3.
        (6, 	 105), 	 	 -- The fan swings vertically.
        (6, 	 106), 	 	 -- The fan swings horizontally.
        (6, 	 107), 	 	 -- The fan swings in both directions.
        (6, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --conversation 
        (7, 	 12), 	 	 -- Unknown state.
        (7, 	 13), 	 	 -- The entity is not reachable.
        (7, 	 108), 	 	 -- Date of the last call in the converstation.
        (7,      109),           -- The command to trigger the event
        --cover 
        (8, 	 12), 	 	 -- Unknown state.
        (8, 	 13), 	 	 -- The entity is not reachable.
        (8, 	 110), 	 	 -- The cover has reach the closed position.
        (8, 	 111), 	 	 -- The cover is in the process of closing to reach a set position.
        (8, 	 112), 	 	 -- The cover has reached the open position.
        (8, 	 113), 	 	 -- The cover is in the process of opening to reach a set position.
        (8, 	 114), 	 	 -- The device class of the binary sensor.
        (8, 	 115), 	 	 -- The device class of the binary sensor.
        (8, 	 116), 	 	 -- The device class of the binary sensor.
        (8, 	 117), 	 	 -- The device class of the binary sensor.
        (8, 	 118), 	 	 -- The device class of the binary sensor.
        (8, 	 119), 	 	 -- The device class of the binary sensor.
        (8, 	 120), 	 	 -- The device class of the binary sensor.
        (8, 	 121), 	 	 -- The device class of the binary sensor.
        (8, 	 27), 	 	 -- The device class of the binary sensor.
        (8, 	 49), 	 	 -- The device class of the binary sensor.
        (8, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --date 
        (9, 	 12), 	 	 -- Unknown state.
        (9, 	 13), 	 	 -- The entity is not reachable.
        (9, 	 108), 	 	 -- Date as string.
        --datetime 
        (10, 	 12), 	 	 -- Unknown state.
        (10, 	 13), 	 	 -- The entity is not reachable.
        (10, 	 108), 	 	 -- Datetime as string.
        --device_tracker 
        (11, 	 12), 	 	 -- Unknown state.
        (11, 	 13), 	 	 -- The entity is not reachable.
        (11, 	 122), 	 	 -- The device is home.
        (11, 	 123), 	 	 -- The cover is not home.
        (11, 	 124), 	 	 -- The source of the device connection.
        (11, 	 125), 	 	 -- The source of the device connection.
        (11, 	 126), 	 	 -- The source of the device connection.
        (11, 	 127), 	 	 -- The source of the device connection.
        (11, 	 128), 	 	 -- The source of the device connection.
        (11, 	 129), 	 	 -- The source of the device connection.
        (11, 	 130), 	 	 -- The source of the device connection.
        (11, 	 131), 	 	 -- The source of the device connection.
        --event 
        (12, 	 12), 	 	 -- Unknown state.
        (12, 	 13), 	 	 -- The entity is not reachable.
        (12, 	 108), 	 	 -- Datetime of the last call.
        (12, 	 132), 	 	 -- The event of a button press.
        (12, 	 133), 	 	 -- The event of a service called.
        (12, 	 134), 	 	 -- The event of component loaded.
        (12, 	 135), 	 	 -- The event of update the core config.
        (12, 	 136), 	 	 -- The event of data entry flow progresses.
        (12, 	 137), 	 	 -- The event of home assistant starting.
        (12, 	 138), 	 	 -- The event ofhome assistant started.
        (12, 	 139), 	 	 -- The event home assistant stopped.
        (12, 	 140), 	 	 -- The event home assistant makes it final write befor shutting down.
        (12, 	 141), 	 	 -- The event of making a logbook entry.
        (12, 	 142), 	 	 -- The event of register a new service.
        (12, 	 143), 	 	 -- The event of removing a service.
        (12, 	 144), 	 	 -- The event of state change of an entity.
        (12, 	 145), 	 	 -- The event of the theme change in the ui.
        (12, 	 146), 	 	 -- The event for a new user.
        (12, 	 147), 	 	 -- The event to remove a user.
        (12, 	 148), 	 	 -- The event of reloading the automation.yaml files.
        (12, 	 149), 	 	 -- The event of triggering an automation.
        (12, 	 150), 	 	 -- The event of reload a scene. 
        (12, 	 151), 	 	 -- The event of the start of a script.
        (12, 	 152), 	 	 -- The event of an area update.
        (12, 	 153), 	 	 -- The event of a category registry update.
        (12, 	 154), 	 	 -- The event of a device registry update.
        (12, 	 155), 	 	 -- The event of a entity registry update.
        (12, 	 156), 	 	 -- A custom event.
        (12,     157),           -- Dict of additional event data
        (12,     158),           -- Dict of additional event context
        --fan 
        (13, 	 12), 	 	 -- Unknown state.
        (13, 	 13), 	 	 -- The entity is not reachable.
        (13, 	 20), 	 	 -- The sensor detects something.
        (13, 	 21), 	 	 -- The sensor detects nothing.
        (13, 	 159), 	 	 -- The current speed percentage. Must be a value between 0 (off and 100).
        (13, 	 160), 	 	 -- The steps for the speed percentage. Must be a value between 1 and 100.
        (13, 	 161), 	 	 -- The if the fan is oscillating.
        (13, 	 162), 	 	 -- The fan spinns forward.
        (13, 	 163), 	 	 -- The fan spinns reverse.
        (13, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --humidifier 
        (14, 	 12), 	 	 -- Unknown state.
        (14, 	 13), 	 	 -- The entity is not reachable.
        (14, 	 20), 	 	 -- The sensor detects something.
        (14, 	 21), 	 	 -- The sensor detects nothing.
        (14, 	 73), 	 	 -- The minimum humidity.
        (14, 	 71), 	 	 -- The maximum humidity.
        (14, 	 69), 	 	 -- The current humidity.
        (14, 	 76), 	 	 -- The target humidity the device is trying to reach.
        (14, 	 164), 	 	 -- The humidifier is off.
        (14, 	 165), 	 	 -- The humidifier does nothing.
        (14, 	 166), 	 	 -- The humidifier humidifying the air.
        (14, 	 167), 	 	 -- The humidifier drying the air.
        (14, 	 168), 	 	 -- The humidifier is a humidifier.
        (14, 	 169), 	 	 -- The humidifier is a dehumidifier.
        (14, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --image 
        (15, 	 12), 	 	 -- Unknown state.
        (15, 	 13), 	 	 -- The entity is not reachable.
        (15, 	 108), 	 	 -- URL as string.
        --lawn_mower
        (16, 	 12), 	 	 -- Unknown state.
        (16, 	 13), 	 	 -- The entity is not reachable.
        (16, 	 170), 	 	 -- The lawn mower is currently mowing.
        (16, 	 171), 	 	 -- The lawn mower is done mowing and is currently docked.
        (16, 	 172), 	 	 -- The lawn mower was active and is now paused.
        (16, 	 173), 	 	 -- The lawn mower encountered an error while active and needs assistance.
        --light
        (17, 	 12), 	 	 -- Unknown state.
        (17, 	 13), 	 	 -- The entity is not reachable.
        (17, 	 20), 	 	 -- The sensor detects something.
        (17, 	 21), 	 	 -- The sensor detects nothing.
        (17, 	 174), 	 	 -- The light makes a rainbow effect.
        (17, 	 175), 	 	 -- The light makes no effect.
        (17, 	 176), 	 	 -- The minimal color value.
        (17, 	 177), 	 	 -- The maximal color value.
        (17, 	 178), 	 	 -- The ui color setting.
        (17, 	 179), 	 	 -- The ui color setting.
        (17, 	 180), 	 	 -- The brightness of the light.
        (17, 	 181), 	 	 -- The color of the light as kelvin number.
        (17, 	 182), 	 	 -- The color of the light in hs-format.
        (17, 	 183), 	 	 -- The color of the light in rgb-format.
        (17, 	 184), 	 	 -- The color of the light in xy-format.
        (17, 	 185), 	 	 -- The color of the light in rgbw-format.
        (17, 	 186), 	 	 -- The color of the light in rgbww-format.
        (17, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --lock
        (18, 	 12), 	 	 -- Unknown state.
        (18, 	 13), 	 	 -- The entity is not reachable.
        (18, 	 112), 	 	 -- The cover has reached the open position.
        (18, 	 113), 	 	 -- The cover is in the process of opening to reach a set position.
        (18, 	 187), 	 	 -- The lock is unabled to toggle.
        (18, 	 188), 	 	 -- The lock is locked.
        (18, 	 189), 	 	 -- The lock is looking.
        (18, 	 190), 	 	 -- The lock is unlocked.
        (18, 	 191), 	 	 -- The lock is unlooking.
        (18, 	 14), 	 	 -- The code format of the alarm control panel.
        (18, 	 15), 	 	 -- The code format of the alarm control panel.
        (18, 	 16), 	 	 -- The alarm control panel got changed by a user.
        (18, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --media_player
        (19, 	 12), 	 	 -- Unknown state.
        (19, 	 13), 	 	 -- The entity is not reachable.
        (19, 	 20), 	 	 -- The sensor detects something.
        (19, 	 21), 	 	 -- The sensor detects nothing.
        (19, 	 58), 	 	 -- The camera observes.
        (19, 	 172), 	 	 -- The lawn mower was active and is now paused.
        (19, 	 192), 	 	 -- The media player playimg something.
        (19, 	 193), 	 	 -- The media player is in standby mode.
        (19, 	 194), 	 	 -- The media player buffering something.
        (19, 	 195), 	 	 -- The volume level of the media player in the range (0..1).
        (19, 	 196), 	 	 -- Its true if volume is currently muted.
        (19, 	 197), 	 	 -- The volume step to use for the volume_up and volume_down services.
        (19, 	 198), 	 	 -- The content ID of current playing media.
        (19, 	 199), 	 	 -- The content type of current playing media.
        (19, 	 200), 	 	 -- The content type of current playing media.
        (19, 	 201), 	 	 -- The content type of current playing media.
        (19, 	 202), 	 	 -- The content type of current playing media.
        (19, 	 203), 	 	 -- The content type of current playing media.
        (19, 	 204), 	 	 -- The content type of current playing media.
        (19, 	 205), 	 	 -- The content type of current playing media.
        (19, 	 206), 	 	 -- The content type of current playing media.
        (19, 	 207), 	 	 -- The content type of current playing media.
        (19, 	 208), 	 	 -- The content type of current playing media.
        (19, 	 209), 	 	 -- The content type of current playing media.
        (19, 	 210), 	 	 -- The content type of current playing media.
        (19, 	 211), 	 	 -- The content type of current playing media.
        (19, 	 212), 	 	 -- The content type of current playing media.
        (19, 	 213), 	 	 -- The content type of current playing media.
        (19, 	 214), 	 	 -- The content type of current playing media.
        (19, 	 215), 	 	 -- The content type of current playing media.
        (19, 	 216), 	 	 -- The content type of current playing media.
        (19, 	 217), 	 	 -- The content type of current playing media.
        (19, 	 218), 	 	 -- The content type of current playing media.
        (19, 	 219), 	 	 -- The name of the current running app.
        (19, 	 220), 	 	 -- A dynamic list of player entities which are currently grouped together for synchronous playback.
        (19, 	 221), 	 	 -- The album artist of current playing media, music track only.
        (19, 	 222), 	 	 -- The album name of current playing media, music track only.
        (19, 	 223), 	 	 -- The artist of current playing media, music track only.
        (19, 	 224), 	 	 -- The channel currently playing.
        (19, 	 225), 	 	 -- The duration of current playing media in seconds.
        (19, 	 226), 	 	 -- The episode of current playing media, TV show only.
        (19, 	 227), 	 	 -- The duration of current playing media in seconds.
        (19, 	 228), 	 	 -- The episode of current playing media, TV show only
        (19, 	 229), 	 	 -- The duration of current playing media in seconds.
        (19, 	 230), 	 	 -- The episode of current playing media, TV show only
        (19, 	 231), 	 	 -- The duration of current playing media in seconds.
        (19, 	 232), 	 	 -- The track number of current playing media, music track only.
        (19, 	 233), 	 	 -- The current repeat mode.
        (19, 	 234), 	 	 -- The current repeat mode.
        (19, 	 235), 	 	 -- The current repeat mode.
        (19, 	 236), 	 	 -- True if shuffle is enabled.
        (19, 	 237), 	 	 -- The currently selected input source for the media player.
        (19, 	 238), 	 	 -- The currently selected input source for the media player.
        (19, 	 239), 	 	 -- The current sound mode of the media player.
        (19, 	 240), 	 	 -- The current sound mode of the media player.
        (19, 	 241), 	 	 -- The media player is a tv.
        (19, 	 242), 	 	 -- The media player is a speaker.
        (19, 	 243), 	 	 -- The media player is a receiver.
        (19, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --notify
        (20, 	 12), 	 	 -- Unknown state.
        (20, 	 13), 	 	 -- The entity is not reachable.
        (20, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --number
        (21, 	 12), 	 	 -- Unknown state.
        (21, 	 13), 	 	 -- The entity is not reachable.
        (21, 	 244), 	 	 -- The number of the entity.
        (21, 	 245), 	 	 -- The minimum accepted value in the number's (inclusive).
        (21, 	 246), 	 	 -- The maximum accepted value in the number's (inclusive).
        (21, 	 247), 	 	 -- Defines the resolution of the values, i.e. the smallest increment or decrement in the number's.
        (21, 	 248), 	 	 -- Defines how the number should be displayed in the UI. Can be box, slider or auto.
        --remote
        (22, 	 12), 	 	 -- Unknown state.
        (22, 	 13), 	 	 -- The entity is not reachable.
        (22, 	 108), 	 	 -- Datetime of the last call.
        (22, 	 249), 	 	 -- The minimum accepted value in the number's (inclusive).
        (22, 	 250), 	 	 -- The maximum accepted value in the number's (inclusive).
        --scene
        (23, 	 12), 	 	 -- Unknown state.
        (23, 	 13), 	 	 -- The entity is not reachable.
        (23, 	 108), 	 	 -- Datetime of the last call.
        (23, 	 251), 	 	 -- The id of the scene.
        (23, 	 252), 	 	 -- The id of the entity in the scene.
        --select
        (24, 	 12), 	 	 -- Unknown state.
        (24, 	 13), 	 	 -- The entity is not reachable.
        (24, 	 253), 	 	 -- The one of the options of the select.
        (24, 	 254), 	 	 -- All options of the select.
        --sensor_float
        (25, 	 12), 	 	 -- Unknown state.
        (25, 	 13), 	 	 -- The entity is not reachable.
        (25, 	 244), 	 	 -- The number of the entity.
        (25, 	 255), 	 	 -- The device class of the sensor.
        (25, 	 256), 	 	 -- The device class of the sensor.
        (25, 	 257), 	 	 -- The device class of the sensor.
        (25, 	 258), 	 	 -- The device class of the sensor.
        (25, 	 259), 	 	 -- The device class of the sensor.
        (25, 	 260), 	 	 -- The device class of the sensor.
        (25, 	 261), 	 	 -- The device class of the sensor.
        (25, 	 262), 	 	 -- The device class of the sensor.
        (25, 	 263), 	 	 -- The device class of the sensor.
        (25, 	 264), 	 	 -- The device class of the sensor.
        (25, 	 265), 	 	 -- The device class of the sensor.
        (25, 	 266), 	 	 -- The device class of the sensor.
        (25, 	 267), 	 	 -- The device class of the sensor.
        (25, 	 268), 	 	 -- The device class of the sensor.
        (25, 	 269), 	 	 -- The device class of the sensor.
        (25, 	 270), 	 	 -- The device class of the sensor.
        (25, 	 271), 	 	 -- The device class of the sensor.
        (25, 	 272), 	 	 -- The device class of the sensor.
        (25, 	 273), 	 	 -- The device class of the sensor.
        (25, 	 274), 	 	 -- The device class of the sensor.
        (25, 	 275), 	 	 -- The device class of the sensor.
        (25, 	 276), 	 	 -- The device class of the sensor.
        (25, 	 277), 	 	 -- The device class of the sensor.
        (25, 	 278), 	 	 -- The device class of the sensor.
        (25, 	 279), 	 	 -- The device class of the sensor.
        (25, 	 280), 	 	 -- The device class of the sensor.
        (25, 	 281), 	 	 -- The device class of the sensor.
        (25, 	 282), 	 	 -- The device class of the sensor.
        (25, 	 283), 	 	 -- The device class of the sensor.
        (25, 	 284), 	 	 -- The device class of the sensor.
        (25, 	 285), 	 	 -- The device class of the sensor.
        (25, 	 286), 	 	 -- The device class of the sensor.
        (25, 	 287), 	 	 -- The device class of the sensor.
        (25, 	 288), 	 	 -- The device class of the sensor.
        (25, 	 289), 	 	 -- The device class of the sensor.
        (25, 	 290), 	 	 -- The device class of the sensor.
        (25, 	 291), 	 	 -- The device class of the sensor.
        (25, 	 292), 	 	 -- The device class of the sensor.
        (25, 	 293), 	 	 -- The device class of the sensor.
        (25, 	 294), 	 	 -- The device class of the sensor.
        (25, 	 295), 	 	 -- The device class of the sensor.
        (25, 	 296), 	 	 -- The device class of the sensor.
        (25, 	 297), 	 	 -- The device class of the sensor.
        (25, 	 298), 	 	 -- The device class of the sensor.
        (25, 	 299), 	 	 -- The device class of the sensor.
        (25, 	 300), 	 	 -- The unit of the sensor value.
        (25, 	 301), 	 	 -- The battery level of the sensor.
        (25, 	 22), 	 	 -- The device class of the binary sensor.
        (25, 	 29), 	 	 -- The device class of the binary sensor.
        (25, 	 33), 	 	 -- The device class of the binary sensor.
        (25, 	 39), 	 	 -- The device class of the binary sensor.
        --sensor_string
        (26, 	 12), 	 	 -- Unknown state.
        (26, 	 13), 	 	 -- The entity is not reachable.
        (26, 	 108), 	 	 -- State as string.
        (26, 	 302), 	 	 -- The device class of the sensor.
        (26, 	 303), 	 	 -- The device class of the sensor.
        --sensor_enum
        (27, 	 12), 	 	 -- Unknown state.
        (27, 	 13), 	 	 -- The entity is not reachable.
        (27, 	 253), 	 	 -- The one of the options of the select.
        --siren
        (28, 	 12), 	 	 -- Unknown state.
        (28, 	 13), 	 	 -- The entity is not reachable.
        (28, 	 20), 	 	 -- The sensor detects something.
        (28, 	 21), 	 	 -- The sensor detects nothing.
        (28, 	 304), 	 	 -- The list of possible sounds for the siren.
        (28, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --stt
        (29, 	 12), 	 	 -- Unknown state.
        (29, 	 13), 	 	 -- The entity is not reachable.
        --switch
        (30, 	 12), 	 	 -- Unknown state.
        (30, 	 13), 	 	 -- The entity is not reachable.
        (30, 	 20), 	 	 -- The sensor detects something.
        (30, 	 21), 	 	 -- The sensor detects nothing.
        (30, 	 305), 	 	 -- The device class of the switch.
        (30, 	 306), 	 	 -- The device class of the switch.
        --text
        (31, 	 12), 	 	 -- Unknown state.
        (31, 	 13), 	 	 -- The entity is not reachable.
        (31, 	 108), 	 	 -- State as string.
        (31, 	 307), 	 	 -- The text ui mode.
        (31, 	 308), 	 	 -- The text ui mode.
        (31, 	 309), 	 	 -- A regex pattern that the text value must match to be valid.
        (31, 	 245), 	 	 -- The minimum accepted value in the number's (inclusive).
        (31, 	 246), 	 	 -- The maximum accepted value in the number's (inclusive).
        --time
        (32, 	 12), 	 	 -- Unknown state.
        (32, 	 13), 	 	 -- The entity is not reachable.
        (32,     19),            -- Time AT which it triggers an event
        (32, 	 108), 	 	 -- Time as string.
        --todo
        (33, 	 12), 	 	 -- Unknown state.
        (33, 	 13), 	 	 -- The entity is not reachable.
        (33, 	 310), 	 	 -- A TodoListEntity state is the count of incomplete items in the To-do list.
        (33, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --tts
        (34, 	 12), 	 	 -- Unknown state.
        (34, 	 13), 	 	 -- The entity is not reachable.
        --update
        (35, 	 12), 	 	 -- Unknown state.
        (35, 	 13), 	 	 -- The entity is not reachable.
        (35, 	 20), 	 	 -- The sensor detects something.
        (35, 	 21), 	 	 -- The sensor detects nothing.
        (35, 	 311), 	 	 -- The device or service that the entity represents has auto update logic. When this is set to True you can not skip updates.
        (35, 	 312), 	 	 -- The currently installed and used version of the software.
        (35, 	 313), 	 	 -- Update installation progress. Can either return a boolean (1 if in progress, 0 if not or an int to indicate the progress from 0 to 100%).
        (35, 	 314), 	 	 -- Summary of the release notes or changelog.
        (35, 	 315), 	 	 -- URL to the full release notes of the latest version available.
        (35, 	 316), 	 	 -- The current version of the update.
        (35, 	 317), 	 	 -- The version that was skipped.
        (35, 	 318), 	 	 -- Title of the software.
        (35, 	 319), 	 	 -- The latest version of the software available.
        (35, 	 320), 	 	 -- The device class of the update.
        (35, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --vacuum
        (36, 	 12), 	 	 -- Unknown state.
        (36, 	 13), 	 	 -- The entity is not reachable.
        (36, 	 58), 	 	 -- The camera observes.
        (36, 	 171), 	 	 -- The lawn mower is done mowing and is currently docked.
        (36, 	 172), 	 	 -- The lawn mower was active and is now paused.
        (36, 	 173), 	 	 -- The lawn mower encountered an error while active and needs assistance.
        (36, 	 321), 	 	 -- The vacuum is cleaning.
        (36, 	 322), 	 	 -- The vacuum is returning to the dock.
        (36, 	 301), 	 	 -- The battery level of the sensor.
        (36, 	 323), 	 	 -- The time the vacuum has been cleaning.
        (36, 	 324), 	 	 -- The percentage of the area that has been cleaned.
        (36, 	 325), 	 	 -- The speed of the vacuum fan.
        (36, 	 326), 	 	 -- The speed of the vacuum fan.
        (36, 	 327), 	 	 -- The speed of the vacuum fan.
        (36, 	 328), 	 	 -- The speed of the vacuum fan.
        (36, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --valv e
        (37, 	 12), 	 	 -- Unknown state.
        (37, 	 13), 	 	 -- The entity is not reachable.
        (37, 	 110), 	 	 -- The cover has reach the closed position.
        (37, 	 111), 	 	 -- The cover is in the process of closing to reach a set position.
        (37, 	 112), 	 	 -- The cover has reached the open position.
        (37, 	 113), 	 	 -- The cover is in the process of opening to reach a set position.
        (37, 	 29), 	 	 -- The device class of the binary sensor.
        (37, 	 297), 	 	 -- The device class of the sensor.
        (37, 	 329), 	 	 -- The current position of the valve.
        --wake_word
        (38, 	 12), 	 	 -- Unknown state.
        (38, 	 13), 	 	 -- The entity is not reachable.
        (38, 	 108), 	 	 -- Datetime of the last call.
        --water_heater
        (39, 	 12), 	 	 -- Unknown state.
        (39, 	 13), 	 	 -- The entity is not reachable.
        (39, 	 21), 	 	 -- The sensor detects nothing.
        (39, 	 65), 	 	 -- The device is set to heat to a target temperature.
        (39, 	 330), 	 	 -- The water heater is in eco mode.
        (39, 	 331), 	 	 -- The water heater is in electric mode.
        (39, 	 332), 	 	 -- The water heater is in high performance mode.
        (39, 	 333), 	 	 -- The water heater is in high performance mode.
        (39, 	 334), 	 	 -- The water heater is in heat pump mode.
        (39, 	 335), 	 	 -- The water heater is in gas mode.
        (39, 	 74), 	 	 -- The minimum temperature in temperature_unit.
        (39, 	 72), 	 	 -- The maximum temperature in temperature_unit.
        (39, 	 70), 	 	 -- The current temperature.
        (39, 	 77), 	 	 -- The temperature currently set to be reached.
        (39, 	 78), 	 	 -- The upper bound target temperature.
        (39, 	 79), 	 	 -- The lower bound target temperature
        (39, 	 336), 	 	 -- The operation mode of the water heater.
        (39, 	 337), 	 	 -- The operation mode of the water heater.
        (39, 	 338), 	 	 -- The operation mode of the water heater.
        (39, 	 339), 	 	 -- The operation mode of the water heater.
        (39, 	 340), 	 	 -- The operation mode of the water heater.
        (39, 	 341), 	 	 -- The operation mode of the water heater.
        (39, 	 342), 	 	 -- The operation mode of the water heater.
        (39, 	 343), 	 	 -- The away mode of the water heater.
        (39, 	 344), 	 	 -- The away mode of the water heater.
        (39, 	 18), 	 	 -- The count of supported features of the alarm control panel.
        --weatherhomeassistant
        (40, 	 12), 	 	 -- Unknown state.
        (40, 	 13), 	 	 -- The entity is not reachable.
        (40, 	 21), 	 	 -- The sensor detects nothing.
        (40, 	 65), 	 	 -- The device is set to heat to a target temperature.
        (40, 	 345), 	 	 -- The weather is clear at night.
        (40, 	 346), 	 	 -- The weather is cloudy.
        (40, 	 347), 	 	 -- The weather is exceptional.
        (40, 	 348), 	 	 -- The weather is foggy.
        (40, 	 349), 	 	 -- The weather is hailing.
        (40, 	 350), 	 	 -- The weather is lightning.
        (40, 	 351), 	 	 -- The weather is lightning and rainy.
        (40, 	 352), 	 	 -- The weather is partly cloudy.
        (40, 	 353), 	 	 -- The weather is pouring.
        (40, 	 354), 	 	 -- The weather is rainy.
        (40, 	 355), 	 	 -- The weather is snowy.
        (40, 	 356), 	 	 -- The weather is snowy and rainy.
        (40, 	 357), 	 	 -- The weather is sunny.
        (40, 	 358), 	 	 -- The weather is windy.
        (40, 	 359), 	 	 -- The weather is windy and variant.
        (40, 	 76), 	 	 -- The target humidity the device is trying to reach.
        (40, 	 77), 	 	 -- The temperature currently set to be reached.
        (40, 	 81), 	 	 -- The unit of temperature measurement for the system (TEMP_CELSIUS or TEMP_FAHRENHEIT).
        (40, 	 360), 	 	 -- The attributor of the weather.
        (40, 	 361), 	 	 -- The current apparent (feels-like temperature in °C or °F).
        (40, 	 362), 	 	 -- The pressure of the weather.
        (40, 	 363), 	 	 -- The pressure unit of the weather.
        (40, 	 364), 	 	 -- The wind bearing of the weather.
        (40, 	 365), 	 	 -- The wind speed unit of the weather.
        (40, 	 366), 	 	 -- The current wind bearing in azimuth angle (degrees or 1-3 letter cardinal direction).
        (40, 	 367), 	 	 -- he current wind gust speed.
        (40, 	 368), 	 	 -- The visibility of the weather.
        (40, 	 369), 	 	 -- The visibility unit of the weather.
        (40, 	 370), 	 	 -- The cloud coverage of the weather.
        (40, 	 371), 	 	 -- The dew point temperature in °C or °F.
        (40, 	 372), 	 	 -- The current ozone level of the weather.
        (40, 	 373), 	 	 -- The uv index of the weather.
        (40, 	 374), 	 	 -- The precipitation unit in mm or in.
        (40, 	 18); 	 	 -- The count of supported features of the alarm control panel.


/* trigger integrations */
/* import the integrations for triggers */

INSERT INTO integration(i_id, i_name)
VALUES  (41,    'homeassistant'),
        (42,    'mqtt'),
        (43,    'sun'),
        (44,    'tag'),
        (45,    'time_pattern'),
        (46,    'persistent_notification'),
        (47,    'webhook'),
        (48,    'zone'),
        (49,    'device');

-- POSSIBLE VALUES --
/* import the values from trigger integrations */

INSERT INTO possible_values(pv_id, property, p_value)
VALUES
/* homeassistant
        attributes extracted from trigger: automation_dissection.py
*/
        (375,       'event',                            'start'),                               -- Home assistant is starting
        (376,       'event',                            'shutdown'),                            -- Home assistant is shutting down
/* mqtt 
        attributes extracted from: automation_dissection.py
*/
        (377,       'payload',                          'string'),                              -- The payload of the message
        (378,       'qos',                              '0'),                                   -- The quality of service of the message
        (379,       'qos',                              '1'),                                   -- The quality of service of the message
        (380,       'qos',                              '2'),                                   -- The quality of service of the message
/* sun
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/sun/
*/ 
        (381,       'main',                             'above_horizon'),                       -- The sun is above the horizon.
        (382,       'main',                             'below_horizon'),                       -- The sun is below the horizon.
        (383,       'azimuth',                          'float'),                               -- The azimuth of the sun.
        (384,       'elevation',                        'float'),                               -- The elevation of the sun.
        (385,       'next_dawn',                        'string'),                              -- The next dawn time.
        (386,       'next_dusk',                        'string'),                              -- The next dusk time.
        (387,       'next_midnight',                    'string'),                              -- The next midnight time.
        (388,       'next_noon',                        'string'),                              -- The next noon time.
        (389,       'next_rising',                      'string'),                              -- The next rising time.
        (390,       'next_setting',                     'string'),                              -- The next setting time.
        (391,       'rising',                           'bool'),                                -- The sun is rising.
        (392,       'event',                            'sunrise'),                             -- The event trigger for sunrises
        (393,       'event',                            'sunset'),                              -- The event trigger for sunsets
/* tag  
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/tag/
*/
        (394,       'device_id',                        'string'),                              -- The id of the device that scanned the tag.
        (395,       'tag_id',                           'string'),                              -- The id of the tag.

/* persistent_notification
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/persistent_notification/
*/
        (396,       'update_type',                      'added'),                               -- The message of the notification.
        (397,       'update_type',                      'updated'),                             -- The message of the notification.
        (398,       'update_type',                      'removed'),                             -- The message of the notification.
        (399,       'update_type',                      'current'),                             -- The message of the notification.
        (400,       'notification_id',                  'string'),                              -- The id of the notification.
/* webhook
        states(main) / attributes extracted from:
        https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger
*/
        (401,       'allowed_method',                   'POST'),                                -- The allowed method for the web.
        (402,       'allowed_method',                   'PUT'),                                 -- The allowed method for the web.
        (403,       'allowed_method',                   'HEAD'),                                -- The allowed method for the web.
        (404,       'allowed_method',                   'GET'),                                 -- The allowed method for the web.
        (405,       'local_only',                       'bool'),                                -- The webhook is local only.
/* zone
        states(main) / attributes extracted from:
        https://www.home-assistant.io/integrations/zone/
*/
        (406,       'radius',                           'int'),                                 -- The radius of the zone.
        (407,       'passive',                          'bool'),                                -- The zone is passive.
        (408,       'persons',                          'list[string]'),                        -- The persons in the zone.
/* device_automation
        states(main) / attributes extracted from:
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/device_automation
*/                                
        (409,       'domain',                           'string'),                              -- enitity domain.
        (410,       'type',                             'turned_on'),                           -- type of trigger.
        (411,       'type',                             'turned_off'),                          -- type of trigger .
        (412,       'type',                             'is_on'),                               -- type of condition.
        (413,       'type',                             'is_off'),                              -- type of condition.
        (414,       'type',                             'turn_on'),                             -- type of action.
        (415,       'type',                             'turn_off'),                            -- type of action.
        (416,       'type',                             'toggle');                              -- type of action.

INSERT INTO integration_values(i_id, pv_id)
VALUES  
        -- homeassistant
        (41,     375),      --  Home assistant is starting
        (41,     376),      --  Home assistant is shutting down
        -- mqtt
        (42,     377),      --  The payload of the message
        (42,     378),      --  The quality of service of the message
        (42,     379),      --  The quality of service of the message
        (42,     380),      --  The quality of service of the message
        -- sun
        (43,     381),      --  The sun is above the horizon.
        (43,     382),      --  The sun is below the horizon.
        (43,     383),      --  The azimuth of the sun.    
        (43,     384),      --  The elevation of the sun.
        (43,     385),      --  The next dawn time.
        (43,     386),      --  The next dusk time. 
        (43,     387),      --  The next midnight time.
        (43,     388),      --  The next noon time.
        (43,     389),      --  The next rising time. 
        (43,     390),      --  The next setting time.
        (43,     391),      --  The sun is rising.
        (43,     392),      --  The event trigger for sunrises 
        (43,     393),      --  The event trigger for sunsets
        -- tag
        (44,     12),       --  unknown
        (44,     13),       --  unavailable
        (44,     108),      --  Date of the last use as string
        (44,     394),      --  The id of the device that last scanned the tag.
        (44,     395),      --  The id of the tag.
        -- time_pattern
        (45,     20),       -- The pattern is active.
        (45,     21),       -- The pattern is inactive.
        -- persistent_notification
        (46,     396),      -- The message of the notification.
        (46,     397),      -- The message of the notification.
        (46,     398),      -- The message of the notification.
        (46,     399),      -- The message of the notification.
        (46,     318),      -- The title of the notification.
        (46,     51),       -- The message of the notification.
        (46,     400),      -- The id of the notification.
        -- webhook
        (47,     401),      -- The allowed method for the webhook.
        (47,     402),      -- The allowed method for the webhook.
        (47,     403),      -- The allowed method for the webhook.
        (47,     404),      -- The allowed method for the webhook.
        (47,     405),      -- The webhook is local only.
        -- zone
        (48,     310),      -- The number of registered people in the zone
        (48,     128),      -- The coordinates of the zone.
        (48,     129),      -- The coordinates of the zone.
        (48,     406),      -- The radius of the zone.
        (48,     407),      -- The zone is passive.
        (48,     408),      -- The persons in the zone.   
        -- device_automation
        (49,    20),        -- device is on 
        (49,    21),        -- device is off
        (49,    252),       -- The id of the entity needed for the trigger.
        (49,    409),       -- enitity domain.
        (49,    394),       -- device id.
        (49,    410),       -- type of trigger.
        (49,    411),       -- type of trigger .
        (49,    412),       -- type of condition.
        (49,    413),       -- type of condition.
        (49,    414),       -- type of action.
        (49,    415),       -- type of action.
        (49,    416);       -- type of action.
        
-- CONDITION INTEGRATION
/* import the integrations for conditions */

INSERT INTO integration(i_id, i_name)
VALUES  (50,    'trigger'),
        (51,    'automation'),
        (52,    'script');

-- POSSIBLE VALUES --
/* import the values from condition integrations */

INSERT INTO possible_values(pv_id, property, p_value)
VALUES 
/* datetime additions
        attributes extracted from: 
        https://www.home-assistant.io/docs/scripts/conditions/#time-condition
*/
        (417,       'weekday',                          'mon'),                                 -- If the day is monday
        (418,       'weekday',                          'tue'),                                 -- If the day is tuesday
        (419,       'weekday',                          'wed'),                                 -- If the day is wednesday
        (420,       'weekday',                          'thu'),                                 -- If the day is thursday
        (421,       'weekday',                          'fri'),                                 -- If the day is friday
        (422,       'weekday',                          'sat'),                                 -- If the day is saturday
        (423,       'weekday',                          'sun'),                                 -- If the day is sunday
/* automation
        states(main) extracted from:
        https://www.home-assistant.io/docs/automation/services/
*/
        (424,       'last_triggered',                   'datetime'),                            -- The last time the automation was triggered.
        (425,       'mode',                             'single'),                              -- The automation won't start if repeated.
        (426,       'mode',                             'restart'),                             -- The automation will restart up if repeated.
        (427,       'mode',                             'queued'),                              -- The automation is queued up if repeated.
        (428,       'mode',                             'parallel'),                            -- The automation is called parallel if repeated.
        (429,       'current',                          'int');                                 -- The current state (not running 0 / running 1) of the automation


INSERT INTO integration_values(i_id, pv_id)
VALUES 
        -- datetime additions
        (10,     417),      -- If the day is monday
        (10,     418),      -- If the day is tuesday
        (10,     419),      -- If the day is wednesday
        (10,     420),      -- If the day is thursday
        (10,     421),      -- If the day is friday
        (10,     422),      -- If the day is saturday
        (10,     423),      -- If the day is sunday
        -- trigger
        (50,     20),       -- The trigger is used.
        (50,     21),       -- The trigger is not used..
        (50,     251),      -- The id of the trigger.     
        -- automation
        (51,     12),       --Unknown state.
        (51,     13),       --The entity is not reachable.
        (51,     20),       --The automation is activated
        (51,     21),       --The automation is deactivated
        (51,     251),      --The id of the automation.
        (51,     424),      --The last time the automation was triggered.
        (51,     425),      --The automation won't start if repeated.
        (51,     426),      --The automation will restart up if repeated.
        (51,     427),      --The automation is queued up if repeated.
        (51,     428),      --The automation is called parallel if repeated.
        (51,     429),      --The current state (not running 0 / running 1) of the automation
        -- script
        (52,     12),       --Unknown state.
        (52,     13),       --The entity is not reachable.
        (52,     20),       --The script is activated
        (52,     21),       --The script is deactivated
        (52,     424),      --The last time the script was triggered.
        (52,     425),      --The script won't start if repeated.
        (52,     426),      --The script will restart up if repeated.
        (52,     427),      --The script is queued up if repeated.
        (52,     428),      --The script is called parallel if repeated.
        (52,     429);      --The current state (not running 0 / running 1) of the script