INSERT INTO automation(
        a_name,
        created,
        autom_mode,
        max_instances,
        script,
        error
    )
VALUES (
        'test_automation_123',
        CURRENT_TIMESTAMP,
        0,
        1,
        'test_automation_123.py',
        0
    );
INSERT INTO entity(e_id, e_name, i_id)
VALUES (1, 'binary_sensor.testsensor2', 2);
INSERT INTO entity(e_id, e_name, i_id)
VALUES (2, 'sun', 41);
INSERT INTO entity(e_id, e_name, i_id)
VALUES (3, 'sensor.example3', 25);
INSERT INTO automation_entity(a_id, e_id, p_role, position, exp_val)
VALUES (1, 1, 1, 0, 5);
INSERT INTO automation_entity(a_id, e_id, p_role, position, exp_val)
VALUES (1, 2, 1, 1, 20);
INSERT INTO automation_entity(a_id, e_id, p_role, position, exp_val)
VALUES (1, 3, 1, 2, 10);
SELECT a.a_name,
    e.e_name,
    i.i_name,
    p_role,
    position
FROM automation_entity
    JOIN entity AS e ON automation_entity.e_id = e.e_id
    JOIN integration AS i ON e.i_id = i.i_id
    JOIN automation AS a ON automation_entity.a_id = a.a_id
WHERE a.a_id == 1;
SELECT pos_val.*
FROM automation_entity AS ae
    JOIN entity AS e ON ae.e_id = e.e_id
    JOIN integration AS i ON e.i_id = i.i_id
    JOIN integration_values AS iv ON i.i_id = iv.i_id
    JOIN possible_values AS pos_val ON iv.pv_id = pos_val.pv_id
WHERE ae.position == 0;