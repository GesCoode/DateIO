<script lang="ts">
	import bumbleLogo from '$lib/assets/Bumble.svg';
	import happnLogo from '$lib/assets/Happn.svg';
	import hingeLogo from '$lib/assets/Hinge.svg';
	import okCupidLogo from '$lib/assets/OkCupid.svg';
	import tinderLogo from '$lib/assets/Tinder.svg';

	type DatingApp = {
		name: string;
		logo: string;
	};

	const apps: DatingApp[] = [
		{ name: 'Tinder', logo: tinderLogo },
		{ name: 'Hinge', logo: hingeLogo },
		{ name: 'Bumble', logo: bumbleLogo },
		{ name: 'OkCupid', logo: okCupidLogo },
		{ name: 'Happn', logo: happnLogo }
	];
</script>

<div class="dating-logos panel-glass">
	<p class="dating-logos__label eyebrow">Optimized for these dating apps</p>
	<ul class="dating-logos__list" aria-label="Tinder, Hinge, Bumble, OkCupid, Happn">
		{#each apps as app (app.name)}
			<li>
				<img
					class="dating-logos__img"
					src={app.logo}
					alt={app.name}
					width="28"
					height="28"
					loading="lazy"
				/>
			</li>
		{/each}
	</ul>
</div>

<style>
	.dating-logos {
		display: flex;
		flex-direction: column;
		gap: 0.85rem;
		padding: 1rem 1.25rem;
		border-radius: var(--radius-lg);
		width: fit-content;
		max-width: 100%;
	}

	.dating-logos__label {
		margin: 0;
	}

	.dating-logos__list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 1rem 1.35rem;
	}

	.dating-logos__img {
		display: block;
		height: 1.5rem;
		width: auto;
		max-width: 5rem;
		object-fit: contain;
		opacity: 0.72;
		filter: grayscale(0.15);
		transition:
			opacity 0.25s ease,
			transform 0.25s var(--ease-out-expo),
			filter 0.25s ease;
	}

	.dating-logos__list li:hover .dating-logos__img {
		opacity: 1;
		filter: grayscale(0);
		transform: translateY(-1px);
	}
</style>
