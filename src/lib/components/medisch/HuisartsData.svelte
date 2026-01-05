<script lang="ts">
    import LabeledInput from "$lib/components/form/LabeledInput.svelte";
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";

    export let handleOpslaan: () => void = () => {};

    export let praktijkNaam = "";
    export let achterNaam = "";
    export let plaats = "";
    export let telefoon = "";
    export let emailAdres = "";
</script>

<!-- Praktijknaam -->
<LabeledInput
    id="Praktijknaam"
    label="Praktijknaam"
    placeholder=""
    bind:value={praktijkNaam}
    tooltipText=""
    showTooltip={false}
/>

<!-- Achternaam -->
<LabeledInput
    id="Achternaam"
    label="Achternaam"
    placeholder=""
    bind:value={achterNaam}
    tooltipText=""
    showTooltip={false}
/>

<!-- Plaats -->
<LabeledInput
    id="Plaats"
    label="Plaats"
    placeholder=""
    bind:value={plaats}
    tooltipText=""
    showTooltip={false}
/>

<!-- Telefoon -->
<LabeledInput
    id="Telefoon"
    label="Telefoon"
    placeholder=""
    bind:value={telefoon}
    tooltipText=""
    showTooltip={false}
/>

<!-- Email -->
<LabeledInput
    id="Emailadres"
    label="Emailadres"
    placeholder=""
    bind:value={emailAdres}
    tooltipText=""
    showTooltip={false}
/>

<!-- Opslaan -->
<div class="flex flex-col items-start">
    <SimpleButton
        text="Opslaan"
        bgColor="#0C3966"
        textColor="#FFF"
        onClick={handleOpslaan}
    />
</div>
