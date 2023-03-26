-- CREATE TABLE
DROP TABLE IF EXISTS covid_cases;
CREATE TABLE covid_cases (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR NOT NULL,
    new_positive_cases INTEGER NOT NULL
);