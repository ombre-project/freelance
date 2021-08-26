DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id serial PRIMARY KEY,
    full_name text,
    email text UNIQUE,
    hashed_password text NOT NULL,
    is_active boolean,
    wallet_address text,
    is_complete_user boolean,
    born DATE,
    city text,
    country text,
    address text,
    bio text,
    resume_address text,
    img_address text,
    password_omb text NOT NULL,
    username_omb text UNIQUE
);

CREATE TABLE projects (
    id_proj serial PRIMARY KEY,
    name text NOT NULL,
    description text NOT NULL,
    is_finish boolean ,
    start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    is_pay boolean DEFAULT false,
    is_taken boolean DEFAULT false,
    common int DEFAULT 0,
    common_describe text ,
    cost FLOAT DEFAULT 0.0,
    img_addr text,
    file_addr text,
    end_date DATE,
    address_of_project_uploaded text,
    project_owner_id int ,
    project_offer_id int ,
    FOREIGN KEY(project_owner_id) REFERENCES users(id),
    FOREIGN KEY(project_offer_id) REFERENCES users(id)
);