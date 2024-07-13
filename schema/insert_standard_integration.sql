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
        (26,    'siren'),
        (27,    'stt'),
        (28,    'switch'),
        (29,    'text'),
        (30,    'time'),
        (31,    'todo'),
        (32,    'tts'),
        (33,    'update'),
        (34,    'vacuum'),
        (35,    'valve'),
        (36,    'wake_word'),
        (37,    'water_heater'),
        (38,    'weather');
  
-- POSSIBLE VALUES --
/* import the values from standard integrations */

/* alarm_control_panel 
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/alarm-control-panel
*/
INSERT INTO possible_values(pv_id, p_value)
VALUES  (1,     'None'),	        --Unknown state.
        (2,     'disarmed'),	        --The alarm is disarmed (off).
        (3,     'armed_home'),	        --The alarm is armed in home mode.
        (4,     'armed_away'),	        --The alarm is armed in away mode.
        (5,     'armed_night'),	        --The alarm is armed in night mode.
        (6,     'armed_vacation'),	--The alarm is armed in vacation mode.
        (7,     'armed_custom_bypass'), --The alarm is armed in bypass mode.
        (8,     'pending'),	        --The alarm is pending (towards triggered).
        (9,     'arming'),	        --The alarm is arming.
        (10,    'disarming'),	        --The alarm is disarming.
        (11,    'triggered');           --The alarm is triggered.
        (12,    'unknown'),	        --Unknown state.
        (13,    'unavailable'),         --The entity is not reachable.

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

/* binary_sensor 
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/binary-sensor
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/binary_sensor
*/
INSERT INTO possible_values(pv_id, p_value)
VALUES  (14,    'on'),	                --The sensor detects something.
        (15,    'off');	                --The sensor detects nothing.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(2, 12),
        (2, 13),
        (2, 14),
        (2, 15);


/* button 
        states / inputs extracted from:
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/button
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES	(3, 12),
        (3, 13);


/* calendar
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/calendar
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/calendar
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES	(4, 12),
        (4, 13),
        (4, 14),
        (4, 15);

/* camera 
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/camera
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/camera

*/
INSERT INTO possible_values(pv_id, p_value)
VALUES  (16,    'idle'),                --The camera observes.
        (17,    'recording'),           --The camera records the recording.
        (18,    'streaming');           --The camera streams the recording.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(5, 12),
        (5, 13),
        (5, 16),
        (5, 17),
        (5, 18);

/* climate  
        states / inputs extracted from:
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/climate
        https://www.home-assistant.io/integrations/climate.mqtt/ 
        https://www.home-assistant.io/integrations/climate/
        https://developers.home-assistant.io/docs/core/entity/climate/
*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (19,    'auto'),                --The device is set to a schedule, learned behavior, AI.
        (20,    'cool'),                --The device is set to cool to a target temperature.
        (21,    'heat'),                --The device is set to heat to a target temperature.
        (22,    'heat_cool'),           --The device is set to heat/cool to a target temperature range.
        (23,    'dry'),                 --The device is set to dry/humidity mode.
        (24,    'fan_only'),            --The device only has the fan on. No heating or cooling taking place.
        --- everything below are attributes --- 
        /*
        (25,    'preheating'),          --Device is preheating.
        (26,    'heating'),             --Device is heating.
        (27,    'cooling'),             --Device is cooling.
        (28,    'drying'),              --Device is drying.
        (29,    'fan'),                 --Device has fan on.
        (30,    'defrosting'),          --Device is defrosting.
        -- fan_modes --
        (31,    'fan_on'),              --The fan is on.
        (32,    'fan_off'),             --The fan off.
        (33,    'fan_auto'),            --The fan turns on automatically.
        (34,    'fan_low'),             --The fan speed is low.
        (35,    'fan_medium'),          --The fan speed is medium.
        (36,    'fan_high'),            --The fan speed is high.
        (37,    'fan_middle'),          --The fan stays in the middle.
        (38,    'fan_focus'),           --The fan focuses in on direction.
        (39,    'fan_diffuse')          --The fan diffuse in all possible directions.
        -- swing_modes --
        (40,    'swing_off'),           --The fan don't swing.
        (41,    'swing_on'),            --The fan swings.
        (42,    'swing_vertical'),      --The fan swings vertically.
        (43,    'swing_horizontal'),    --The fan swings horizontally.
        (44,    'swing_both');          --The fan swings in both directions.
        */

--not included: humidity, temperature - real
INSERT INTO integration_values(i_id, pv_id)
VALUES  (6, 12),
        (6, 13),
        (6, 15),
        (6, 20),
        (6, 21),
        (6, 22),
        (6, 23),
        (6, 24);
        /*
        (6, 25),
        (6, 26),
        (6, 27),
        (6, 28),
        (6, 29),
        (6, 30),
        (6, 31),
        (6, 32),
        (6, 33),
        (6, 34),
        (6, 35),
        (6, 36),
        (6, 37),
        (6, 38),
        (6, 39),
        (6, 40),
        (6, 41),
        (6, 42),
        (6, 43),
        (6, 44),
        (6, 45);
        */

/* conversation 
        states / inputs extracted from:
        https://www.home-assistant.io/integrations/conversation/
        https://developers.home-assistant.io/docs/core/entity/conversation
*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (25,     'text')                --The scentence in the converstation.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (7, 12),
        (7, 13),
        (7, 25);

/* cover
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/cover

*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (26,     'closed'),             --The cover has reach the closed position.
        (27,     'closing'),            --The cover is in the process of closing to reach a set position.
        (28,     'open'),               --The cover has reached the open position.
        (29,     'opening');            --The cover is in the process of opening to reach a set position

INSERT INTO integration_values(i_id, pv_id)
VALUES  (8, 12),
        (8, 13),
        (8, 26),
        (8, 27),
        (8, 28),
        (8, 29);

/* date
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/date
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/date
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (9, 12),
        (9, 13),
        (9, 25);

/* datetime
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/datetime
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/datetime
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (10, 12),
        (10, 13),
        (10, 25);

/* device_tracer
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/device-tracker
*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (30,     'home'),               --The device is home.
        (31,     'not_home');           --The cover is not home.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (11, 12),
        (11, 13),
        (11, 30),
        (11, 31):

/* event
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/event
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/event
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (12, 12),
        (12, 13),
        (12, 25);

/* fan
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/fan
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/fan
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (13, 12),
        (13, 13),
        (13, 14),
        (13, 15);

/* humidifier
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/humidifier
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/humidifier
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (14, 12),
        (14, 13),
        (14, 14),
        (14, 15);

/* image
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/image
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (15, 12),
        (15, 13),
        (15, 25);

/* lawn_mower
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/lawn-mower
        https://github.com/home-assistant/core/tree/dev/homeassistant/components/lawn_mower

*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (32,    "mowing"), 	        --The lawn mower is currently mowing.
        (33,    "docked"),	        --The lawn mower is done mowing and is currently docked.
        (34,    "paused"),	        --The lawn mower was active and is now paused.
        (35,    "error");       	--The lawn mower encountered an error while active and needs assistance.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (16, 12),
        (16, 13),
        (16, 32),
        (16, 33),
        (16, 34),
        (16, 35);

/* light
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/light
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES  (17, 12),
        (17, 13),
        (17, 14),
        (17, 15);

/* lock
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/lock
*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (36,    "jammed"),              --The lock is unabled to toggle.
        (37,    "locked"),              --The lock is locked.
        (38,    "locking"),             --The lock is looking.
        (39,    "unlocked"),            --The lock is unlocked.
        (40,    "unlocking");           --The lock is unlooking.

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

/* media_player
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/media-player
*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (41,    "playing"),             --The media player playimg something.
        (42,    "standby"),             --The media player is in standby mode.
        (43,    "buffering");           --The media player buffering something.

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

/* notify
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/notify
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* number
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/number
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* remote
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/remote
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* scene
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/scene
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* select
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/select
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* sensor
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/sensor
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* siren
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/siren
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* stt
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/stt
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* switch
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/switch
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* text
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/text
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* time
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/time
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* todo
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/todo
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* tts
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/tts
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* update
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/update
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* vacuum
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/vacuum
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* valve
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/valve
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* wake_word
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/wake_word
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* water_heater
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/water-heater
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* weather
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/weather
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES
