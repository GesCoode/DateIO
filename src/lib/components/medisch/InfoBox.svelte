<script lang="ts">
    import ArrowDown from "$lib/assets/ArrowDown.svg";
    import { slide } from "svelte/transition";

    export let icon: string;
    export let header: string;
    export let subheader: string;
    export let isOpen: boolean = false; // toggle arrow / expansion

    let overlayOpacity = 0;
    const hoverOpacity = 0.2;
    const activeOpacity = 0.4;

    function handleClick() {
        isOpen = !isOpen; // toggle open state
    }
</script>

<div class="flex flex-col w-full">
    <!-- Main clickable header -->
    <button
        type="button"
        class="relative flex w-full items-center gap-4 pt-4 px-4 pb-4 rounded-t-[4px] border border-b-0 flex-1 overflow-hidden cursor-pointer text-left"
        style="border: 1px solid #B87373; background: #FFF;"
        on:mouseenter={() => (overlayOpacity = hoverOpacity)}
        on:mouseleave={() => (overlayOpacity = 0)}
        on:mousedown={() => (overlayOpacity = activeOpacity)}
        on:mouseup={() => (overlayOpacity = hoverOpacity)}
        on:click={handleClick}
    >
        <!-- Overlay -->
        <div
            class="absolute inset-0 bg-black pointer-events-none transition-opacity duration-150"
            style="opacity: {overlayOpacity};"
        ></div>

        <!-- Icon -->
        <img src={icon} alt="Icon" class="h-10 w-10 relative z-10" />

        <!-- Header -->
        <div
            class="flex flex-col justify-center items-start gap-2 flex-1 relative z-10"
        >
            <h1
                class="text-black font-semibold text-[14px]"
                style="font-family: Arial, sans-serif;"
            >
                {header}
            </h1>
            <h2
                class="text-[#8F8F8F] font-medium text-[12px]"
                style="font-family: Arial, sans-serif;"
            >
                {subheader}
            </h2>
        </div>

        <!-- Arrow -->
        <div
            class="flex w-[12px] h-[40px] flex-col justify-end items-end relative z-10"
        >
            <img
                src={ArrowDown}
                alt="Arrow"
                class="h-[11px] w-[12px] transition-transform duration-200"
                style="transform: rotate({isOpen ? 180 : 0}deg);"
            />
        </div>
    </button>

    <!-- Expandable content slot -->
    {#if isOpen}
        <div
            class="flex flex-col w-full overflow-hidden rounded-b-[4px] border border-t-0 border-[#B87373]"
            transition:slide={{ duration: 200 }}
        >
            <slot />
        </div>
    {/if}
</div>
