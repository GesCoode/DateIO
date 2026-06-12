<script lang="ts">
	let email = $state('');
	let submitted = $state(false);
	let submitting = $state(false);
	let error = $state('');

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		error = '';

		const trimmed = email.trim();
		if (!trimmed || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed)) {
			error = 'Please enter a valid email address.';
			return;
		}

		submitting = true;

		try {
			const response = await fetch('/api/waitlist', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email: trimmed })
			});

			const data = (await response.json()) as { error?: string };

			if (!response.ok) {
				error = data.error ?? 'Could not join the waitlist. Please try again.';
				return;
			}

			submitted = true;
		} catch {
			error = 'Could not join the waitlist. Please try again.';
		} finally {
			submitting = false;
		}
	}
</script>

<section id="notify" class="notify landing-section" aria-labelledby="notify-heading">
	<div class="notify__spotlight" aria-hidden="true"></div>

	<div class="notify__inner landing-section__inner">
		<header class="notify__copy">
			<span class="notify__label eyebrow">Early access</span>
			<h2 id="notify-heading">Get on the list</h2>
			<p class="notify__lede">
				Join the waitlist for launch access and <strong>free generation tokens</strong>.
			</p>
			<ul class="notify__perks" aria-label="Waitlist benefits">
				<li>Free tokens on launch day</li>
				<li>First in line when Visagely opens</li>
				<li>One email at launch. No spam.</li>
			</ul>
		</header>

		<div class="notify__form-wrap">
			<div class="notify__form-border" aria-hidden="true"></div>
			<div class="notify__form-surface">
				<span class="notify__form-badge">Join the waitlist now!</span>
				{#if submitted}
				<p class="notify__success" role="status">
					You are on the list. We will email you at launch with your free tokens.
				</p>
			{:else}
				<form class="notify__form" onsubmit={handleSubmit} novalidate>
					<label class="notify__field-label" for="notify-email">Email</label>
					<div class="notify__form-row">
						<input
							id="notify-email"
							type="email"
							name="email"
							autocomplete="email"
							placeholder="you@example.com"
							bind:value={email}
							required
						/>
						<button type="submit" class="btn btn-light notify__submit" disabled={submitting}>
							{submitting ? 'Joining…' : 'Join waitlist'}
						</button>
					</div>
					{#if error}
						<p class="notify__error" role="alert">{error}</p>
					{/if}
				</form>
				{/if}
			</div>
		</div>
	</div>
</section>

<style>
	.notify {
		position: relative;
		overflow: hidden;
		background:
			radial-gradient(ellipse 80% 70% at 72% 42%, color-mix(in srgb, var(--color-accent) 8%, transparent), transparent 58%),
			radial-gradient(ellipse 45% 38% at 18% 78%, color-mix(in srgb, var(--color-champagne) 6%, transparent), transparent 52%),
			var(--color-bg);
	}

	.notify__inner {
		position: relative;
		z-index: 1;
		max-width: 76rem;
		margin-inline: auto;
		display: grid;
		grid-template-columns: minmax(0, 1fr) minmax(0, 38rem);
		gap: 2.5rem 3.5rem;
		align-items: center;
	}

	.notify__spotlight {
		position: absolute;
		z-index: 0;
		top: 50%;
		right: 8%;
		width: min(42rem, 55vw);
		height: min(28rem, 70%);
		transform: translateY(-50%);
		background: radial-gradient(
			ellipse at center,
			color-mix(in srgb, var(--color-champagne) 12%, transparent) 0%,
			color-mix(in srgb, var(--color-accent) 6%, transparent) 42%,
			transparent 72%
		);
		pointer-events: none;
		animation: notify-spotlight 7s ease-in-out infinite alternate;
	}

	.notify__label {
		display: block;
		margin-bottom: 0.65rem;
	}

	.notify h2 {
		font-family: var(--font-display);
		font-size: clamp(2.25rem, 3.2vw, 3rem);
		font-weight: 500;
		letter-spacing: 0.01em;
		color: var(--color-text);
		margin: 0 0 1rem;
		line-height: 1.05;
	}

	.notify__lede {
		font-size: 1.1875rem;
		line-height: 1.6;
		color: var(--color-text-muted);
		margin: 0;
		max-width: 32rem;
	}

	.notify__lede strong {
		color: var(--color-champagne-bright);
		font-weight: 600;
	}

	.notify__perks {
		margin: 1.25rem 0 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.notify__perks li {
		position: relative;
		padding-left: 1.35rem;
		font-size: 0.9375rem;
		line-height: 1.45;
		color: var(--color-text-subtle);
	}

	.notify__perks li::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0.5em;
		width: 0.35rem;
		height: 0.35rem;
		border-radius: 50%;
		background: var(--color-champagne);
		box-shadow: 0 0 10px var(--color-champagne-soft);
	}

	.notify__form-wrap {
		position: relative;
		z-index: 1;
		width: 100%;
		min-height: 9.5rem;
		border-radius: var(--radius-xl);
	}

	.notify__form-border {
		position: absolute;
		inset: 0;
		border-radius: inherit;
		padding: 1px;
		background: linear-gradient(
			135deg,
			color-mix(in srgb, var(--color-champagne) 55%, transparent),
			color-mix(in srgb, var(--color-accent) 30%, transparent) 42%,
			color-mix(in srgb, var(--color-accent-bright) 45%, transparent) 72%,
			color-mix(in srgb, var(--color-champagne) 35%, transparent)
		);
		background-size: 200% 200%;
		animation: notify-border-shift 8s ease infinite;
		mask:
			linear-gradient(#fff 0 0) content-box,
			linear-gradient(#fff 0 0);
		mask-composite: exclude;
		-webkit-mask-composite: xor;
		pointer-events: none;
	}

	.notify__form-surface {
		position: relative;
		display: flex;
		align-items: center;
		min-height: 9.5rem;
		padding: 2rem 2.25rem;
		border-radius: inherit;
		background:
			linear-gradient(
				155deg,
				color-mix(in srgb, var(--color-accent) 10%, var(--color-surface-elevated)) 0%,
				color-mix(in srgb, var(--color-surface-elevated) 94%, #000) 45%,
				var(--color-surface) 100%
			);
		box-shadow:
			0 0 0 1px color-mix(in srgb, var(--color-accent) 22%, transparent),
			0 0 48px -12px var(--color-accent-glow),
			0 24px 48px -28px color-mix(in srgb, #000 70%, transparent);
		backdrop-filter: blur(14px);
	}

	.notify__form-badge {
		position: absolute;
		top: 0;
		right: 1.25rem;
		transform: translateY(-50%);
		padding: 0.55rem 1.15rem;
		font-family: var(--font-display);
		font-size: 0.9375rem;
		font-weight: 600;
		letter-spacing: -0.02em;
		text-transform: none;
		color: var(--color-champagne-bright);
		background: color-mix(in srgb, var(--color-bg) 78%, var(--color-surface-elevated));
		border: 1px solid color-mix(in srgb, var(--color-champagne) 35%, var(--color-border));
		border-radius: var(--radius-pill);
		box-shadow: 0 4px 16px -8px color-mix(in srgb, #000 80%, transparent);
		pointer-events: none;
		user-select: none;
	}

	.notify__form {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 0.65rem;
	}

	.notify__form-row {
		display: flex;
		align-items: center;
		gap: 0.65rem;
	}

	.notify__field-label {
		font-family: var(--font-mono);
		font-size: 0.625rem;
		font-weight: 500;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--color-text-subtle);
	}

	.notify__form input {
		flex: 1;
		min-width: 0;
		height: 2.75rem;
		padding: 0 1rem;
		font-size: 0.9375rem;
		font-family: inherit;
		border: 1px solid color-mix(in srgb, var(--color-border) 80%, var(--color-accent) 20%);
		border-radius: var(--radius-md);
		background: color-mix(in srgb, var(--color-bg) 65%, var(--color-surface));
		color: var(--color-text);
		outline: none;
		transition:
			border-color 0.15s ease,
			box-shadow 0.15s ease;
	}

	.notify__form input::placeholder {
		color: var(--color-text-subtle);
	}

	.notify__form input:focus {
		border-color: color-mix(in srgb, var(--color-accent) 45%, var(--color-border));
		box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 14%, transparent);
	}

	.notify__form .btn {
		flex-shrink: 0;
	}

	.notify__submit.btn-light {
		padding-inline: 1.5rem;
	}

	.notify__error {
		margin: 0;
		font-size: 0.8125rem;
		color: #f87171;
	}

	.notify__success {
		margin: 0;
		font-size: 0.9375rem;
		font-weight: 500;
		line-height: 1.5;
		color: var(--color-accent-bright);
	}

	@media (max-width: 900px) {
		.notify__inner {
			grid-template-columns: 1fr;
			gap: var(--space-block);
			max-width: 44rem;
		}
	}

	@keyframes notify-spotlight {
		from {
			opacity: 0.75;
			transform: translateY(-48%) scale(1);
		}
		to {
			opacity: 1;
			transform: translateY(-52%) scale(1.06);
		}
	}

	@keyframes notify-border-shift {
		0%,
		100% {
			background-position: 0% 50%;
		}
		50% {
			background-position: 100% 50%;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.notify__spotlight,
		.notify__form-border {
			animation: none;
		}
	}

	@media (max-width: 900px) {
		.notify__spotlight {
			right: 50%;
			top: 72%;
			width: 100%;
			height: 20rem;
			transform: translate(50%, -50%);
		}
	}

	@media (max-width: 640px) {
		.notify__form-wrap,
		.notify__form-surface {
			min-height: 12.5rem;
		}

		.notify__form-surface {
			align-items: stretch;
			padding: 1.75rem 1.25rem 1.5rem;
		}

		.notify__form-badge {
			right: 0.75rem;
			font-size: 0.8125rem;
			padding: 0.5rem 0.9rem;
		}

		.notify__form-row {
			flex-direction: column;
			align-items: stretch;
		}

		.notify__form input {
			width: 100%;
			height: 2.75rem;
			flex: none;
		}

		.notify__form .btn {
			width: 100%;
		}
	}
</style>
