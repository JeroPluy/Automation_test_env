-- STANDARD INTEGRATION
/* import the standard integrations */

INSERT INTO integration(i_name)
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
3,      
-- POSSIBLE VALUES
/* import the values from standard integrations */

/* alarm_control_panel */
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

INSERT INTO integration_values(i_id,pv_id)
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
        (1, 11);

/* binary_sensor */
INSERT INTO possible_values(pv_id, p_value)
VALUES  (12,    'unknown'),	        --Unknown state.
        (13,    'unavailable'),         --The sensor is not reachable.
        (14,    'on'),	                --The sensor detects something.
        (15,    'off');	                --The sensor detects nothing.

INSERT INTO integration_values(i_id,pv_id)
VALUES	(2, 12),
        (2, 13),
        (2, 14),
        (2, 15);


/* button */
INSERT INTO possible_values(p_value)
VALUES  (16,    'pressed');             --The button is pressed.

INSERT INTO integration_values(i_id,pv_id)
VALUES	(3, 12),
        (3, 13),
        (3, 16);


/* calendar */
INSERT INTO integration_values(i_id,pv_id)
VALUES	(4, 12),
        (4, 13),
        (4, 14),
        (4, 15);