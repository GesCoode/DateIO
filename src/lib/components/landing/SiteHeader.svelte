<script lang="ts">
	const brand = 'Visagely';
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

<div class="site-header-spacer" aria-hidden="true"></div>

<div class="site-header-wrap" class:scrolled>
	<header class="site-header">
		<div class="site-header__inner">
			<a href="/" class="site-header__brand">
				<span class="site-header__mark" aria-hidden="true"></span>
				<span class="site-header__wordmark">{brand}</span>
			</a>
			<nav class="site-header__nav" aria-label="Primary">
				<a class="site-header__link" href="#how-it-works">How it works</a>
				<a class="site-header__link" href="#prompt-studio">Studio</a>
				<a class="site-header__link" href="#faq">Q&amp;A</a>
				<a href="#notify" class="site-header__nav-cta btn btn-primary btn--compact">Get early access</a>
			</nav>
		</div>
	</header>
</div>

<style>
	.site-header-spacer {
		flex-shrink: 0;
		height: 4.25rem;
	}

	.site-header-wrap {
		--header-gutter: clamp(1.25rem, 4vw, 4rem);
		--header-float-top: 0.875rem;

		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 100;
		padding: 0;
		pointer-events: none;
		transition: padding 0.5s var(--ease-out-expo);
	}

	.site-header-wrap.scrolled {
		padding: var(--header-float-top) var(--header-gutter) 0;
	}

	.site-header {
		pointer-events: auto;
		border-bottom: 1px solid transparent;
		background: transparent;
		border-radius: 0;
		transition:
			border-radius 0.5s var(--ease-out-expo),
			border-color 0.5s var(--ease-out-expo),
			box-shadow 0.5s var(--ease-out-expo),
			background 0.5s var(--ease-out-expo);
	}

	.site-header-wrap.scrolled .site-header {
		border-radius: var(--radius-pill);
		border: 1px solid var(--color-glass-border);
		box-shadow: var(--shadow-glass);
		background: color-mix(in srgb, var(--color-glass) 88%, transparent);
		backdrop-filter: blur(24px) saturate(1.2);
	}

	.site-header__inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1.5rem;
		max-width: 76rem;
		margin-inline: auto;
		padding: 1.1rem var(--space-page-x);
		transition: padding 0.5s var(--ease-out-expo);
	}

	.site-header-wrap.scrolled .site-header__inner {
		padding: 0.75rem 1.5rem;
	}

	.site-header__brand {
		display: inline-flex;
		align-items: center;
		gap: 0.75rem;
		text-decoration: none;
		color: var(--color-text);
	}

	.site-header__wordmark {
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 500;
		letter-spacing: 0.02em;
		line-height: 1;
		transition: font-size 0.5s var(--ease-out-expo);
	}

	.site-header-wrap.scrolled .site-header__wordmark {
		font-size: 1.35rem;
	}

	.site-header__mark {
		width: 0.625rem;
		height: 0.625rem;
		border-radius: 50%;
		border: 1.5px solid var(--color-champagne);
		box-shadow: 0 0 14px var(--color-champagne-soft);
		flex-shrink: 0;
	}

	.site-header__nav {
		display: flex;
		align-items: center;
		gap: 1.75rem;
	}

	.site-header__link {
		font-size: 0.8125rem;
		font-weight: 500;
		letter-spacing: 0.02em;
		color: var(--color-text-muted);
		text-decoration: none;
		transition: color 0.2s ease;
	}

	.site-header__link:hover {
		color: var(--color-champagne-bright);
	}

	.site-header__nav-cta {
		color: var(--color-on-accent) !important;
	}

	@media (max-width: 768px) {
		.site-header__link {
			display: none;
		}

		.site-header__inner {
			padding-inline: 1.25rem;
		}

		.site-header-wrap.scrolled .site-header__inner {
			padding-inline: 1.15rem;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.site-header-wrap,
		.site-header,
		.site-header__inner,
		.site-header__wordmark {
			transition: none;
		}
	}
</style>
