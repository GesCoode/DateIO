<script lang="ts">
	type PreviewPhoto = {
		alt: string;
		label: string;
		src?: string;
		hue: number;
	};

	const photos: PreviewPhoto[] = [
		{
			alt: 'Generated dating photo in a café setting',
			label: 'Café candid',
			hue: 155
		},
		{
			alt: 'Generated dating photo at golden hour outdoors',
			label: 'Golden hour',
			hue: 42
		},
		{
			alt: 'Generated dating photo on a city evening',
			label: 'City evening',
			hue: 265
		}
	];

	function photoStyle(hue: number) {
		return `
			background:
				linear-gradient(
					145deg,
					color-mix(in srgb, hsl(${hue} 35% 22%) 90%, #0a0a0a) 0%,
					color-mix(in srgb, hsl(${hue} 25% 10%) 95%, #000) 55%,
					#0a0a0a 100%
				);
		`;
	}
</script>

<figure class="stem-preview" aria-label="Example Visagely dating profile photos">
	<figure class="stem-preview__photo stem-preview__photo--top">
		{#if photos[1].src}
			<img src={photos[1].src} alt={photos[1].alt} loading="lazy" />
		{:else}
			<div class="stem-preview__placeholder" style={photoStyle(photos[1].hue)}></div>
		{/if}
		<figcaption class="stem-preview__caption">{photos[1].label}</figcaption>
	</figure>

	<figure class="stem-preview__photo stem-preview__photo--left">
		{#if photos[0].src}
			<img src={photos[0].src} alt={photos[0].alt} loading="lazy" />
		{:else}
			<div class="stem-preview__placeholder" style={photoStyle(photos[0].hue)}></div>
		{/if}
		<figcaption class="stem-preview__caption">{photos[0].label}</figcaption>
	</figure>

	<figure class="stem-preview__photo stem-preview__photo--right">
		{#if photos[2].src}
			<img src={photos[2].src} alt={photos[2].alt} loading="lazy" />
		{:else}
			<div class="stem-preview__placeholder" style={photoStyle(photos[2].hue)}></div>
		{/if}
		<figcaption class="stem-preview__caption">{photos[2].label}</figcaption>
	</figure>
</figure>

<style>
	.stem-preview {
		position: relative;
		width: 100%;
		max-width: 34rem;
		height: min(540px, calc(100dvh - 15rem));
		min-height: 440px;
		margin-inline: auto;
		margin-top: 0;
		overflow: visible;
	}

	.stem-preview__photo {
		position: absolute;
		margin: 0;
		width: 38%;
		aspect-ratio: 10 / 19.5;
		border-radius: var(--radius-lg);
		overflow: hidden;
		border: 1px solid color-mix(in srgb, var(--color-champagne) 22%, var(--color-border));
		box-shadow:
			0 16px 40px -16px color-mix(in srgb, #000 75%, transparent),
			0 0 0 1px color-mix(in srgb, var(--color-champagne) 8%, transparent),
			inset 0 1px 0 color-mix(in srgb, #fff 5%, transparent);
		transition:
			transform 0.35s cubic-bezier(0.33, 1, 0.68, 1),
			box-shadow 0.35s ease;
	}

	.stem-preview__photo:hover {
		transform: translateY(-4px) scale(1.02);
		box-shadow:
			0 16px 40px -10px color-mix(in srgb, var(--color-accent) 25%, transparent),
			0 0 0 1px color-mix(in srgb, var(--color-accent-bright) 35%, transparent);
		z-index: 2;
	}

	.stem-preview__photo--top {
		top: 0;
		left: 50%;
		transform: translateX(-50%);
		width: 42%;
		z-index: 3;
	}

	.stem-preview__photo--top:hover {
		transform: translateX(-50%) translateY(-4px) scale(1.02);
	}

	.stem-preview__photo--left {
		left: 0;
		top: 24%;
		width: 36%;
		transform: rotate(-8deg);
		transform-origin: right center;
	}

	.stem-preview__photo--left:hover {
		transform: rotate(-8deg) translateY(-4px) scale(1.02);
	}

	.stem-preview__photo--right {
		right: 0;
		top: 16%;
		width: 36%;
		transform: rotate(9deg);
		transform-origin: left center;
	}

	.stem-preview__photo--right:hover {
		transform: rotate(7deg) translateY(-4px) scale(1.02);
	}

	.stem-preview__photo img,
	.stem-preview__placeholder {
		display: block;
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.stem-preview__placeholder {
		position: relative;
	}

	.stem-preview__placeholder::after {
		content: '';
		position: absolute;
		inset: 0;
		background: radial-gradient(
			ellipse 80% 70% at 50% 25%,
			color-mix(in srgb, var(--color-accent-bright) 12%, transparent) 0%,
			transparent 60%
		);
		pointer-events: none;
	}

	.stem-preview__caption {
		position: absolute;
		bottom: 0.5rem;
		left: 0.625rem;
		right: 0.625rem;
		margin: 0;
		padding: 0.3rem 0.6rem;
		font-family: var(--font-mono);
		font-size: 0.6875rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--color-text);
		background: color-mix(in srgb, #000 55%, transparent);
		border-radius: var(--radius-pill);
		text-align: center;
		backdrop-filter: blur(4px);
	}

	@media (prefers-reduced-motion: reduce) {
		.stem-preview__photo,
		.stem-preview__photo--top:hover,
		.stem-preview__photo--left:hover,
		.stem-preview__photo--right:hover {
			transition: none;
		}
	}
</style>
