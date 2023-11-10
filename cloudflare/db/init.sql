DROP TABLE IF EXISTS Todos;
CREATE TABLE IF NOT EXISTS Todos (
    todoId INTEGER PRIMARY KEY, 
    title TEXT NOT NULL, 
    description TEXT NOT NULL, 
    context TEXT,
    due_date DATE DEFAULT (DATE('now')), 
    completed BOOLEAN DEFAULT 0
);

DROP TABLE IF EXISTS Prompts;
CREATE TABLE IF NOT EXISTS Prompts (
    Message TEXT NOT NULL, 
    Output TEXT NOT NULL, 
    tag TEXT
);