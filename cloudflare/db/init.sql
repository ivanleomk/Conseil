DROP TABLE IF EXISTS Prompts;


DROP TABLE IF EXISTS Todos;
CREATE TABLE IF NOT EXISTS Todos (
    todoId INTEGER PRIMARY KEY, 
    title TEXT NOT NULL, 
    description TEXT NOT NULL, 
    context TEXT,
    due_date DATE DEFAULT (DATE('now')) NOT NULL,  
    completed_at DATE,
    completed BOOLEAN DEFAULT 0
);

DROP TABLE IF EXISTS Logs;
CREATE TABLE IF NOT EXISTS Logs (
    promptId INTEGER PRIMARY KEY, 
    message TEXT NOT NULL, 
    output TEXT NOT NULL, 
    tag TEXT
    createdAT Date DEFAULT (Date('now'))
);