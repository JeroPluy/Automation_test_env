-- STANDARD INTEGRATION
/* import the standard integrations */

INSERT INTO integration(i_name)
VALUES  ('alarm_control_panel'),
        ('binary_sensor'),
        ('button'),
        ('calendar'),
        ('camera'),
        ('climate'),
        ('conversation'),
        ('cover'),
        ('date'),
        ('datetime'),
        ('device_tracker'),
        ('event'),
        ('fan'),
        ('humidifier'),
        ('image'),
        ('lawn_mower'),
        ('light'),
        ('lock'),
        ('media_player'),
        ('notify'),
        ('number'),
        ('remote'),
        ('scene'),
        ('select'),
        ('sensor'),
        ('siren'),
        ('stt'),
        ('switch'),
        ('text'),
        ('time'),
        ('todo'),
        ('tts'),
        ('update'),
        ('vacuum'),
        ('valve'),
        ('wake_word'),
        ('water_heater'),
        ('weather');

-- POSSIBLE VALUES
/* import the values from standard integrations */

/* alarm_control_panel */
INSERT INTO integration(p_value,i_id)
VALUES  ('None', 1),	            --Unknown state.
        ('disarmed', 1),	        --The alarm is disarmed (off).
        ('armed_home', 1),	        --The alarm is armed in home mode.
        ('armed_away', 1),	        --The alarm is armed in away mode.
        ('armed_night', 1),	        --The alarm is armed in night mode.
        ('armed_vacation', 1),	    --The alarm is armed in vacation mode.
        ('armed_custom_bypass', 1), --The alarm is armed in bypass mode.
        ('pending', 1),	            --The alarm is pending (towards triggered).
        ('arming', 1),	            --The alarm is arming.
        ('disarming', 1),	        --The alarm is disarming.
        ('triggered', 1);           --The alarm is triggered.

/* binary_sensor */
INSERT INTO integration(p_value,i_id)
VALUES  ('unknown', 2),	    --Unknown state.
        ('unavailable', 2), --The sensor is not reachable.
        ('on', 2),	        --The sensor detects something.
        ('off', 2),	        --The sensor detects nothing.

/* button */
INSERT INTO integration(p_value,i_id)
VALUES  ('unknown', 3),	        --Unknown state.
        ('unavailable', 3),	    --The button is not reachable.
        ('pressed', 3),	        --The button is pressed.

/* calendar */
INSERT INTO integration(p_value,i_id)
VALUES  ('unknown', 3),	        --Unknown state.
        ('unavailable', 3),	    --The button is not reachable.
        ('pressed', 3),	        --The button is pressed.
        ('pressed', 3),	        --The button is pressed.
