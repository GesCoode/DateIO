<script lang="ts">
    import InputField from "$lib/components/form/LabeledInput.svelte";
    import LabeledSliderInfo from "$lib/components/composits/LabeledSliderInfo.svelte";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let nummer: number = 1; // Contactpersoon number
    export let deletable: boolean = false; // whether the cross should appear

    export let Naam = "";
    export let Relatie = "";
    export let Telefoon = "";
    export let Mobiel = "";
    export let Emailadres = "";

    export let contactPersoonMailen: boolean = false;
</script>

<div class="flex flex-col gap-4">
    <!-- Header row with optional delete -->
    <div class="flex items-center justify-between">
        <div class="text-black font-heebo text-sm font-bold capitalize">
            Contactpersoon {nummer}
        </div>

        {#if deletable}
            <button
                type="button"
                class="shrink-0 text-gray-400 hover:text-red-600 transition text-sm"
                aria-label="Verwijderen"
                on:click={() => dispatch("delete")}
            >
                ✕
            </button>
        {/if}
    </div>

    <InputField
        label="Naam"
        id={`Naam-${nummer}`}
        placeholder=""
        bind:value={Naam}
    />
    <InputField
        label="Relatie"
        id={`Relatie-${nummer}`}
        placeholder=""
        bind:value={Relatie}
    />
    <InputField
        label="Telefoon"
        id={`Telefoon-${nummer}`}
        placeholder=""
        bind:value={Telefoon}
    />
    <InputField
        label="Mobiel"
        id={`Mobiel-${nummer}`}
        placeholder=""
        bind:value={Mobiel}
    />
    <InputField
        label="Emailadres"
        id={`Emailadres-${nummer}`}
        placeholder=""
        bind:value={Emailadres}
    />

    <LabeledSliderInfo
        label="Bericht per mail als SOStag gescand wordt"
        tooltipText=""
        statusTextTrue="Contactpersoon ontvangt wel een mail"
        statusTextFalse="Contactpersoon ontvangt geen mail"
        bind:checked={contactPersoonMailen}
        handleColor="#FFF"
        trueColor="#45B652"
        statusTextColor="#374151"
        showTooltip={false}
    />

    <hr class="border-t border-gray-500 w-full" />
</div>
