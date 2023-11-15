import { D1Database } from '@cloudflare/workers-types/2023-07-01/index';

export const getAllLogs = async (db: D1Database) => {
	const sql = 'SELECT * FROM Logs';
	const { results } = await db.prepare(sql).all();

	return results;
};

export const getAllTodos = async (db: D1Database, completed: string | null, start: string | null, end: string | null) => {
	let sql = `SELECT * FROM Todos`;

	if (completed) {
		if (completed !== 'y' && completed !== 'n') {
			throw new Error(`Completed only takes in an argument of y or no. ${completed} was passed instead.`);
		}
		sql += ` WHERE completed = ${completed === 'y' ? 1 : 0}`;
	}

	if (start) {
		let StartDate;
		try {
			StartDate = new Date(start).toISOString().split('T')[0];

			sql += ` ${sql.includes('WHERE') ? 'AND' : ' WHERE'} date(due_date) >= date('${StartDate}')`;
		} catch (error) {
			throw new Error('Unable to parse start date');
		}
	}

	if (end) {
		let EndDate;
		try {
			EndDate = new Date(end).toISOString().slice(0, 10);
			sql += ` ${sql.includes('WHERE') ? 'AND' : 'WHERE'} due_date <= '${EndDate}'`;
		} catch (error) {
			throw new Error('Unable to parse end date');
		}
	}
	const { results } = await db.prepare(`${sql};`).all();
	return results;
};

export const addLogItem = async (db: D1Database, body: { input: string; output: string; tag: string }) => {
	const { input, output, tag } = body;
	const sql = `INSERT INTO Logs (Message, Output, tag) VALUES (?, ?, ?) RETURNING *`;

	const response = await db.prepare(sql).bind(input, output, tag).first();

	return response;
};

export const deleteTodoItem = async (db: D1Database, id: string) => {
	const sql = `DELETE FROM Todos WHERE todoId = ? RETURNING *`;
	const { results } = await db.prepare(sql).bind(id).all();
	return Response.json(results);
};

export const addTodoItem = async (
	db: D1Database,
	body: {
		title?: string;
		description?: string;
		context?: string;
		due_date?: string;
	}
) => {
	const { title, description, context, due_date } = body;
	if (!title || !description) {
		throw new Error('Invalid Response Body');
	}
	const sql = `INSERT INTO Todos (title, description, context, due_date) VALUES (?, ?, ?, ?) RETURNING *`;
	try {
		const parsedDate = due_date ? new Date(due_date) : new Date();
		const response = await db.prepare(sql).bind(title, description, context, parsedDate.toISOString().slice(0, 10)).first();

		if (!response) {
			throw Error();
		}

		return response;
	} catch (error) {
		throw new Error('Unable to add new todo item');
	}
};
