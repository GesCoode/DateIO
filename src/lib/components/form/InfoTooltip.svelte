<script lang="ts">
    export let infoText: string = "Information goes here";
    export let color: string = "#0C3966"; // default icon color
</script>

<div class="relative inline-block">
    <div
        class="w-4 h-4 rounded-full border flex items-center justify-center cursor-pointer text-xs"
        style="border-color: {color}; color: {color};"
    >
        i
    </div>

    <!-- Tooltip overlay -->
    <div
        class="absolute top-1/2 left-full transform -translate-y-1/2 ml-2 w-48 p-2 bg-gray-800 text-white text-sm rounded shadow-lg opacity-0 pointer-events-none transition-opacity duration-200 z-50"
    >
        {infoText}
    </div>
</div>

<style>
    div.relative:hover div.absolute {
        opacity: 1;
        pointer-events: auto;
    }
</style>
