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

INSERT INTO integration_values(i_id, pv_id)
VALUES	(1, 12),
        (1, 13),
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (1, 10),
        (1, 11);

/* binary_sensor 
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/binary-sensor
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/binary_sensor
*/
INSERT INTO possible_values(pv_id, p_value)
VALUES  (12,    'unknown'),	        --Unknown state.
        (13,    'unavailable'),         --The sensor is not reachable.
        (14,    'on'),	                --The sensor detects something.
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
INSERT INTO possible_values(pv_id, p_value)
VALUES  (16,    'pressed');             --The button is pressed.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(3, 12),
        (3, 13),
        (3, 16);


/* calendar
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES	(4, 12),
        (4, 13),
        (4, 14),
        (4, 15);

/* camera 
        states / inputs extracted from:

*/
INSERT INTO possible_values(pv_id, p_value)
VALUES  (17,    'idle'),                --The camera observes.
        (18,    'recording'),           --The camera records the recording.
        (19,    'streaming');           --The camera streams the recording.

INSERT INTO integration_values(i_id, pv_id)
VALUES	(5, 12),
        (5, 13),
        (5, 17),
        (5, 18),
        (5, 19);

/* climate  
        states / inputs extracted from:
        https://github.com/home-assistant/core/blob/dev/homeassistant/components/climate
        https://www.home-assistant.io/integrations/climate.mqtt/ 
        https://www.home-assistant.io/integrations/climate/
        https://developers.home-assistant.io/docs/core/entity/climate/
*/

INSERT INTO possible_values(i_id, pv_id)
VALUES  (20,    'auto'),                --The device is set to a schedule, learned behavior, AI.
        (21,    'cool'),                --The device is set to cool to a target temperature.
        (22,    'heat'),                --The device is set to heat to a target temperature.
        (23,    'heat_cool'),           --The device is set to heat/cool to a target temperature range.
        (24,    'dry'),                 --The device is set to dry/humidity mode.
        (25,    'fan_only'),            --The device only has the fan on. No heating or cooling taking place.
        (26,    'preheating'),          --Device is preheating.
        (27,    'heating'),             --Device is heating.
        (28,    'cooling'),             --Device is cooling.
        (29,    'drying'),              --Device is drying.
        (30,    'fan'),                 --Device has fan on.
        (31,    'defrosting'),          --Device is defrosting.
        (32,    'fan_on'),              --The fan is on.
        (33,    'fan_off'),             --The fan off.
        (34,    'fan_auto'),            --The fan turns on automatically.
        (35,    'fan_low'),             --The fan speed is low.
        (36,    'fan_medium'),          --The fan speed is medium.
        (37,    'fan_high'),            --The fan speed is high.
        (38,    'fan_middle'),          --The fan stays in the middle.
        (39,    'fan_focus'),           --The fan focuses in on direction.
        (40,    'fan_diffuse')          --The fan diffuse in all possible directions.
        (41,    'swing_off'),           --The fan don't swing.
        (42,    'swing_on'),            --The fan swings.
        (43,    'swing_vertical'),      --The fan swings vertically.
        (44,    'swing_horizontal'),    --The fan swings horizontally.
        (45,    'swing_both');          --The fan swings in both directions.

--not included: humidity, temperature - real
INSERT INTO integration_values(i_id, pv_id)
VALUES  (6, 12),
        (6, 13),
        (6, 15),
        (6, 20),
        (6, 21),
        (6, 22),
        (6, 23),
        (6, 24),
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

/* conversation 
        states / inputs extracted from:
        https://www.home-assistant.io/integrations/conversation/
        https://developers.home-assistant.io/docs/core/entity/conversation
*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (46,     'text')                --The said text in the converstation.

INSERT INTO integration_values(i_id, pv_id)
VALUES  (7, 12),
        (7, 13),
        (7, 46);

/* cover
        states / inputs extracted from:
        https://developers.home-assistant.io/docs/core/entity/cover

*/
INSERT INTO possible_values(i_id, pv_id)
VALUES  (47,     'closed'),             --The cover has reach the closed position.
        (48,     'closing'),            --The cover is in the process of closing to reach a set position.
        (49,     'open'),               --The cover has reached the open position.
        (50,     'opening'),            --The cover is in the process of opening to reach a set position


INSERT INTO integration_values(i_id, pv_id)
VALUES  (8, 12),
        (8, 13),


/* date
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* datetime
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* device_tracer
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* event
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* fan
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* humidifier
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* image
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* lawn_mower
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* light
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* lock
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* media_player
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* notify
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* number
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* remote
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* scene
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* select
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* sensor
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* siren
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* stt
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* switch
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* text
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* time
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* todo
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* tts
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* update
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* vacuum
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* valve
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* wake_word
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* water_heater
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES

/* weather
        states / inputs extracted from:
*/
INSERT INTO integration_values(i_id, pv_id)
VALUES
