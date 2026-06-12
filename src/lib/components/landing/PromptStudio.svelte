<script lang="ts">
	type Draft = {
		id: number;
		scene: string;
		hue: number;
	};

	type DraftCount = 1 | 2 | 4 | 8;

	type DemoScenario = {
		keywords: string[];
		prompt: string;
		draftCount: DraftCount;
		pickDraftId: number;
	};

	const draftCountOptions: { count: DraftCount; label: string }[] = [
		{ count: 1, label: '1 draft' },
		{ count: 2, label: '2 drafts' },
		{ count: 4, label: '4 drafts' },
		{ count: 8, label: '8 drafts' }
	];

	const premadeKeywords = [
		'warm smile',
		'golden hour',
		'café candid',
		'outdoor portrait',
		'city evening',
		'wine bar',
		'natural light',
		'candid laugh',
		'rooftop',
		'confident pose',
		'park walk',
		'travel vibe'
	];

	const demoScenarios: DemoScenario[] = [
		{
			draftCount: 8,
			keywords: ['café candid', 'warm smile', 'golden hour'],
			prompt: 'Relaxed smile, looking at camera, soft window light, date-night energy',
			pickDraftId: 3
		},
		{
			draftCount: 4,
			keywords: ['rooftop', 'city evening', 'confident pose'],
			prompt: 'Golden hour skyline behind me, natural laugh, smart casual, open posture',
			pickDraftId: 2
		},
		{
			draftCount: 2,
			keywords: ['wine bar', 'candid laugh', 'natural light'],
			prompt: 'Cozy booth, warm ambient light, holding a drink, approachable vibe',
			pickDraftId: 2
		},
		{
			draftCount: 1,
			keywords: ['park walk', 'outdoor portrait', 'travel vibe'],
			prompt: 'Sunday morning path, soft greenery, casual jacket, eye contact with camera',
			pickDraftId: 1
		}
	];

	const drafts: Draft[] = [
		{ id: 1, scene: 'Café window', hue: 145 },
		{ id: 2, scene: 'Rooftop sunset', hue: 95 },
		{ id: 3, scene: 'Park path', hue: 125 },
		{ id: 4, scene: 'Bookshop', hue: 160 },
		{ id: 5, scene: 'City night', hue: 175 },
		{ id: 6, scene: 'Beach walk', hue: 110 },
		{ id: 7, scene: 'Wine bar', hue: 135 },
		{ id: 8, scene: 'Garden terrace', hue: 150 }
	];

	type Phase =
		| 'keywords'
		| 'typing'
		| 'generating'
		| 'revealing'
		| 'picking'
		| 'focus-loading'
		| 'save-ready'
		| 'saving';

	let phase = $state<Phase>('keywords');
	let scenarioIndex = $state(0);
	let draftCount = $state<DraftCount>(8);
	let litKeywords = $state<string[]>([]);
	let typedText = $state('');
	let visibleDrafts = $state(0);
	let pickDraftId = $state<number | null>(null);
	let focusDraftId = $state<number | null>(null);
	let actionsVisible = $state(false);
	let savePressed = $state(false);

	const focusDraft = $derived(drafts.find((d) => d.id === focusDraftId) ?? null);
	const deckPicked = $derived(focusDraftId !== null);
	const activeDrafts = $derived(drafts.filter((d) => d.id <= draftCount));

	function draftStyle(draft: Draft, highlighted: boolean) {
		return `
			background: linear-gradient(
				165deg,
				color-mix(in srgb, hsl(${draft.hue} 42% 16%) 92%, #000) 0%,
				color-mix(in srgb, hsl(${draft.hue} 32% 7%) 96%, #000) 100%
			);
			${highlighted ? 'box-shadow: 0 0 0 2px var(--color-accent-bright);' : ''}
		`;
	}

	function stepLabel(current: Phase, count: DraftCount) {
		switch (current) {
			case 'generating':
				return `Generating ${count} photo${count === 1 ? '' : 's'}…`;
			case 'revealing':
				return 'Showing results…';
			case 'picking':
				return 'Pick a favorite…';
			case 'focus-loading':
				return 'Upscaling selected photo…';
			case 'save-ready':
			case 'saving':
				return 'Save, favorite, or put back';
			default:
				return `Next: generate ${count} photo${count === 1 ? '' : 's'}`;
		}
	}

	type LoopSignal = {
		cancelled: boolean;
		timeouts: ReturnType<typeof setTimeout>[];
	};

	function wait(ms: number, signal: LoopSignal) {
		return new Promise<void>((resolve) => {
			const id = setTimeout(() => {
				if (!signal.cancelled) resolve();
			}, ms);
			signal.timeouts.push(id);
		});
	}

	function resetScenario(count: DraftCount) {
		draftCount = count;
		litKeywords = [];
		typedText = '';
		visibleDrafts = 0;
		pickDraftId = null;
		focusDraftId = null;
		actionsVisible = false;
		savePressed = false;
		phase = 'keywords';
	}

	$effect(() => {
		const signal: LoopSignal = { cancelled: false, timeouts: [] };
		const reducedMotion =
			typeof window !== 'undefined' &&
			window.matchMedia('(prefers-reduced-motion: reduce)').matches;

		async function runScenario(scenario: DemoScenario) {
			resetScenario(scenario.draftCount);

			if (reducedMotion) {
				litKeywords = [...scenario.keywords];
				typedText = scenario.prompt;
				visibleDrafts = scenario.draftCount;
				pickDraftId = scenario.pickDraftId;
				focusDraftId = scenario.pickDraftId;
				actionsVisible = true;
				phase = 'save-ready';
				await wait(6000, signal);
				return;
			}

			await wait(450, signal);

			for (const kw of scenario.keywords) {
				if (signal.cancelled) return;
				litKeywords = [...litKeywords, kw];
				await wait(280, signal);
			}

			phase = 'typing';
			await wait(250, signal);
			for (let i = 0; i <= scenario.prompt.length; i++) {
				if (signal.cancelled) return;
				typedText = scenario.prompt.slice(0, i);
				await wait(28, signal);
			}

			phase = 'generating';
			await wait(1000, signal);

			phase = 'revealing';
			for (let n = 1; n <= scenario.draftCount; n++) {
				if (signal.cancelled) return;
				visibleDrafts = n;
				await wait(200, signal);
			}

			await wait(500, signal);

			phase = 'picking';
			pickDraftId = scenario.pickDraftId;
			await wait(900, signal);

			focusDraftId = scenario.pickDraftId;
			phase = 'focus-loading';
			await wait(1800, signal);

			phase = 'save-ready';
			actionsVisible = true;
			await wait(3800, signal);

			savePressed = true;
			await wait(400, signal);
			phase = 'saving';
			actionsVisible = false;
			await wait(350, signal);

			focusDraftId = null;
			pickDraftId = null;
			visibleDrafts = 0;
			savePressed = false;
			await wait(650, signal);
		}

		async function runLoop() {
			let index = 0;
			while (!signal.cancelled) {
				scenarioIndex = index % demoScenarios.length;
				await runScenario(demoScenarios[scenarioIndex]);
				if (signal.cancelled) return;
				index += 1;
			}
		}

		runLoop();

		return () => {
			signal.cancelled = true;
			for (const id of signal.timeouts) clearTimeout(id);
		};
	});
</script>

<section id="prompt-studio" class="studio landing-section" aria-labelledby="studio-heading">
	<div class="studio__inner landing-section__inner">
		<header class="studio__intro">
			<span class="studio__label eyebrow">Prompt studio</span>
			<h2 id="studio-heading">Generate your best dating photos</h2>
			<p class="studio__lede">
				Choose a vibe or use the presets. Visagely instantly generates high-quality dating-ready photos
				of you, all fully consistent with your personal model. Get perfect images of yourself across
				different styles, angles, and moods, then pick the ones that make you look your best.
			</p>
			<a class="studio__cta btn btn-primary" href="#notify">Join waitlist to try it first</a>
		</header>

		<div class="studio__demo panel-glass" aria-hidden="true">
			<div class="studio__demo-bar">
				<span class="studio__demo-title">Generate your pictures</span>
			</div>
			<div class="studio__demo-batch" aria-label="How many drafts to generate">
				<span class="studio__demo-batch-label">How many drafts?</span>
				<div class="studio__demo-counts" role="group" aria-label="Picture count">
					{#each draftCountOptions as option (option.count)}
						<span
							class="studio__demo-count"
							class:studio__demo-count--active={draftCount === option.count}
						>
							{option.label}
						</span>
					{/each}
				</div>
			</div>

			<div class="studio__demo-chips">
				{#each premadeKeywords as keyword}
					<span
						class="studio__chip"
						class:studio__chip--lit={litKeywords.includes(keyword)}
					>
						{keyword}
					</span>
				{/each}
			</div>

			<div
				class="studio__demo-input"
				class:studio__demo-input--typing={phase === 'typing'}
			>
				<span class="studio__demo-input-text">
					{typedText}<span class="studio__caret" class:studio__caret--on={phase === 'typing'}></span>
				</span>
			</div>

			<div
				class="studio__demo-step"
				class:studio__demo-step--running={phase !== 'keywords' && phase !== 'typing'}
				aria-hidden="true"
			>
				<span
					class="studio__demo-step-dot"
					class:studio__demo-step-dot--pulse={phase === 'generating' || phase === 'focus-loading'}
				></span>
				{#if phase === 'generating' || phase === 'focus-loading'}
					<span class="studio__demo-spinner"></span>
				{/if}
				<span class="studio__demo-step-text">{stepLabel(phase, draftCount)}</span>
			</div>

			<div
				class="studio__demo-stage"
				class:studio__demo-stage--picked={deckPicked}
				class:studio__demo-stage--out={phase === 'saving'}
			>
				<div
					class="studio__demo-grid studio__demo-grid--count-{draftCount}"
					class:studio__demo-grid--loading={phase === 'generating'}
					class:studio__demo-grid--deck={deckPicked}
				>
					{#each activeDrafts as draft (draft.id)}
						<div
							class="studio__demo-tile"
							class:studio__demo-tile--visible={draft.id <= visibleDrafts}
							class:studio__demo-tile--pick={pickDraftId === draft.id && phase === 'picking'}
							class:studio__demo-tile--back={deckPicked && focusDraftId !== draft.id}
							class:studio__demo-tile--ghost={focusDraftId === draft.id}
							style={draftStyle(draft, pickDraftId === draft.id || focusDraftId === draft.id)}
						>
							<span>{draft.scene}</span>
							{#if pickDraftId === draft.id && phase === 'picking'}
								<span class="studio__demo-tile-cursor" aria-hidden="true"></span>
							{/if}
						</div>
					{/each}
				</div>

				{#if focusDraft}
					<div class="studio__demo-float" class:studio__demo-float--out={phase === 'saving'}>
						<div
							class="studio__demo-float-card"
							class:studio__demo-float-card--loading={phase === 'focus-loading'}
							class:studio__demo-float-card--ready={phase === 'save-ready' || phase === 'saving'}
							style={draftStyle(focusDraft, true)}
						>
							{#if phase === 'focus-loading'}
								<div class="studio__demo-float-overlay">
									<span class="studio__demo-float-spinner"></span>
								</div>
							{/if}
							<span class="studio__demo-float-label">{focusDraft.scene}</span>
						</div>

						{#if actionsVisible}
							<div class="studio__demo-actions">
								<span class="studio__demo-action">Put back</span>
								<span class="studio__demo-action">Favorite</span>
								<span class="studio__demo-action studio__demo-action--danger">Delete</span>
								<span
									class="studio__demo-action studio__demo-action--primary btn btn-primary"
									class:studio__demo-action--pressed={savePressed}
								>
									Save to library
								</span>
							</div>
						{/if}
					</div>
				{/if}
			</div>
		</div>
	</div>

	<p class="studio__sr-only">
		Animated preview: select keywords, choose draft count, generate pictures, pick one from the
		deck, upscale it, then save to library or start the next prompt.
	</p>
</section>

<style>
	.studio__inner {
		display: grid;
		grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr);
		gap: 3rem 3.5rem;
		align-items: center;
	}

	.studio__label {
		display: block;
		margin-bottom: 0.35rem;
	}

	.studio__intro {
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
	}

	.studio__intro h2 {
		font-family: var(--font-display);
		font-size: clamp(2rem, 2.8vw, 2.75rem);
		font-weight: 500;
		letter-spacing: 0.01em;
		margin: 0;
		line-height: 1.08;
	}

	.studio__lede {
		margin: 0;
		font-size: 0.9875rem;
		line-height: 1.65;
		color: var(--color-text-muted);
		max-width: 28rem;
	}

	.studio__lede strong {
		color: var(--color-text);
		font-weight: 600;
	}

	.studio__cta.btn-primary {
		margin-top: 0.5rem;
	}

	.studio__demo {
		padding: 1.125rem;
		min-width: 0;
		container-type: inline-size;
	}

	.studio__demo-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 0.75rem;
		padding-bottom: 0.625rem;
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.studio__demo-title {
		font-family: var(--font-display);
		font-size: 0.875rem;
		font-weight: 600;
	}

	.studio__demo-batch {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem 0.75rem;
		margin-bottom: 0.625rem;
		padding: 0.5rem 0.625rem;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border-subtle);
		background: color-mix(in srgb, var(--color-surface) 80%, transparent);
	}

	.studio__demo-batch-label {
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--color-text-muted);
	}

	.studio__demo-counts {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.3rem;
	}

	.studio__demo-count {
		padding: 0.3rem 0.6rem;
		font-size: 0.6875rem;
		font-weight: 600;
		white-space: nowrap;
		color: var(--color-text-subtle);
		border-radius: var(--radius-pill);
		border: 1px solid var(--color-border);
		background: var(--color-surface);
		transition:
			border-color 0.2s ease,
			color 0.2s ease,
			background 0.2s ease;
	}

	.studio__demo-count--active {
		color: var(--color-accent-bright);
		border-color: color-mix(in srgb, var(--color-accent) 45%, transparent);
		background: var(--color-accent-soft);
	}

	.studio__demo-chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.3rem;
		margin-bottom: 0.625rem;
	}

	.studio__chip {
		font-size: 0.625rem;
		font-weight: 500;
		padding: 0.2rem 0.5rem;
		border-radius: var(--radius-pill);
		border: 1px solid var(--color-border);
		color: var(--color-text-subtle);
		background: var(--color-surface);
		transition:
			border-color 0.2s ease,
			color 0.2s ease,
			background 0.2s ease;
	}

	.studio__chip--lit {
		border-color: color-mix(in srgb, var(--color-accent) 45%, transparent);
		background: var(--color-accent-soft);
		color: var(--color-accent-bright);
	}

	.studio__demo-input {
		min-height: 2.5rem;
		padding: 0.5rem 0.625rem;
		margin-bottom: 0.625rem;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border-subtle);
		background: var(--color-surface);
	}

	.studio__demo-input--typing {
		border-color: color-mix(in srgb, var(--color-accent) 30%, var(--color-border));
	}

	.studio__demo-input-text {
		font-size: 0.75rem;
		line-height: 1.45;
		color: var(--color-text-muted);
	}

	.studio__caret {
		display: inline-block;
		width: 1px;
		height: 0.85em;
		margin-left: 1px;
		vertical-align: text-bottom;
		background: transparent;
	}

	.studio__caret--on {
		background: var(--color-accent-bright);
		animation: studio-caret 0.9s step-end infinite;
	}

	@keyframes studio-caret {
		50% {
			opacity: 0;
		}
	}

	.studio__demo-step {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
		padding: 0.5rem 0.75rem;
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border-subtle);
		border-left: 3px solid var(--color-border);
		background: color-mix(in srgb, var(--color-surface-alt) 90%, transparent);
		cursor: default;
		pointer-events: none;
		user-select: none;
	}

	.studio__demo-step--running {
		border-left-color: var(--color-accent);
		background: color-mix(in srgb, var(--color-accent-soft) 55%, var(--color-surface-alt));
	}

	.studio__demo-step-dot {
		width: 0.4rem;
		height: 0.4rem;
		border-radius: 50%;
		background: var(--color-text-subtle);
		flex-shrink: 0;
	}

	.studio__demo-step--running .studio__demo-step-dot {
		background: var(--color-accent-bright);
	}

	.studio__demo-step-dot--pulse {
		animation: studio-dot-pulse 1s ease-in-out infinite;
	}

	.studio__demo-step-text {
		font-family: var(--font-mono);
		font-size: 0.625rem;
		font-weight: 500;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--color-text-subtle);
	}

	.studio__demo-step--running .studio__demo-step-text {
		color: var(--color-accent-bright);
	}

	.studio__demo-spinner {
		width: 0.75rem;
		height: 0.75rem;
		border: 1.5px solid color-mix(in srgb, var(--color-accent) 35%, transparent);
		border-top-color: var(--color-accent-bright);
		border-radius: 50%;
		animation: studio-spin 0.65s linear infinite;
		flex-shrink: 0;
	}

	@keyframes studio-dot-pulse {
		0%,
		100% {
			opacity: 0.5;
			transform: scale(1);
		}
		50% {
			opacity: 1;
			transform: scale(1.2);
		}
	}

	@keyframes studio-spin {
		to {
			transform: rotate(360deg);
		}
	}

	.studio__demo-stage {
		position: relative;
		--studio-cols: 4;
		--studio-rows: 2;
		--studio-gap: 0.4rem;
		--studio-pad: 0.625rem;
		--studio-safe: 1.25rem;
		box-sizing: border-box;
		padding: var(--studio-pad);
		height: max(
			24rem,
			calc(
				((100cqi - (var(--studio-cols) - 1) * var(--studio-gap)) / var(--studio-cols)) * (4 / 3) *
					var(--studio-rows) + (var(--studio-rows) - 1) * var(--studio-gap) + var(--studio-safe) +
					var(--studio-pad) * 2
			)
		);
		overflow: visible;
	}

	.studio__demo-stage--picked::after {
		content: '';
		position: absolute;
		inset: -0.25rem;
		border-radius: var(--radius-lg);
		background: radial-gradient(
			ellipse 55% 70% at 50% 42%,
			transparent 0%,
			color-mix(in srgb, var(--color-bg) 55%, transparent) 100%
		);
		pointer-events: none;
		z-index: 1;
	}

	.studio__demo-stage--out .studio__demo-grid,
	.studio__demo-stage--out .studio__demo-float {
		opacity: 0;
		transform: scale(0.98);
	}

	.studio__demo-grid {
		position: relative;
		z-index: 0;
		display: grid;
		gap: 0.4rem;
		padding: 0.25rem;
		transition:
			opacity 0.4s ease,
			transform 0.4s ease,
			filter 0.4s ease;
	}

	.studio__demo-grid--count-1 {
		grid-template-columns: 1fr;
		max-width: 4.5rem;
		margin-inline: auto;
	}

	.studio__demo-grid--count-2 {
		grid-template-columns: repeat(2, 1fr);
		max-width: 9rem;
		margin-inline: auto;
	}

	.studio__demo-grid--count-4 {
		grid-template-columns: repeat(2, 1fr);
		max-width: 12rem;
		margin-inline: auto;
	}

	.studio__demo-grid--count-8 {
		grid-template-columns: repeat(4, 1fr);
	}

	.studio__demo-grid--loading {
		opacity: 0.45;
	}

	.studio__demo-grid--deck {
		filter: saturate(0.75);
	}

	.studio__demo-tile {
		position: relative;
		aspect-ratio: 3 / 4;
		border-radius: 0.375rem;
		border: 1px solid var(--color-border-subtle);
		opacity: 0;
		transform: scale(0.92) translateY(4px);
		transition:
			opacity 0.35s ease,
			transform 0.45s cubic-bezier(0.33, 1, 0.68, 1),
			box-shadow 0.25s ease,
			filter 0.35s ease;
		display: flex;
		align-items: flex-end;
		padding: 0.3rem;
	}

	.studio__demo-tile--visible {
		opacity: 1;
		transform: scale(1) translateY(0);
	}

	.studio__demo-tile--pick {
		transform: scale(1.05);
		z-index: 2;
		box-shadow: 0 6px 20px -8px color-mix(in srgb, #000 45%, transparent);
	}

	.studio__demo-tile--back {
		opacity: 0.38;
		transform: scale(0.92) translateY(2px);
		filter: blur(0.4px);
	}

	.studio__demo-tile--ghost {
		opacity: 0;
		transform: scale(1);
		pointer-events: none;
	}

	.studio__demo-tile span {
		font-family: var(--font-mono);
		font-size: 0.5rem;
		letter-spacing: 0.04em;
		color: color-mix(in srgb, var(--color-text) 75%, transparent);
		line-height: 1.2;
	}

	.studio__demo-tile-cursor {
		position: absolute;
		top: 28%;
		right: 18%;
		width: 0.65rem;
		height: 0.65rem;
		border-radius: 50%;
		background: var(--color-accent-bright);
		box-shadow: 0 0 0 4px color-mix(in srgb, var(--color-accent) 35%, transparent);
		animation: studio-cursor-tap 0.55s ease 0.35s 2;
	}

	@keyframes studio-cursor-tap {
		0%,
		100% {
			transform: scale(1);
		}
		50% {
			transform: scale(0.82);
		}
	}

	.studio__demo-float {
		position: absolute;
		z-index: 3;
		left: 50%;
		top: 42%;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
		width: min(100%, 14rem);
		transform: translate(-50%, -50%);
		pointer-events: none;
		transition:
			opacity 0.35s ease,
			transform 0.35s ease;
	}

	.studio__demo-float--out {
		opacity: 0;
		transform: translate(-50%, -48%) scale(0.94);
	}

	.studio__demo-float-card {
		position: relative;
		width: 7.5rem;
		aspect-ratio: 3 / 4;
		border-radius: 0.625rem;
		border: 1px solid color-mix(in srgb, var(--color-accent) 40%, var(--color-border));
		display: flex;
		align-items: flex-end;
		padding: 0.55rem;
		box-shadow:
			0 0 0 1px color-mix(in srgb, var(--color-accent) 18%, transparent),
			0 24px 56px -18px color-mix(in srgb, #000 50%, transparent),
			0 0 40px -8px var(--color-accent-glow);
		transform: scale(0.72) translateY(10px);
		opacity: 0;
		animation: studio-card-lift 0.55s cubic-bezier(0.33, 1, 0.68, 1) forwards;
		transition:
			width 0.55s cubic-bezier(0.33, 1, 0.68, 1),
			transform 0.55s cubic-bezier(0.33, 1, 0.68, 1),
			box-shadow 0.35s ease;
	}

	.studio__demo-float-card--loading {
		width: 9.5rem;
		transform: scale(1.04);
	}

	.studio__demo-float-card--ready {
		width: 11rem;
		transform: scale(1.08);
		box-shadow:
			0 0 0 1px color-mix(in srgb, var(--color-accent-bright) 35%, transparent),
			0 32px 64px -20px color-mix(in srgb, #000 58%, transparent),
			0 0 48px -6px var(--color-accent-glow);
	}

	@keyframes studio-card-lift {
		from {
			opacity: 0;
			transform: scale(0.72) translateY(14px);
		}
		to {
			opacity: 1;
			transform: scale(1) translateY(0);
		}
	}

	.studio__demo-float-overlay {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: inherit;
		background: color-mix(in srgb, var(--color-bg) 50%, transparent);
		backdrop-filter: blur(2px);
	}

	.studio__demo-float-spinner {
		width: 1.75rem;
		height: 1.75rem;
		border: 2px solid color-mix(in srgb, var(--color-accent) 30%, transparent);
		border-top-color: var(--color-accent-bright);
		border-radius: 50%;
		animation: studio-spin 0.7s linear infinite;
	}

	.studio__demo-float-label {
		position: relative;
		z-index: 1;
		font-family: var(--font-mono);
		font-size: 0.5625rem;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: color-mix(in srgb, var(--color-text) 85%, transparent);
	}

	.studio__demo-actions {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 0.35rem;
		animation: studio-save-in 0.35s ease;
	}

	.studio__demo-action {
		padding: 0.35rem 0.65rem;
		font-size: 0.625rem;
		font-weight: 600;
		font-family: inherit;
		line-height: 1.2;
		white-space: nowrap;
		color: var(--color-text-muted);
		background: color-mix(in srgb, var(--color-surface-elevated) 90%, transparent);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-pill);
	}

	.studio__demo-action--danger {
		color: #f87171;
		border-color: color-mix(in srgb, #f87171 35%, var(--color-border));
	}

	.studio__demo-action--primary {
		min-height: 2rem;
		padding: 0.4rem 0.85rem;
		font-size: 0.6875rem;
	}

	.studio__demo-action--pressed {
		transform: translateY(1px);
		filter: brightness(0.97);
	}

	@keyframes studio-save-in {
		from {
			opacity: 0;
			transform: translateY(6px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.studio__sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}

	@media (max-width: 960px) {
		.studio__inner {
			grid-template-columns: 1fr;
			gap: var(--space-block-lg);
		}

		.studio__demo-grid {
			grid-template-columns: repeat(4, 1fr);
		}

		.studio__demo-float-card--ready {
			width: 9.5rem;
		}
	}

	@container (max-width: 400px) {
		.studio__demo-stage {
			--studio-cols: 2;
			--studio-rows: 4;
			--studio-safe: 1.5rem;
		}

		.studio__demo-grid--count-8 {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media (max-width: 480px) {
		.studio__demo-chips {
			max-height: none;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.studio__demo-tile,
		.studio__demo-float,
		.studio__demo-float-card,
		.studio__chip,
		.studio__caret--on,
		.studio__demo-actions,
		.studio__demo-grid {
			transition: none;
			animation: none;
		}

		.studio__demo-float-card {
			opacity: 1;
			transform: scale(1);
		}

		.studio__demo-tile-cursor {
			display: none;
		}
	}
</style>
