<script lang="ts">
    export let checked: boolean = false;
    export let onChange: (value: boolean) => void = () => {};
    export let ariaLabel: string = "Toggle slider";

    // colors
    export let handleColor: string = "#FFFFFF"; // white
    export let trueColor: string = "#0C3966"; // dark blue

    function toggle() {
        checked = !checked;
        onChange(checked);
    }
</script>

<button
    type="button"
    class="w-12 h-6 rounded-full p-1 flex items-center focus:outline-none
         bg-gray-300 transition-colors duration-300 ease-in-out"
    on:click={toggle}
    aria-pressed={checked}
    aria-label={ariaLabel}
    style="background-color: {checked ? trueColor : '#D1D5DB'}"
>
    <div
        class="w-4 h-4 rounded-full shadow-md transform transition-all duration-300 ease-in-out"
        style="background-color: {handleColor}"
        class:translate-x-0={!checked}
        class:translate-x-6={checked}
    ></div>
</button>
