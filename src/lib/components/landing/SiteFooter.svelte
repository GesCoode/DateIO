<script lang="ts">
	const year = new Date().getFullYear();
</script>

<footer class="site-footer landing-section">
	<div class="site-footer__inner landing-section__inner">
		<div class="site-footer__brand">
			<p class="site-footer__name">
				<span class="site-footer__mark" aria-hidden="true"></span>
				Visagely
			</p>
			<p class="site-footer__tagline">Dating photos that win more matches.</p>
			<a class="site-footer__domain" href="https://visagely.com">visagely.com</a>
		</div>

		<p class="site-footer__meta" aria-label="Footer links and trust">
			<a class="site-footer__meta-link" href="#faq">Q&amp;A</a>
			<span class="site-footer__meta-sep" aria-hidden="true">·</span>
			<span>Privacy-first pipeline</span>
			<span class="site-footer__meta-sep" aria-hidden="true">·</span>
			<span>Studio Model technology</span>
		</p>

		<p class="site-footer__copy">&copy; {year} Visagely. All rights reserved.</p>
	</div>
</footer>

<style>
	.site-footer {
		background: transparent;
	}

	.site-footer__inner {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		grid-template-rows: auto auto;
		gap: 0.75rem 2.5rem;
		align-items: start;
	}

	.site-footer__brand {
		grid-column: 1;
		grid-row: 1;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		min-width: 0;
	}

	.site-footer__name {
		display: inline-flex;
		align-items: center;
		gap: 0.55rem;
		font-family: var(--font-display);
		font-weight: 500;
		font-size: 1.25rem;
		letter-spacing: 0.02em;
		color: var(--color-text);
		margin: 0;
	}

	.site-footer__mark {
		width: 0.5rem;
		height: 0.5rem;
		border-radius: 50%;
		border: 1px solid var(--color-champagne);
		flex-shrink: 0;
	}

	.site-footer__tagline {
		font-size: 0.875rem;
		line-height: 1.5;
		color: var(--color-text-muted);
		margin: 0;
	}

	.site-footer__domain {
		font-family: var(--font-mono);
		font-size: 0.6875rem;
		letter-spacing: 0.08em;
		text-transform: lowercase;
		color: var(--color-text-subtle);
		text-decoration: none;
		transition: color 0.2s ease;
	}

	.site-footer__domain:hover {
		color: var(--color-champagne);
	}

	.site-footer__meta {
		grid-column: 1;
		grid-row: 2;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.45rem 0.65rem;
		margin: 0;
		font-family: var(--font-mono);
		font-size: 0.625rem;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--color-text-subtle);
	}

	.site-footer__meta-link {
		color: inherit;
		text-decoration: none;
		transition: color 0.15s ease;
	}

	.site-footer__meta-link:hover {
		color: var(--color-champagne);
	}

	.site-footer__meta-sep {
		opacity: 0.35;
		user-select: none;
	}

	.site-footer__copy {
		grid-column: 2;
		grid-row: 1;
		justify-self: end;
		align-self: center;
		margin: 0;
		font-size: 0.75rem;
		color: var(--color-text-subtle);
		text-align: right;
		white-space: nowrap;
	}

	@media (max-width: 768px) {
		.site-footer__inner {
			grid-template-columns: 1fr;
			gap: 1rem;
		}

		.site-footer__copy {
			grid-column: 1;
			grid-row: 3;
			justify-self: start;
			text-align: left;
			padding-top: 0.75rem;
			border-top: 1px solid var(--color-border-subtle);
			width: 100%;
			white-space: normal;
		}
	}
</style>
