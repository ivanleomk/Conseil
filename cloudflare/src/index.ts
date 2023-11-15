/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

import { addLogItem, addTodoItem, deleteTodoItem, getAllLogs, getAllTodos } from './helpers';

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

const supportedRoutes = {
	GET_LOGS: '/get-logs',
	GET_ALL_TODOS: '/get-all',
	ADD_LOG_ITEM: '/add-log',
	DELETE_TODO_ITEM: '/delete',
	ADD_TODO_ITEM: '/add',
};

export default {
	async fetch(request: Request, env: Env) {
		const { pathname } = new URL(request.url);

		if (pathname === supportedRoutes.GET_LOGS && request.method === 'GET') {
			const data = await getAllLogs(env.DB);
			return Response.json(data);
		}

		if (pathname === supportedRoutes.GET_ALL_TODOS && request.method === 'GET') {
			const url = new URL(request.url);
			const completed = url.searchParams.get('completed');
			const start = url.searchParams.get('start');
			const end = url.searchParams.get('end');
			const data = await getAllTodos(env.DB, completed, start, end);
			return Response.json(data);
		}

		if (pathname === supportedRoutes.ADD_LOG_ITEM && request.method === 'POST') {
			const data = await addLogItem(env.DB, await request.json());
			return Response.json(data);
		}

		if (pathname === supportedRoutes.DELETE_TODO_ITEM && request.method === 'POST') {
			const url = new URL(request.url);
			const id = url.searchParams.get('id');

			if (!id) {
				throw new Error('A valid ID must be supplied.');
			}

			const data = await deleteTodoItem(env.DB, id);
			return Response.json(data);
		}

		if (pathname === supportedRoutes.ADD_TODO_ITEM && request.method === 'POST') {
			const data = await addTodoItem(env.DB, await request.json());
			return Response.json(data);
		}

		throw new Error(`Invalid Route of ${pathname} supplied. Please double check parameters supplied.`);
	},
};
