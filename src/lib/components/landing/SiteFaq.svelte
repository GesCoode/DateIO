<script lang="ts">
	import { faqItems } from '$lib/data/faq';

	let openId = $state<string | null>(null);

	function toggle(id: string) {
		openId = openId === id ? null : id;
	}
</script>

<section id="faq" class="faq landing-section" aria-labelledby="faq-heading">
	<div class="faq__inner landing-section__inner">
		<span class="faq__eyebrow eyebrow">Support</span>
		<h2 id="faq-heading" class="faq__heading">Questions &amp; answers</h2>

		{#if faqItems.length > 0}
			<div class="faq__list">
				{#each faqItems as item (item.id)}
					<div class="faq__item panel-glass">
						<button
							type="button"
							class="faq__question"
							aria-expanded={openId === item.id}
							aria-controls="faq-answer-{item.id}"
							id="faq-question-{item.id}"
							onclick={() => toggle(item.id)}
						>
							<span>{item.question}</span>
							<span class="faq__icon" aria-hidden="true"></span>
						</button>
						<div
							id="faq-answer-{item.id}"
							class="faq__answer"
							class:faq__answer--open={openId === item.id}
							role="region"
							aria-labelledby="faq-question-{item.id}"
							aria-hidden={openId !== item.id}
						>
							<div class="faq__answer-inner">
								<p>{item.answer}</p>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</section>

<style>
	.faq {
		background: var(--color-bg);
	}

	.faq__inner {
		max-width: 48rem;
		margin-inline: auto;
	}

	.faq__eyebrow {
		display: block;
		margin-bottom: 0.5rem;
	}

	.faq__heading {
		margin: 0;
		font-family: var(--font-display);
		font-size: clamp(2rem, 2.8vw, 2.75rem);
		font-weight: 500;
		letter-spacing: 0.01em;
		line-height: 1.08;
		color: var(--color-text);
	}

	.faq__list {
		margin-top: 1.75rem;
		display: flex;
		flex-direction: column;
		gap: 0.65rem;
	}

	.faq__item {
		overflow: hidden;
		padding: 0;
	}

	.faq__question {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		padding: 1rem 1.25rem;
		font-family: inherit;
		font-size: 0.9375rem;
		font-weight: 600;
		line-height: 1.4;
		text-align: left;
		color: var(--color-text);
		background: transparent;
		border: none;
		cursor: pointer;
		transition: color 0.15s ease;
	}

	.faq__question:hover {
		color: var(--color-champagne-bright);
	}

	.faq__icon {
		position: relative;
		flex-shrink: 0;
		width: 1rem;
		height: 1rem;
	}

	.faq__icon::before,
	.faq__icon::after {
		content: '';
		position: absolute;
		top: 50%;
		left: 50%;
		background: var(--color-text-muted);
		border-radius: 1px;
		transition:
			transform 0.2s ease,
			background 0.15s ease;
	}

	.faq__icon::before {
		width: 0.625rem;
		height: 1.5px;
		transform: translate(-50%, -50%);
	}

	.faq__icon::after {
		width: 1.5px;
		height: 0.625rem;
		transform: translate(-50%, -50%);
	}

	.faq__question[aria-expanded='true'] .faq__icon::after {
		transform: translate(-50%, -50%) scaleY(0);
	}

	.faq__question[aria-expanded='true'] .faq__icon::before,
	.faq__question[aria-expanded='true'] .faq__icon::after {
		background: var(--color-champagne);
	}

	.faq__answer {
		display: grid;
		grid-template-rows: 0fr;
		transition: grid-template-rows 0.35s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.faq__answer--open {
		grid-template-rows: 1fr;
	}

	.faq__answer-inner {
		overflow: hidden;
		min-height: 0;
	}

	.faq__answer-inner p {
		margin: 0;
		padding: 0 1.25rem 1.15rem;
		font-size: 0.9375rem;
		line-height: 1.65;
		color: var(--color-text-muted);
		opacity: 0;
		transition: opacity 0.28s ease;
	}

	.faq__answer--open .faq__answer-inner p {
		opacity: 1;
		transition-delay: 0.06s;
	}

	@media (prefers-reduced-motion: reduce) {
		.faq__answer {
			transition: none;
		}

		.faq__answer-inner p {
			transition: none;
		}

		.faq__answer:not(.faq__answer--open) .faq__answer-inner p {
			visibility: hidden;
		}
	}

	@media (max-width: 640px) {
		.faq__list {
			margin-top: 1.25rem;
		}
	}
</style>
