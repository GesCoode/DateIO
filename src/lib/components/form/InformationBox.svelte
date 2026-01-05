<script lang="ts">
    export let outlineColor: string = "#B87373";
    export let fillColor: string = "#ECD1D1";
    export let textColor: string = "#3F3F3F";
</script>

<div
    class="border rounded px-4 py-2 text-sm"
    style="
        border-color: {outlineColor};
        background-color: {fillColor};
        color: {textColor};
    "
>
    <slot />
</div>
