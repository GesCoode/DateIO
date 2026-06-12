<script lang="ts">
	import DashboardHeader from '$lib/components/dashboard/DashboardHeader.svelte';
	import DashboardSidebar from '$lib/components/dashboard/DashboardSidebar.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<title>Dashboard · Visagely</title>
</svelte:head>

<div class="dashboard-shell">
	<div class="dashboard-shell__backdrop" aria-hidden="true">
		<div class="dashboard-shell__mesh"></div>
	</div>

	<div class="dashboard-body">
		<DashboardSidebar />

		<div class="dashboard-body__main">
			<DashboardHeader />

			<main class="dashboard-main">
				{@render children()}
			</main>
		</div>
	</div>
</div>

<style>
	.dashboard-shell {
		--dash-sidebar-width: 15.5rem;

		position: relative;
		isolation: isolate;
		min-height: 100dvh;
		color: var(--color-text);
		font-family: var(--font-body);
		background: var(--color-bg);
	}

	.dashboard-body {
		display: flex;
		min-height: 100dvh;
	}

	.dashboard-body__main {
		flex: 1;
		display: flex;
		flex-direction: column;
		min-width: 0;
		position: relative;
		z-index: 1;
	}

	.dashboard-shell__backdrop {
		pointer-events: none;
		position: fixed;
		inset: 0;
		z-index: -1;
	}

	.dashboard-shell__mesh {
		position: absolute;
		inset: 0;
		background:
			radial-gradient(ellipse 50% 40% at 8% 12%, var(--color-bg-mesh-a) 0%, transparent 55%),
			radial-gradient(ellipse 45% 35% at 92% 80%, var(--color-bg-mesh-b) 0%, transparent 50%),
			var(--color-bg);
	}

	.dashboard-main {
		flex: 1;
		width: 100%;
		max-width: 120rem;
		margin-inline: auto;
		padding: 0 2.5rem 2.5rem;
	}

	@media (max-width: 768px) {
		.dashboard-shell {
			--dash-sidebar-width: 0px;
		}

		.dashboard-main {
			padding: 0 1.25rem 2rem;
		}
	}
</style>
