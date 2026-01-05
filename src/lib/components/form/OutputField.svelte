<script lang="ts">
    export let value: string = "";
    export let showRemove: boolean = false;
    export let onRemove: () => void = () => {};
</script>

<div class="flex flex-col gap-1 w-full">
    <!-- Cross button -->
    {#if showRemove}
        <div class="flex justify-end mb-1">
            <button
                class="text-white font-bold px-2 py-1 rounded hover:bg-white/20"
                on:click={onRemove}
                aria-label="Verwijder"
            >
                ✕
            </button>
        </div>
    {/if}

    <!-- Read-only value -->
    <div
        class="px-3 py-2 rounded border border-gray-300 select-none"
        role="textbox"
        style="background: rgba(0, 0, 0, 0.45); color: #D1D5DB;"
    >
        {value || "..."}
    </div>
</div>
