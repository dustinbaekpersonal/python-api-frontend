
-- Create Mock DB for templateapp DB tables
-- version: 1
-- date: 13 May 2020

CREATE TABLE IF NOT EXISTS codes_mcc_all (
        code SERIAL NOT NULL,
        combined_description VARCHAR(255),
        description VARCHAR(255),
        edited_description VARCHAR(255),
        irs_description VARCHAR(255),
        irs_reportable VARCHAR(255),
        usda_description VARCHAR(255),
        PRIMARY KEY (code)
);
