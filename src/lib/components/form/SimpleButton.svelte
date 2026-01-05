<script lang="ts">
    export let text: string = "Button";
    export let onClick: () => void = () => {};

    export let bgColor: string = "#0C3966";
    export let textColor: string = "#FFFFFF";

    export let rounded: boolean = false;

    let overlayOpacity = 0;
    const hoverOpacity = 0.2;
    const activeOpacity = 0.5;
</script>

<button
    class="relative flex justify-center items-center gap-2 flex-1 px-5 py-[7px] font-sans font-semibold text-[14px] leading-normal tracking-[-0.266px] overflow-hidden transition-colors duration-150
        {rounded ? 'rounded' : 'rounded-[2px]'}"
    style="background: {bgColor}; color: {textColor};"
    on:click={onClick}
    on:mouseenter={() => (overlayOpacity = hoverOpacity)}
    on:mouseleave={() => (overlayOpacity = 0)}
    on:mousedown={() => (overlayOpacity = activeOpacity)}
    on:mouseup={() => (overlayOpacity = hoverOpacity)}
>
    {text}

    <div
        class="absolute inset-0 bg-black pointer-events-none transition-opacity duration-150"
        style="opacity: {overlayOpacity}"
    ></div>
</button>
