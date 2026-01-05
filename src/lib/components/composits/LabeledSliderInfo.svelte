<script lang="ts">
    import SliderButton from "$lib/components/form/SliderButton.svelte";
    import InfoTooltip from "$lib/components/form/InfoTooltip.svelte";

    // Props
    export let label: string = "Receive newsletter";
    export let tooltipText: string =
        "If enabled, you will receive our newsletter via email.";
    export let statusTextTrue: string = "You currently receive the newsletter";
    export let statusTextFalse: string =
        "You currently do NOT receive the newsletter";

    export let checked: boolean = false;
    export let onChange: (value: boolean) => void = () => {};

    // Optional colors
    export let handleColor: string = "#FFF";
    export let trueColor: string = "#0C3966";
    export let statusTextColor: string = "#4B5563"; // default gray-600

    // NEW PROP: whether to show the tooltip
    export let showTooltip: boolean = true;

    function handleToggle(value: boolean) {
        checked = value;
        onChange(value);
    }
</script>

<div class="flex flex-col items-start self-stretch">
    <!-- Top row: label + optional info tooltip -->
    <div class="flex items-start gap-1 self-stretch">
        <span class="text-sm font-medium" style="color: {statusTextColor}">
            {label}
        </span>

        {#if showTooltip}
            <InfoTooltip infoText={tooltipText} color={statusTextColor} />
        {/if}
    </div>

    <!-- Bottom row: slider + status text -->
    <div class="flex items-start gap-2 self-stretch mt-2">
        <div class="flex-shrink-0">
            <SliderButton
                {checked}
                onChange={handleToggle}
                {handleColor}
                {trueColor}
            />
        </div>
        <span class="text-sm" style="color: {statusTextColor}">
            {checked ? statusTextTrue : statusTextFalse}
        </span>
    </div>
</div>
