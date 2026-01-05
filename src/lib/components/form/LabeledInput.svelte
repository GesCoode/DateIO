<script lang="ts">
    import InfoTooltip from "$lib/components/form/InfoTooltip.svelte";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    // Props
    export let label: string;
    export let value: string = "";
    export let placeholder: string = "";
    export let type: string = "text";
    export let id: string;

    // Delete support
    export let deletable: boolean = false;

    // Tooltip
    export let tooltipText: string = "";
    export let showTooltip: boolean = true;
</script>

<div class="space-y-1">
    <!-- Label row -->
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-1">
            <label for={id} class="block text-sm font-medium text-gray-700">
                {label}
            </label>

            {#if showTooltip && tooltipText}
                <InfoTooltip infoText={tooltipText} color="#4B5563" />
            {/if}
        </div>

        {#if deletable}
            <button
                type="button"
                class="shrink-0 text-gray-400 hover:text-red-600 transition text-sm"
                aria-label="Verwijderen"
                on:click={() => dispatch("delete")}
            >
                ✕
            </button>
        {/if}
    </div>

    <!-- Input field -->
    <input
        {id}
        {type}
        bind:value
        {placeholder}
        class="block w-full rounded-md border border-gray-300 px-3 py-2
               shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
    />
</div>
