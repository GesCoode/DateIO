<script lang="ts">
	import InteractiveDots from '$lib/components/landing/InteractiveDots.svelte';
	import SiteHeader from '$lib/components/landing/SiteHeader.svelte';
	import SiteFooter from '$lib/components/landing/SiteFooter.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<title>Visagely — Dating photos that win more matches</title>
	<meta
		name="description"
		content="Visagely creates realistic AI dating photos from your selfies. Train your Studio Model and generate profile shots for Tinder, Hinge, Bumble, and more."
	/>
</svelte:head>

<div class="landing-shell">
	<div class="landing-shell__backdrop" aria-hidden="true">
		<div class="landing-shell__mesh"></div>
		<div class="landing-shell__vignette"></div>
		<InteractiveDots />
	</div>
	<SiteHeader />
	<main class="landing-main">
		{@render children()}
	</main>
	<SiteFooter />
</div>

<style>
	.landing-shell {
		position: relative;
		isolation: isolate;
		display: flex;
		flex-direction: column;
		min-height: 100dvh;
		overflow-x: clip;
		color: var(--color-text);
		font-family: var(--font-body);
		background-color: var(--color-bg);
	}

	.landing-shell__backdrop {
		pointer-events: none;
		position: fixed;
		inset: 0;
		z-index: -1;
		overflow: hidden;
	}

	.landing-shell__mesh {
		position: absolute;
		inset: 0;
		background:
			radial-gradient(ellipse 65% 50% at 12% 8%, var(--color-bg-mesh-b) 0%, transparent 55%),
			radial-gradient(ellipse 50% 42% at 92% 12%, var(--color-bg-mesh-c) 0%, transparent 50%),
			radial-gradient(ellipse 55% 48% at 78% 82%, var(--color-bg-mesh-a) 0%, transparent 52%),
			radial-gradient(ellipse 40% 35% at 28% 72%, var(--color-bg-mesh-b) 0%, transparent 48%),
			var(--color-bg);
	}

	.landing-shell__vignette {
		position: absolute;
		inset: 0;
		background: radial-gradient(
			ellipse 85% 70% at 50% 45%,
			transparent 35%,
			color-mix(in srgb, var(--color-bg) 55%, transparent) 100%
		);
	}

	.landing-main {
		flex: 1;
		display: flex;
		flex-direction: column;
		position: relative;
		z-index: 1;
	}
</style>
