import postgres from 'postgres';
import { requireEnv } from '$lib/server/env';

let sql: ReturnType<typeof postgres> | null = null;

export function getSql() {
	if (!sql) {
		sql = postgres(requireEnv('DATABASE_URL'), { max: 4, idle_timeout: 20 });
	}

	return sql;
}
