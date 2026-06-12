<script lang="ts">
	import { page } from '$app/stores';

	type NavItem = {
		href: string;
		label: string;
		icon: string;
		disabled?: boolean;
	};

	const nav: NavItem[] = [
		{ href: '/dashboard', label: 'Overview', icon: '◫' },
		{ href: '/dashboard/generate', label: 'Generate', icon: '✦', disabled: true },
		{ href: '/dashboard/photos', label: 'My photos', icon: '▣', disabled: true },
		{ href: '/dashboard/model', label: 'Your LoRA', icon: '◎', disabled: true },
		{ href: '/dashboard/settings', label: 'Settings', icon: '⚙', disabled: true }
	];

	function isActive(href: string, pathname: string) {
		if (href === '/dashboard') return pathname === '/dashboard';
		return pathname.startsWith(href);
	}
</script>

<aside class="dash-sidebar" aria-label="Dashboard navigation">
	<nav class="dash-sidebar__nav" aria-label="Sections">
		<ul>
			{#each nav as item}
				<li>
					{#if item.disabled}
						<span class="dash-sidebar__link dash-sidebar__link--disabled" title="Coming soon">
							<span class="dash-sidebar__icon" aria-hidden="true">{item.icon}</span>
							{item.label}
							<span class="dash-sidebar__soon">Soon</span>
						</span>
					{:else}
						<a
							href={item.href}
							class="dash-sidebar__link"
							class:dash-sidebar__link--active={isActive(item.href, $page.url.pathname)}
							aria-current={isActive(item.href, $page.url.pathname) ? 'page' : undefined}
						>
							<span class="dash-sidebar__icon" aria-hidden="true">{item.icon}</span>
							{item.label}
						</a>
					{/if}
				</li>
			{/each}
		</ul>
	</nav>
</aside>

<style>
	.dash-sidebar {
		position: sticky;
		top: 0;
		align-self: flex-start;
		display: flex;
		flex-direction: column;
		width: var(--dash-sidebar-width, 15.5rem);
		flex-shrink: 0;
		height: 100dvh;
		padding: 5.5rem 1rem 1.5rem 1.25rem;
		border-right: 1px solid var(--color-border-subtle);
		background: color-mix(in srgb, var(--color-surface) 88%, transparent);
		z-index: 2;
	}

	.dash-sidebar__nav ul {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.dash-sidebar__link {
		display: flex;
		align-items: center;
		gap: 0.65rem;
		padding: 0.625rem 0.75rem;
		border-radius: var(--radius-md);
		font-size: 0.9375rem;
		font-weight: 500;
		color: var(--color-text-muted);
		text-decoration: none;
		transition:
			background 0.15s ease,
			color 0.15s ease;
	}

	.dash-sidebar__link:hover {
		color: var(--color-text);
		background: var(--color-accent-soft);
	}

	.dash-sidebar__link--active {
		color: var(--color-text);
		background: var(--color-accent-soft);
		box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--color-accent) 25%, transparent);
	}

	.dash-sidebar__link--disabled {
		cursor: default;
		opacity: 0.55;
	}

	.dash-sidebar__link--disabled:hover {
		background: transparent;
		color: var(--color-text-muted);
	}

	.dash-sidebar__icon {
		width: 1.25rem;
		text-align: center;
		font-size: 0.875rem;
		opacity: 0.85;
	}

	.dash-sidebar__soon {
		margin-left: auto;
		font-family: var(--font-mono);
		font-size: 0.5625rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--color-text-subtle);
	}

	@media (max-width: 768px) {
		.dash-sidebar {
			display: none;
		}
	}
</style>
