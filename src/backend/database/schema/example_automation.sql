INSERT INTO automation (a_name, autom_mode, max_instances, script)
VALUES (
        'example_automation',
        0,
        1,
        'AUTOMATION_SCRIPT_PATH\example_automation.py'
    );
INSERT INTO additional_information (a_id, info_type, info)
VALUES (1, "project", "example_project");
INSERT INTO additional_information (a_id, info_type, info)
VALUES (1, "version", 1);
INSERT INTO additional_information (a_id, info_type, info)
VALUES (
        1,
        "description",
        "This is an example automation."
    );
INSERT INTO entity (e_name, i_id)
VALUES ("binary_sensor.test_sensor", 2);
INSERT INTO automation_entity (a_id, e_id, p_role, position, exp_val)
VALUES (
        1,
        1,
        0,
        0,
        "{'to': 'off'}"
    );
INSERT INTO entity (e_name, i_id)
VALUES ("media_player.test_actor", 19);
INSERT INTO automation_entity (a_id, e_id, p_role, position, exp_val)
VALUES (
        1,
        2,
        3,
        0,
        "{'action': 'media_pause'}"
    );