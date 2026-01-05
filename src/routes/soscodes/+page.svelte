<script>
    import LabeledInput from "$lib/components/form/LabeledInput.svelte";
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";
    import CodesBlock from "$lib/components/soscodes/codes.svelte";
</script>

<!-- SOSCodes toevoegen -->
<div class="flex flex-row gap-4 px-4 py-4">
    <LabeledInput
        id="Nieuwe SOScode"
        label="Nieuwe SOScode"
        placeholder="..."
        tooltipText="Type hier uw nieuwe SOScode"
        showTooltip={true}
    />

    <LabeledInput
        id="Omschrijving"
        label="Omschrijving"
        placeholder="..."
        tooltipText=""
        showTooltip={false}
    />
</div>
<!-- Verwerken -->
<div class="flex flex-col items-start px-4">
    <SimpleButton
        text="Verwerk nieuwe SOScode"
        bgColor="#0C3966"
        textColor="#FFF"
    />
</div>
<!-- SOScodes lijst -->
<div class="flex flex-col h-[600px] w-full gap-3">
    <CodesBlock></CodesBlock>
</div>
