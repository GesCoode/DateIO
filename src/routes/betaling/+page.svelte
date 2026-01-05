<script lang="ts">
    import accountImage from "$lib/assets/TempImage1.png";
    import LeftBetalingBlock from "$lib/components/betaling/LeftBetalingBlock.svelte";
    import RightBetalingBlock from "$lib/components/betaling/RightBetalingBlock.svelte";
</script>

<div class="w-full px-5 flex flex-col items-start">
    <div class="flex flex-col xl:flex-row gap-3 self-stretch">
        <!-- Left block -->
        <div class="h-[600px] w-full xl:flex-1 flex flex-col gap-3">
            <LeftBetalingBlock></LeftBetalingBlock>
        </div>

        <!-- Right block -->
        <div class="flex flex-col h-[600px] w-full xl:flex-1 gap-3">
            <RightBetalingBlock></RightBetalingBlock>
        </div>

        <!-- Image -->
        <img
            src={accountImage}
            alt="Gezellige eettafel"
            class="hidden xl:block h-[600px] w-[360px] object-cover flex-shrink-0"
        />
    </div>
</div>
