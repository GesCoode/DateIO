import { getSql } from '$lib/server/db';

export type WaitlistSignup = {
	id: string;
	email: string;
	createdAt: string;
};

type WaitlistRow = {
	id: string;
	email: string;
	created_at: Date;
};

function mapSignup(row: WaitlistRow): WaitlistSignup {
	return {
		id: row.id,
		email: row.email,
		createdAt: row.created_at.toISOString()
	};
}

export async function joinWaitlist(email: string): Promise<WaitlistSignup> {
	const sql = getSql();
	const normalizedEmail = email.trim().toLowerCase();

	const rows = await sql<WaitlistRow[]>`
    INSERT INTO waitlist_signups (email)
    VALUES (${normalizedEmail})
    ON CONFLICT (email) DO UPDATE SET email = EXCLUDED.email
    RETURNING id, email, created_at
  `;

	return mapSignup(rows[0]);
}
