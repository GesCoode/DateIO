<script lang="ts">
    import { fly, scale } from "svelte/transition";
    import LabeledSliderInfo from "../composits/LabeledSliderInfo.svelte";
    import LabeledInput from "../form/LabeledInput.svelte";
    import SimpleButton from "../form/SimpleButton.svelte";

    export let actieveSOScode: boolean = false;
</script>

<div
    transition:fly={{ y: -200, duration: 300 }}
    class="flex flex-col gap-6 bg-white border border-gray-300 rounded-lg p-4 w-[440px] shadow-lg"
>
    <LabeledInput
        id="SOScode omschrijving"
        label="SOScode omschrijving"
        placeholder="..."
        tooltipText="Type hier een onhandige omschrijving voor uw SOScode."
        showTooltip={true}
    />

    <LabeledSliderInfo
        label="Deactiveer deze SOScode"
        tooltipText="Deactiveer tijdelijk deze SOScode. U kunt deze deactivatie ieder moment weer terugzetten."
        statusTextTrue="Deze code is actief"
        statusTextFalse="Deze code is inactief"
        bind:checked={actieveSOScode}
        handleColor="#FFF"
        trueColor="#45B652"
        statusTextColor="#374151"
    />

    <div class="flex flex-row gap-2">
        <SimpleButton
            text="Opslaan"
            bgColor="#0C3966"
            textColor="#FFF"
            rounded={true}
        />
        <SimpleButton
            text="Annuleren"
            bgColor="#DAA9A9"
            textColor="#0C3966"
            rounded={true}
        />
    </div>
</div>
