<script lang="ts">
	import { demoUser } from '$lib/data/dashboard-demo';

	const SCROLL_THRESHOLD = 56;

	let scrolled = $state(false);

	function updateScrolled() {
		scrolled = window.scrollY > SCROLL_THRESHOLD;
	}

	$effect(() => {
		updateScrolled();
		window.addEventListener('scroll', updateScrolled, { passive: true });
		return () => window.removeEventListener('scroll', updateScrolled);
	});
</script>

<div class="dash-header-spacer" aria-hidden="true"></div>

<div class="dash-header-wrap" class:scrolled>
	<header class="dash-header">
		<div class="dash-header__inner">
			<a href="/dashboard" class="dash-header__brand">
				<span class="dash-header__mark" aria-hidden="true"></span>
				Visagely
			</a>

			<div class="dash-header__actions">
				<div class="dash-header__tokens" title="Generation tokens remaining">
					<span class="dash-header__tokens-num">{demoUser.tokens}</span>
					<span class="dash-header__tokens-label">tokens</span>
				</div>
				<button type="button" class="dash-header__buy btn btn-primary btn--compact">Buy tokens</button>
				<button type="button" class="dash-header__avatar" aria-label="Account menu">
					<span aria-hidden="true">{demoUser.name.charAt(0)}</span>
				</button>
			</div>
		</div>
	</header>
</div>

<style>
	.dash-header-spacer {
		flex-shrink: 0;
		height: 4.5rem;
	}

	.dash-header-wrap {
		--header-gutter: clamp(1.25rem, 3vw, 2.5rem);
		--header-float-top: 0.75rem;

		position: fixed;
		top: 0;
		left: var(--dash-sidebar-width, 15.5rem);
		right: 0;
		z-index: 100;
		padding: 0;
		pointer-events: none;
		transition: padding 0.45s cubic-bezier(0.33, 1, 0.68, 1);
	}

	.dash-header-wrap.scrolled {
		padding: var(--header-float-top) var(--header-gutter) 0;
	}

	.dash-header {
		pointer-events: auto;
		border-bottom: 1px solid transparent;
		background: transparent;
		border-radius: 0;
		transition:
			border-radius 0.45s cubic-bezier(0.33, 1, 0.68, 1),
			border-color 0.45s cubic-bezier(0.33, 1, 0.68, 1),
			box-shadow 0.45s cubic-bezier(0.33, 1, 0.68, 1),
			background 0.45s cubic-bezier(0.33, 1, 0.68, 1);
	}

	.dash-header-wrap.scrolled .dash-header {
		border-radius: var(--radius-pill);
		border: 1px solid var(--color-glass-border);
		box-shadow: var(--shadow-glass);
		background: var(--color-glass);
		backdrop-filter: blur(16px);
	}

	.dash-header__inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1.5rem;
		padding: 1.25rem 2.5rem;
		transition: padding 0.45s cubic-bezier(0.33, 1, 0.68, 1);
	}

	.dash-header-wrap.scrolled .dash-header__inner {
		padding: 0.875rem 1.75rem;
	}

	.dash-header__brand {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		font-family: var(--font-display);
		font-size: 1.25rem;
		font-weight: 700;
		letter-spacing: -0.03em;
		color: var(--color-text);
		text-decoration: none;
		transition: font-size 0.45s cubic-bezier(0.33, 1, 0.68, 1);
	}

	.dash-header-wrap.scrolled .dash-header__brand {
		font-size: 1.125rem;
	}

	.dash-header__mark {
		width: 0.5rem;
		height: 0.5rem;
		border-radius: 50%;
		border: 1px solid var(--color-champagne);
		background: transparent;
		box-shadow: 0 0 10px var(--color-accent-glow);
		flex-shrink: 0;
	}

	.dash-header__actions {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.dash-header__tokens {
		display: flex;
		align-items: baseline;
		gap: 0.35rem;
		padding: 0.45rem 0.85rem;
		border-radius: var(--radius-pill);
		border: 1px solid var(--color-border-subtle);
		background: color-mix(in srgb, var(--color-surface) 60%, transparent);
	}

	.dash-header-wrap.scrolled .dash-header__tokens {
		border-color: color-mix(in srgb, var(--color-glass-border) 80%, transparent);
		background: color-mix(in srgb, var(--color-surface-elevated) 50%, transparent);
	}

	.dash-header__tokens-num {
		font-family: var(--font-display);
		font-size: 1.125rem;
		font-weight: 700;
		color: var(--color-accent-bright);
	}

	.dash-header__tokens-label {
		font-size: 0.8125rem;
		color: var(--color-text-muted);
	}

	.dash-header__avatar {
		width: 2.5rem;
		height: 2.5rem;
		border-radius: 50%;
		border: 1px solid var(--color-border);
		background: var(--color-surface-elevated);
		color: var(--color-accent-bright);
		font-family: var(--font-display);
		font-size: 1rem;
		font-weight: 700;
		cursor: pointer;
		transition: border-color 0.15s ease;
	}

	.dash-header__avatar:hover {
		border-color: color-mix(in srgb, var(--color-accent) 45%, var(--color-border));
	}

	@media (max-width: 768px) {
		.dash-header-wrap {
			left: 0;
		}

		.dash-header__inner {
			padding: 1.25rem 1.25rem;
		}

		.dash-header-wrap.scrolled .dash-header__inner {
			padding: 0.875rem 1.25rem;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.dash-header-wrap,
		.dash-header,
		.dash-header__inner,
		.dash-header__brand {
			transition: none;
		}
	}
</style>
