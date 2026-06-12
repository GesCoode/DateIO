import { json, type RequestHandler } from '@sveltejs/kit';
import { joinWaitlist } from '$lib/server/waitlist';

export const POST: RequestHandler = async ({ request }) => {
	let body: { email?: string };

	try {
		body = await request.json();
	} catch {
		return json({ error: 'Invalid request body.' }, { status: 400 });
	}

	const email = body.email?.trim() ?? '';

	if (!email) {
		return json({ error: 'Please enter your email address.' }, { status: 400 });
	}

	if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
		return json({ error: 'Please enter a valid email address.' }, { status: 400 });
	}

	try {
		const signup = await joinWaitlist(email);

		return json({
			ok: true,
			email: signup.email
		});
	} catch (error) {
		console.error('Waitlist signup failed:', error);
		return json({ error: 'Could not join the waitlist. Please try again.' }, { status: 500 });
	}
};
