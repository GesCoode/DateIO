<script lang="ts">
    export let text: string = "Button";
    export let onClick: () => void = () => {};
    export let bgColor: string = "#0C3966";
    export let textColor: string = "#FFFFFF";
    export let activated: boolean = true;

    let overlayOpacity = 0;
    const hoverOpacity = 0.2;
    const activeOpacity = 0.4;
</script>

<button
    class="relative flex justify-center items-center gap-2 flex-1 rounded-[4px] px-5 py-[7px] font-sans font-semibold text-[14px] leading-normal tracking-[-0.266px] overflow-hidden transition-colors duration-150 outline-none
         {activated ? 'pulse' : ''} {activated
        ? 'cursor-pointer'
        : 'cursor-not-allowed'}"
    style="background: {bgColor}; color: {textColor};"
    on:click={activated ? onClick : undefined}
    on:mouseenter={() => activated && (overlayOpacity = hoverOpacity)}
    on:mouseleave={() => activated && (overlayOpacity = 0)}
    on:mousedown={() => activated && (overlayOpacity = activeOpacity)}
    on:mouseup={() => activated && (overlayOpacity = hoverOpacity)}
>
    {text}

    <!-- Black overlay when not activated -->
    {#if !activated}
        <div
            class="absolute inset-0 bg-black pointer-events-none opacity-50"
        ></div>
    {/if}

    <!-- Hover / active overlay -->
    {#if activated}
        <div
            class="absolute inset-0 bg-black pointer-events-none transition-opacity duration-400"
            style="opacity: {overlayOpacity}"
        ></div>
    {/if}
</button>

<style>
    @keyframes pulseOutline {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.5);
        }
        50% {
            box-shadow: 0 0 6px 3px rgba(252, 211, 77, 0.5); /* softer yellow glow */
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.5);
        }
    }

    .pulse {
        animation: pulseOutline 1.5s infinite ease-in-out;
    }
</style>
