<script lang="ts">
	let {
		heading = 'Ready for more matches?',
		body = 'Join the waitlist. Get early access and free tokens on launch day.',
		buttonLabel = 'Get early access',
		paired = false
	}: {
		heading?: string;
		body?: string;
		buttonLabel?: string;
		paired?: boolean;
	} = $props();
</script>

<section
	class="waitlist-cta"
	class:waitlist-cta--paired={paired}
	aria-labelledby="waitlist-cta-heading"
>
	<div class="waitlist-cta__inner panel-glass">
		<div class="waitlist-cta__copy">
			<h2 id="waitlist-cta-heading">{heading}</h2>
			<p>{body}</p>
		</div>
		<a class="waitlist-cta__btn btn btn-primary" href="#notify">{buttonLabel}</a>
	</div>
</section>

<style>
	.waitlist-cta {
		border-top: 1px solid var(--color-border-subtle);
		padding-inline: 4rem;
	}

	.waitlist-cta__inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 2rem;
		flex-wrap: wrap;
		max-width: 76rem;
		margin-inline: auto;
		padding: 2rem 2.25rem;
	}

	.waitlist-cta h2 {
		margin: 0 0 0.5rem;
		font-family: var(--font-display);
		font-size: clamp(1.5rem, 2.2vw, 1.875rem);
		font-weight: 500;
		letter-spacing: 0.01em;
		line-height: 1.1;
		color: var(--color-text);
	}

	.waitlist-cta p {
		margin: 0;
		font-size: 0.9375rem;
		line-height: 1.55;
		color: var(--color-text-muted);
		max-width: 32rem;
	}

	.waitlist-cta__btn {
		flex-shrink: 0;
	}

	.waitlist-cta--paired {
		border-top: none;
		padding: 0;
		min-width: 0;
		height: 100%;
	}

	.waitlist-cta--paired .waitlist-cta__inner {
		flex-direction: column;
		align-items: flex-start;
		justify-content: space-between;
		gap: 1.5rem;
		max-width: none;
		height: 100%;
		margin: 0;
		padding: 2rem;
		box-sizing: border-box;
	}

	.waitlist-cta--paired p {
		max-width: none;
	}

	@media (max-width: 640px) {
		.waitlist-cta:not(.waitlist-cta--paired) {
			padding-inline: 1.25rem;
		}

		.waitlist-cta__inner {
			padding: 1.5rem 1.25rem;
		}

		.waitlist-cta--paired .waitlist-cta__inner {
			padding: 1.5rem 1.25rem;
		}
	}
</style>
