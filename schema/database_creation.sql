-- AUTOMATION
/* basic information of automations */


CREATE TABLE automation
(
    a_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    a_name        TEXT NOT NULL,
    created       TEXT NOT NULL, -- Using TEXT for datetime
    autom_mode    INTEGER NOT NULL,
    max_instances INTEGER NOT NULL,
    script        TEXT NOT NULL,
    error         INTEGER
);


-- INFORMATION
/* additional information for automations */

CREATE TABLE additional_information
(
    info_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    info_type TEXT NOT NULL,
    info      TEXT NOT NULL,
    a_id      INTEGER NOT NULL,
    FOREIGN KEY (a_id) REFERENCES automation (a_id)
);

-- INTEGRATION
/* integration (user generated or from Home Assistant) */

CREATE TABLE integration
(
    i_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    i_name TEXT NOT NULL
);

-- ENTITY
/* represents entities from Home Assistant */


CREATE TABLE entity
(
    e_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    e_name TEXT NOT NULL,
    i_id   INTEGER NOT NULL,
    FOREIGN KEY (i_id) REFERENCES integration (i_id)
);

-- POSSIBLE VALUE
/* possible values of the integrations */

CREATE TABLE possible_values
(
    pv_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    p_value  NUMERIC NOT NULL,
    i_id     INTEGER NOT NULL,
    FOREIGN KEY (i_id) REFERENCES integration (i_id)
);

-- AUTOMATION ENTITY
/* parameter of automations */

CREATE TABLE automation_entity
(
    a_id      INTEGER NOT NULL,
    e_id      INTEGER NOT NULL,
    p_role    INTEGER NOT NULL,
    position  INTEGER NOT NULL,
    exp_val   NUMERIC NOT NULL,
    PRIMARY KEY (a_id, e_id, p_role, position),
    FOREIGN KEY (a_id) REFERENCES automation (a_id),
    FOREIGN KEY (e_id) REFERENCES entity (e_id)
);

-- TEST CASE
/* information to test cases of automations */

CREATE TABLE test_case
(
    case_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    c_timestamp TEXT NOT NULL, -- Using TEXT for datetime
    requirement NUMERIC,
    case_priority  INTEGER,
    a_id        INTEGER NOT NULL,
    FOREIGN KEY (a_id) REFERENCES automation (a_id)
);

-- TEST CASE INPUT
/* input values for test cases */

CREATE TABLE test_case_input
(
    case_input_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_value    NUMERIC NOT NULL,
    case_id       INTEGER NOT NULL,
    a_id          INTEGER NOT NULL,
    e_id          INTEGER NOT NULL,
    p_role        INTEGER NOT NULL,
    position      INTEGER NOT NULL,
    FOREIGN KEY (case_id) REFERENCES test_case (case_id),
    FOREIGN KEY (a_id, e_id, p_role, position) REFERENCES automation_entity (a_id, e_id, p_role, position)
);

-- TEST CASE COLLECTION
/* saved selection of test cases */

CREATE TABLE test_case_collection
(
    tcc_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    tcc_name TEXT NOT NULL,
    a_id     INTEGER NOT NULL,
    FOREIGN KEY (a_id) REFERENCES automation (a_id)
);

-- TEST CASE COLLECTION TEST CASE
/* test cases of the selection of test cases */

CREATE TABLE case_collection_test_cases
(
    tcc_id  INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    PRIMARY KEY (tcc_id, case_id),
    FOREIGN KEY (tcc_id) REFERENCES test_case_collection (tcc_id),
    FOREIGN KEY (case_id) REFERENCES test_case (case_id)
);

-- TEST EXECUTION
/* information of the test executions */

CREATE TABLE test_execution
(
    te_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ex_timestamp   TEXT NOT NULL, -- Using TEXT for datetime
    exec_mode      TEXT NOT NULL,
    exec_group     INTEGER NOT NULL,
    error_type     TEXT,
    error_comment  TEXT,
    case_id        INTEGER NOT NULL,
    a_id           INTEGER NOT NULL,
    FOREIGN KEY (case_id) REFERENCES test_case (case_id),
    FOREIGN KEY (a_id) REFERENCES automation (a_id)
);


-- TEST EXECUTION OUTPUT
/* output parameter of the execution */

CREATE TABLE test_execution_output
(
    teo_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    output_val  NUMERIC,
    te_id       INTEGER NOT NULL,
    a_id        INTEGER NOT NULL,
    e_id        INTEGER NOT NULL,
    p_role      INTEGER NOT NULL,
    position    INTEGER NOT NULL,
    FOREIGN KEY (te_id) REFERENCES test_execution (te_id),
    FOREIGN KEY (a_id, e_id, p_role, position) REFERENCES automation_entity (a_id, e_id, p_role, position)
);