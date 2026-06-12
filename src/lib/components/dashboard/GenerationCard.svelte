<script lang="ts">
	import type { Generation } from '$lib/data/dashboard-demo';

	let { generation }: { generation: Generation } = $props();

	function thumbStyle(hue: number) {
		return `
			background: linear-gradient(
				165deg,
				color-mix(in srgb, hsl(${hue} 42% 16%) 92%, #000) 0%,
				color-mix(in srgb, hsl(${hue} 32% 7%) 96%, #000) 100%
			);
		`;
	}
</script>

<article class="gen-card panel-glass">
	<div class="gen-card__thumb" style={thumbStyle(generation.hue)} role="img" aria-label={generation.scene}>
		{#if generation.favorite}
			<span class="gen-card__fav" aria-label="Favorite">★</span>
		{/if}
	</div>
	<div class="gen-card__body">
		<h3>{generation.scene}</h3>
		<p>{generation.prompt}</p>
		<footer>
			<time datetime="">{generation.createdAt}</time>
			<button type="button" class="gen-card__action">Open</button>
		</footer>
	</div>
</article>

<style>
	.gen-card {
		display: flex;
		flex-direction: column;
		overflow: hidden;
		padding: 0;
		transition: box-shadow 0.15s ease;
	}

	.gen-card:hover {
		box-shadow:
			var(--shadow-glass),
			0 0 0 1px color-mix(in srgb, var(--color-accent) 20%, transparent);
	}

	.gen-card__thumb {
		position: relative;
		aspect-ratio: 4 / 5;
		width: 100%;
	}

	.gen-card__fav {
		position: absolute;
		top: 0.5rem;
		right: 0.5rem;
		font-size: 0.75rem;
		color: var(--color-accent-bright);
		text-shadow: 0 0 8px var(--color-accent-glow);
	}

	.gen-card__body {
		padding: 0.875rem 1rem 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
		flex: 1;
	}

	.gen-card h3 {
		margin: 0;
		font-size: 0.9375rem;
		font-weight: 600;
		color: var(--color-text);
	}

	.gen-card p {
		margin: 0;
		font-size: 0.8125rem;
		line-height: 1.45;
		color: var(--color-text-muted);
		display: -webkit-box;
		-webkit-line-clamp: 2;
		line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}

	.gen-card footer {
		margin-top: auto;
		padding-top: 0.5rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
	}

	.gen-card time {
		font-size: 0.75rem;
		color: var(--color-text-subtle);
	}

	.gen-card__action {
		padding: 0.3rem 0.65rem;
		font-size: 0.75rem;
		font-weight: 600;
		font-family: inherit;
		color: var(--color-text-muted);
		background: transparent;
		border: 1px solid var(--color-border);
		border-radius: var(--radius-pill);
		cursor: pointer;
		transition:
			border-color 0.15s ease,
			color 0.15s ease;
	}

	.gen-card__action:hover {
		color: var(--color-text);
		border-color: color-mix(in srgb, var(--color-accent) 40%, var(--color-border));
	}
</style>
