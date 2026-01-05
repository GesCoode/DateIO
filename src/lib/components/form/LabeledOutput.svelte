<script lang="ts">
    export let label: string = "";
    export let value: string = "";
    export let showRemove: boolean = false;
    export let onRemove: () => void = () => {};

    let id = `output-${Math.random().toString(36).substr(2, 9)}`;
</script>

<div class="flex flex-col gap-1 w-full">
    {#if label}
        <!-- Label + cross -->
        <div class="flex justify-between items-center">
            <span {id} class="text-sm font-medium text-white">{label}</span>

            {#if showRemove}
                <button
                    class="text-white font-bold px-2 py-1 rounded hover:bg-white/20"
                    on:click={onRemove}
                    aria-label="Verwijder"
                >
                    ✕
                </button>
            {/if}
        </div>
    {/if}

    <!-- Read-only value -->
    <div
        class="px-3 py-2 rounded border border-gray-300 select-none"
        role="textbox"
        aria-labelledby={id}
        style="background: rgba(0, 0, 0, 0.45); color: #D1D5DB;"
    >
        {value || "..."}
    </div>
</div>
