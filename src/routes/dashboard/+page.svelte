<script lang="ts">
	import GenerationCard from '$lib/components/dashboard/GenerationCard.svelte';
	import { recentGenerations } from '$lib/data/dashboard-demo';

	type HubFrame = {
		id: string;
		title: string;
		description: string;
		href?: string;
	};

	const hubFrames: HubFrame[] = [
		{
			id: 'loras',
			title: "LoRA's",
			description: 'Browse and manage your trained likeness models.'
		},
		{
			id: 'prompt-studio',
			title: 'Prompt studio',
			description: 'Keywords, eight drafts, favorites, and refine — all in one flow.'
		},
		{
			id: 'library',
			title: 'Library',
			description: 'Every generation you have saved, sorted and ready to export.'
		}
	];
</script>

<div class="overview">
	<div class="overview__toolbar">
		<p class="overview__intro">Pick a workspace or train a new model.</p>
		<button type="button" class="overview__train">Train new LoRA</button>
	</div>

	<section class="overview__hub" aria-label="Workspaces">
		{#each hubFrames as frame (frame.id)}
			<button type="button" class="overview__frame panel-glass">
				<span class="overview__frame-label">{frame.title}</span>
				<p class="overview__frame-desc">{frame.description}</p>
				<span class="overview__frame-arrow" aria-hidden="true">→</span>
			</button>
		{/each}
	</section>

	<section class="overview__recent" aria-labelledby="recent-heading">
		<div class="overview__recent-header">
			<div>
				<span class="overview__section-label">Recent</span>
				<h2 id="recent-heading">Latest generations</h2>
			</div>
		</div>
		<div class="overview__grid">
			{#each recentGenerations as generation (generation.id)}
				<GenerationCard {generation} />
			{/each}
		</div>
	</section>
</div>

<style>
	.overview {
		display: flex;
		flex-direction: column;
		gap: 2.5rem;
	}

	.overview__toolbar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1.5rem;
		flex-wrap: wrap;
		padding-top: 0.5rem;
	}

	.overview__intro {
		margin: 0;
		font-size: 1rem;
		color: var(--color-text-muted);
	}

	.overview__train {
		padding: 0.65rem 1.25rem;
		font-size: 0.9375rem;
		font-weight: 600;
		font-family: inherit;
		color: var(--color-text);
		background: transparent;
		border: 1px solid var(--color-border);
		border-radius: var(--radius-pill);
		cursor: pointer;
		transition:
			border-color 0.15s ease,
			background 0.15s ease,
			transform 0.15s ease;
	}

	.overview__train:hover {
		border-color: color-mix(in srgb, var(--color-accent) 45%, var(--color-border));
		background: var(--color-accent-soft);
		transform: translateY(-1px);
	}

	.overview__hub {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 1.25rem;
	}

	.overview__frame {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.75rem;
		min-height: 11rem;
		padding: 1.75rem 1.75rem 1.5rem;
		text-align: left;
		font-family: inherit;
		cursor: pointer;
		transition:
			box-shadow 0.2s ease,
			transform 0.2s ease,
			border-color 0.2s ease;
	}

	.overview__frame:hover {
		transform: translateY(-2px);
		box-shadow:
			var(--shadow-glass),
			0 0 0 1px color-mix(in srgb, var(--color-accent) 22%, transparent);
	}

	.overview__frame-label {
		font-family: var(--font-display);
		font-size: clamp(1.5rem, 2.2vw, 2rem);
		font-weight: 700;
		letter-spacing: -0.03em;
		color: var(--color-text);
	}

	.overview__frame-desc {
		margin: 0;
		font-size: 0.9375rem;
		line-height: 1.55;
		color: var(--color-text-muted);
		max-width: 22rem;
		flex: 1;
	}

	.overview__frame-arrow {
		margin-top: auto;
		font-size: 1.25rem;
		color: var(--color-accent-bright);
		opacity: 0.85;
		transition: transform 0.2s ease;
	}

	.overview__frame:hover .overview__frame-arrow {
		transform: translateX(4px);
	}

	.overview__section-label {
		font-family: var(--font-mono);
		font-size: 0.625rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--color-text-subtle);
	}

	.overview__recent-header h2 {
		margin: 0.35rem 0 0;
		font-family: var(--font-display);
		font-size: 1.25rem;
		font-weight: 700;
		letter-spacing: -0.02em;
	}

	.overview__recent-header {
		margin-bottom: 1.25rem;
	}

	.overview__grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(11.5rem, 1fr));
		gap: 1rem;
	}

	@media (max-width: 900px) {
		.overview__hub {
			grid-template-columns: 1fr;
		}

		.overview__frame {
			min-height: 9rem;
		}
	}
</style>
