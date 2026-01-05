<script lang="ts">
    import LabeledOutput from "$lib/components/form/LabeledOutput.svelte";
    import LabeledSliderInfo from "$lib/components/composits/LabeledSliderInfo.svelte";

    export let email = "example@gmail.com";
    export let newsletterEnabled: boolean = true;
    export let gegevensWaarschuwingEnabled: boolean = false;
</script>

<div
    class="flex flex-col justify-center items-center gap-3 flex-1 self-stretch px-6 bg-[#0C3966]"
>
    <!-- Uw emailadres -->
    <div
        class="flex flex-col justify-center items-center self-stretch max-w-[600px]"
    >
        <LabeledOutput label="Uw emailadres" value={email} />
    </div>

    <!-- Ontvang de nieuwsbrief -->
    <LabeledSliderInfo
        label="Ontvang SOStag nieuwsbrief op uw mail"
        tooltipText="Ontvang een nieuwsbrief op uw mail met handige informatie over onze zorg."
        statusTextTrue="U ontvangt momenteel wel een nieuwsbrief"
        statusTextFalse="U ontvangt momenteel geen nieuwsbrief"
        bind:checked={newsletterEnabled}
        handleColor="#FFF"
        trueColor="#45B652"
        statusTextColor="#FFF"
    />

    <!-- Waarschuw voor bijwerken gegevens -->
    <LabeledSliderInfo
        label="Waarschuw mij per mail om mijn gegevens bij te werken"
        tooltipText="Mits er gegevens ontbreken of niet meer actueel zijn, dan zal u via mail hierover op de hoogte worden gehouden."
        statusTextTrue="U wordt momenteel wel via mail gewaarschuwd"
        statusTextFalse="U wordt momenteel niet via mail gewaarschuwd"
        bind:checked={gegevensWaarschuwingEnabled}
        handleColor="#FFF"
        trueColor="#45B652"
        statusTextColor="#FFF"
    />
</div>
