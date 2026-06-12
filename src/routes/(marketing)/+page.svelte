<script lang="ts">
	import DatingAppLogos from '$lib/components/landing/DatingAppLogos.svelte';
	import HeroStemPreview from '$lib/components/landing/HeroStemPreview.svelte';
	import NotifySignup from '$lib/components/landing/NotifySignup.svelte';
	import PromptStudio from '$lib/components/landing/PromptStudio.svelte';
	import SiteFaq from '$lib/components/landing/SiteFaq.svelte';
	import WaitlistCta from '$lib/components/landing/WaitlistCta.svelte';

	const steps = [
		{
			title: 'Upload a few selfies',
			body: 'We learn your face and style from your own photos.',
			image: '/how-it-works/step-upload.svg',
			imageAlt: 'Illustration of a few uploaded selfie photos'
		},
		{
			title: 'We train your Studio Model',
			body: 'A private model of you, tuned for realistic dating shots.',
			image: '/how-it-works/step-train.svg',
			imageAlt: 'Illustration of a computer training your personal model'
		},
		{
			title: 'Generate and pick winners',
			body: 'Describe the vibe, generate drafts, star your favorites, and tweak until they feel perfect.',
			image: '/how-it-works/step-generate.svg',
			imageAlt: 'Illustration of dating photos moving along a conveyor'
		}
	];
</script>

<section class="hero" aria-labelledby="hero-heading">
	<div class="hero__inner">
		<div class="hero__content">
			<span class="hero__eyebrow eyebrow">AI portrait studio</span>
			<h1 id="hero-heading">
				<span class="hero__title-line">Stop losing matches</span>
				<span class="hero__title-line hero__title-line--accent">to bad photos</span>
			</h1>
			<p class="hero__pitch">
				Your next dating photoshoot is AI-powered. Upload a few selfies and let
				<strong class="hero__pitch-brand">Visagely</strong> create dating photos that actually look like
				you. Our custom AI training technology learns your face and style to generate realistic,
				high-quality photos built to increase matches on Tinder, Hinge, Bumble, and more.
			</p>

			<DatingAppLogos />

			<div class="hero__actions">
				<a class="hero__cta btn btn-primary" href="#notify">Join waitlist to receive free tokens</a>
			</div>
		</div>

		<div class="hero__visual">
			<HeroStemPreview />
		</div>
	</div>

	<div class="hero-panels">
		<div class="hero-panels__inner">
			<div id="how-it-works" class="hero__details panel-glass">
				<div class="hero__details-header">
					<span class="hero__details-label eyebrow">Process</span>
					<h2>How it works</h2>
				</div>
				<ol class="hero__steps">
					{#each steps as step, i}
						<li class="hero__step">
							<span class="hero__step-num">{String(i + 1).padStart(2, '0')}</span>
							<div class="hero__step-main">
								<img
									class="hero__step-visual"
									src={step.image}
									alt={step.imageAlt}
									width="120"
									height="72"
									loading="lazy"
									decoding="async"
								/>
								<div class="hero__step-copy">
									<strong>{step.title}</strong>
									<p>{step.body}</p>
								</div>
							</div>
						</li>
					{/each}
				</ol>
			</div>

			<WaitlistCta
				paired
				heading="Better photos, more right swipes"
				body="Waitlist members get launch access plus free generation tokens to try Visagely Studio Model on their profile."
			/>
		</div>
	</div>
</section>

<PromptStudio />

<NotifySignup />

<SiteFaq />

<style>
	.hero {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: var(--space-hero-panels-gap);
	}

	.hero__inner {
		display: grid;
		grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
		gap: 4.5rem;
		align-items: start;
		width: 100%;
		max-width: 1920px;
		margin-inline: auto;
		padding: var(--space-hero-top) var(--space-page-x) 0;
		min-height: min(760px, calc(100dvh - 11rem));
	}

	.hero__visual {
		display: flex;
		justify-content: center;
		align-items: flex-start;
		align-self: start;
		min-width: 0;
		padding-top: 0.125rem;
	}

	/* below lg: hide preview, give text full width */
	@media (max-width: 1023px) {
		.hero__inner {
			grid-template-columns: 1fr;
			gap: 2.5rem;
			padding: var(--space-hero-top) var(--space-page-x) 0;
			min-height: auto;
		}

		.hero__visual {
			display: none;
		}

		.hero__pitch {
			max-width: none;
		}

		.hero__details {
			padding: 1.5rem 1.25rem;
		}
	}

	@media (max-width: 767px) {
		.hero__inner {
			padding: var(--space-hero-top) var(--space-page-x) 0;
		}
	}

	.hero__content {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		min-width: 0;
		width: 100%;
	}

	.hero__eyebrow {
		margin-bottom: -0.25rem;
	}

	.hero h1 {
		display: flex;
		flex-direction: column;
		font-family: var(--font-display);
		font-size: clamp(3rem, 4.8vw, 4.75rem);
		font-weight: 400;
		line-height: 0.98;
		letter-spacing: -0.01em;
		margin: 0;
	}

	.hero__title-line {
		color: var(--color-text);
	}

	.hero__title-line--accent {
		font-style: italic;
		font-weight: 500;
		background: linear-gradient(
			105deg,
			var(--color-champagne-bright) 0%,
			var(--color-accent-bright) 52%,
			var(--color-accent) 100%
		);
		-webkit-background-clip: text;
		background-clip: text;
		color: transparent;
	}

	.hero__pitch {
		font-size: 1.0625rem;
		line-height: 1.8;
		color: var(--color-text-muted);
		max-width: 34rem;
		margin: 0;
	}

	.hero__pitch-brand {
		color: var(--color-text);
		font-weight: 600;
		font-family: var(--font-display);
		font-size: 1.125em;
		letter-spacing: 0.01em;
	}

	.hero__actions {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.5rem;
		margin: 0;
	}

	.hero__cta.btn-primary {
		padding-inline: 1.65rem;
	}

	.hero-panels {
		width: 100%;
		max-width: 1920px;
		margin-inline: auto;
		padding: 0 var(--space-page-x) calc(var(--space-section-y) / 2);
	}

	.hero-panels__inner {
		display: grid;
		grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
		gap: 1rem;
		align-items: stretch;
	}

	.hero__details {
		padding: 2rem 2.25rem;
		margin: 0;
		width: 100%;
		box-sizing: border-box;
	}

	.hero__details-header {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 1.5rem;
	}

	.hero__details-label {
		margin-bottom: 0.15rem;
	}

	.hero__details h2 {
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 500;
		letter-spacing: 0.01em;
		color: var(--color-text);
		margin: 0;
	}

	.hero__steps {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.hero__step {
		display: grid;
		grid-template-columns: 2.5rem minmax(0, 1fr);
		gap: 1rem;
		align-items: start;
		width: 100%;
	}

	.hero__step-main {
		display: flex;
		align-items: flex-start;
		gap: 1rem;
		min-width: 0;
		flex: 1;
	}

	.hero__step-visual {
		flex-shrink: 0;
		width: 5.5rem;
		height: auto;
		border-radius: var(--radius-md);
		background: color-mix(in srgb, var(--color-surface) 80%, transparent);
		border: 1px solid var(--color-border-subtle);
	}

	.hero__step-num {
		font-family: var(--font-mono);
		font-size: 0.6875rem;
		font-weight: 500;
		color: var(--color-champagne);
		padding-top: 0.2rem;
		opacity: 0.85;
	}

	.hero__step-copy {
		min-width: 0;
	}

	.hero__steps strong {
		display: block;
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text);
		margin-bottom: 0.25rem;
	}

	.hero__steps p {
		margin: 0;
		font-size: 0.875rem;
		line-height: 1.55;
		color: var(--color-text-muted);
	}

	@media (max-width: 1023px) {
		.hero-panels {
			padding-inline: var(--space-page-x);
		}

		.hero-panels__inner {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 520px) {
		.hero__step {
			grid-template-columns: 2rem minmax(0, 1fr);
			gap: 0.75rem;
		}

		.hero__step-main {
			flex-direction: column;
			gap: 0.75rem;
		}

		.hero__step-visual {
			width: 6.5rem;
		}
	}
</style>
