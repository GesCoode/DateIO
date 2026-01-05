<script lang="ts">
    let open = false;

    export let label: string = "Selecteer";
    export let items: { label: string; onClick: () => void }[] = [];

    // Colors
    export let buttonBg: string = "#0C3966";
    export let buttonText: string = "#FFFFFF";
    export let dropdownBg: string = "#FFFFFF";
    export let dropdownBorder: string = "#D1D5DB";

    // Selected label
    let selectedLabel: string = label;

    function toggle() {
        open = !open;
    }

    function handleItemClick(item: { label: string; onClick: () => void }) {
        selectedLabel = item.label;
        item.onClick();
        open = false;
    }

    // Close dropdown on outside click
    let dropdownRef: HTMLElement;
    import { onMount } from "svelte";

    onMount(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (!dropdownRef.contains(e.target as Node)) open = false;
        };
        document.addEventListener("click", handleClickOutside);
        return () => document.removeEventListener("click", handleClickOutside);
    });
</script>

<div class="relative inline-block" bind:this={dropdownRef}>
    <!-- Button -->
    <button
        class="flex items-center px-2 rounded font-medium text-sm focus:outline-none focus:ring-2 focus:ring-offset-1"
        on:click={toggle}
        aria-haspopup="true"
        aria-expanded={open}
        style="background-color: {buttonBg}; color: {buttonText};"
    >
        {selectedLabel}
        <span class="text-xl">▾</span>
    </button>

    <!-- Dropdown -->
    {#if open}
        <div
            class="absolute right-0 w-48 rounded shadow-lg z-50 border"
            style="background-color: {dropdownBg}; border-color: {dropdownBorder};"
        >
            {#each items as item}
                <button
                    class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 focus:bg-gray-200 focus:outline-none"
                    on:click={() => handleItemClick(item)}
                    style="background-color: {dropdownBg};"
                >
                    {item.label}
                </button>
            {/each}
        </div>
    {/if}
</div>
