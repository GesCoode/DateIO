<script lang="ts">
    import InfoTooltip from "$lib/components/form/InfoTooltip.svelte";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    // Props
    export let label: string;
    export let value: string = "";
    export let placeholder: string = "";
    export let id: string;

    // Delete support
    export let deletable: boolean = false;

    // Tooltip
    export let tooltipText: string = "";
    export let showTooltip: boolean = true;

    // Height control
    export let minHeight: number = 80;
    export let initialHeight: number = 120;
    export let maxHeight: number = 500;

    let textareaHeight = initialHeight;

    // Drag state
    let isResizing = false;
    let startY: number;
    let startHeight: number;

    function startResize(event: MouseEvent) {
        isResizing = true;
        startY = event.clientY;
        startHeight = textareaHeight;
        event.preventDefault();

        window.addEventListener("mousemove", resize);
        window.addEventListener("mouseup", stopResize);
    }

    function resize(event: MouseEvent) {
        if (!isResizing) return;
        const dy = event.clientY - startY;
        textareaHeight = Math.min(
            maxHeight,
            Math.max(minHeight, startHeight + dy),
        );
    }

    function stopResize() {
        isResizing = false;
        window.removeEventListener("mousemove", resize);
        window.removeEventListener("mouseup", stopResize);
    }

    function handleKeyResize(event: KeyboardEvent) {
        if (event.key === "ArrowUp") {
            textareaHeight = Math.max(minHeight, textareaHeight - 5);
            event.preventDefault();
        }
        if (event.key === "ArrowDown") {
            textareaHeight = Math.min(maxHeight, textareaHeight + 5);
            event.preventDefault();
        }
    }
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
                class="text-gray-400 hover:text-red-600 transition text-sm"
                aria-label="Verwijderen"
                on:click={() => dispatch("delete")}
            >
                ✕
            </button>
        {/if}
    </div>

    <!-- Textarea container -->
    <div class="relative w-full">
        <textarea
            {id}
            bind:value
            {placeholder}
            class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm resize-none focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            style="height: {textareaHeight}px;"
        ></textarea>

        <!-- Resize handle -->
        <button
            type="button"
            class="absolute bottom-0 left-1/2 -translate-x-1/2 w-6 h-2 bg-gray-400 rounded-sm cursor-row-resize p-0 border-none"
            aria-label="Resize textarea"
            on:mousedown={startResize}
            on:keydown={handleKeyResize}
        ></button>
    </div>
</div>
