/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export interface Env {
	// Example binding to KV. Learn more at https://developers.cloudflare.com/workers/runtime-apis/kv/
	// MY_KV_NAMESPACE: KVNamespace;
	//
	// Example binding to Durable Object. Learn more at https://developers.cloudflare.com/workers/runtime-apis/durable-objects/
	// MY_DURABLE_OBJECT: DurableObjectNamespace;
	//
	// Example binding to R2. Learn more at https://developers.cloudflare.com/workers/runtime-apis/r2/
	// MY_BUCKET: R2Bucket;
	//
	// Example binding to a Service. Learn more at https://developers.cloudflare.com/workers/runtime-apis/service-bindings/
	// MY_SERVICE: Fetcher;
	//
	// Example binding to a Queue. Learn more at https://developers.cloudflare.com/queues/javascript-apis/
	// MY_QUEUE: Queue;
	DB: D1Database;
}

export default {
	async fetch(request: Request, env: Env) {
		const { pathname } = new URL(request.url);

		if (pathname === '/get-all') {
			const url = new URL(request.url);
			const completed = url.searchParams.get('completed');
			let sql = 'SELECT * FROM Todos';

			if (completed) {
				sql += ` WHERE completed = ${completed === 'y' ? 1 : 0}`;
			}

			const { results } = await env.DB.prepare(sql).all();
			// If you did not use `DB` as your binding name, change it here
			return Response.json(results);
		}
		if (pathname === '/delete') {
			const url = new URL(request.url);
			const id = url.searchParams.get('id');

			let sql = `DELETE FROM Todos WHERE todoId = ?`;
			const { results } = await env.DB.prepare(sql).bind(id).all();
			return Response.json(results);
		}

		if (pathname === '/add') {
			let body = await request.json();
			const { title, description, context, due_date } = body;
			const sql = `
			INSERT INTO Todos (title, description, context, due_date)
			VALUES (?, ?, ?, ?)
		`;
			const parsedDate = due_date ? new Date(due_date) : new Date();
			const { results } = await env.DB.prepare(sql).bind(title, description, context, parsedDate.toUTCString()).all();

			return Response.json(results);
		}

		return new Response('Call /get-all to get all todos');
	},
};
